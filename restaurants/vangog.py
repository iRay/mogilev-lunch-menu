import re
import requests
from selenium import webdriver

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from util import reply_keyboard_restaurants, msg
from config import restaurant


class Vangog:
    @classmethod
    def menu(cls, update: Update, context: CallbackContext):
        menu = cls.fetch_menu()
        if menu:
            context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=menu,
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard_restaurants, resize_keyboard=True
                ),
            )
        else:
            update.message.reply_text(
                msg["sorry_no_menu"],
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard_restaurants, resize_keyboard=True
                ),
            )

    @staticmethod
    def init_driver():
        """
        Selenium driver initialization
        :return:
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.headless = True
        # driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)
        driver.set_window_size(1024, 768)
        return driver

    @staticmethod
    def fetch_menu():
        img_url = ""
        driver = Vangog.init_driver()
        try:
            url = restaurant["vangog"]["instagram"]["url"]
            driver.get(url)
            posts = driver.find_elements_by_xpath(
                restaurant["vangog"]["instagram"]["posts_xpath"]
            )
            for post in posts:
                post_url = post.get_attribute("href")
                page_src = requests.get(post_url).text
                menu = re.findall(r".+(обеденное\s+меню).+", page_src)
                tags = re.findall(
                    restaurant["vangog"]["instagram"]["tags_regexp"], page_src
                )
                if menu or tags:
                    img = post.find_element_by_css_selector("img")
                    img_url = img.get_attribute("src")
                    driver.quit()
                    return img_url
        except:
            driver.quit()
        finally:
            driver.quit()
            return img_url
