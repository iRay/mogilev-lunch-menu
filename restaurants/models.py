import re
import requests
from selenium import webdriver

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from util import reply_keyboard_restaurants, msg
from config import restaurant


class InstagramMenu:
    def __init__(self, restaurant, update: Update, context: CallbackContext):
        self.restaurant = restaurant
        self.update = update
        self.context = context
        self.menu()

    def menu(self):
        menu = self.fetch_menu()
        if menu:
            self.context.bot.send_photo(
                chat_id=self.update.message.chat_id,
                photo=menu,
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard_restaurants, resize_keyboard=True
                ),
            )
        else:
            self.update.message.reply_text(
                msg["sorry_no_menu"],
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard_restaurants, resize_keyboard=True
                ),
            )

    @classmethod
    def init_driver(cls):
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

    def fetch_menu(self):
        img_url = ""
        driver = self.init_driver()
        try:
            url = restaurant[self.restaurant]["instagram"]["url"]
            driver.get(url)
            posts = driver.find_elements_by_xpath(
                restaurant[self.restaurant]["instagram"]["posts_xpath"]
            )
            for post in posts:
                post_url = post.get_attribute("href")
                page_src = requests.get(post_url).text
                menu = re.findall(r".+(обеденное\s+меню).+", page_src)
                tags = re.findall(
                    restaurant[self.restaurant]["instagram"]["tags_regexp"], page_src
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


class UserNotification:
    def __init__(self, chat_id, msg):
        self.chat_id = chat_id
        self.msg = msg
