import re
from typing import Dict

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from util import msg
from config import restaurant
from util import init_driver


class Kinza:
    restaurant = "kinza"

    @classmethod
    def menu(cls, update: Update, context: CallbackContext):
        cls.get_menu(update=update, context=context)

    @classmethod
    def fetch_menu(cls):
        lunch_menu = ""
        driver = init_driver()
        try:
            url = restaurant[cls.restaurant]["site_url"]
            driver.get(url)
            menu = driver.find_element_by_xpath(
                restaurant[cls.restaurant]["menu_xpath"]
            )
            lunch_menu = menu.text
        except:
            driver.quit()
        finally:
            driver.quit()
            return lunch_menu

    @classmethod
    def menu_handler(cls, update: Update, context: CallbackContext):
        """
        Menu items selection handler
        :param update:
        :param context:
        :return:
        """
        query = update.callback_query
        options = context.user_data["menu_options"]
        added_options = context.user_data["menu_options_selected"]

        if query.data in options:
            re_option_price = re.findall(r"(\d+),(\d+)\s*руб", options[query.data])
            if re_option_price:
                option_price = re_option_price.pop()
                item_price = int(option_price[0]) + float(option_price[1]) / 100

                if query.data in added_options:
                    context.user_data["menu_price"] -= item_price
                    options[query.data] = added_options[query.data]
                    del added_options[query.data]
                else:
                    added_options[query.data] = options[query.data]
                    options[query.data] = f"✅ {options[query.data]}"
                    context.user_data["menu_price"] += item_price

                price = "{0:.2f}".format(abs(context.user_data["menu_price"]))

                buttons = [
                    [InlineKeyboardButton(v, callback_data=k)]
                    for k, v in options.items()
                ]
                reply_markup = InlineKeyboardMarkup(list(buttons))

                query.edit_message_text(
                    text=f"{msg['lunch_price']}: {price}", reply_markup=reply_markup
                )

    @classmethod
    def get_menu(cls, update: Update, context):
        """
        Get and prepare menu and appropriate inline keyboard
        :param update:
        :param context:
        :return:
        """
        options = cls.parse_menu_items()
        buttons = [
            [InlineKeyboardButton(v, callback_data=k)] for k, v in options.items()
        ]
        reply_markup = InlineKeyboardMarkup(list(buttons))

        context.user_data["context"] = "kinza"
        context.user_data["menu_options"] = options
        context.user_data["menu_options_selected"] = {}
        context.user_data["menu_price"] = 0
        update.message.reply_text("Обеденное меню", reply_markup=reply_markup)

    @classmethod
    def parse_menu_items(cls) -> Dict[str, str]:
        """
        Parse menu items
        :return:
        """
        menu = cls.fetch_menu()
        items = re.split(r"\n", menu)
        options = {}
        item_count = 0
        for item in items:
            curr_item = item.strip()
            if re.match(r".+\s+руб", curr_item):
                options[f"kinza_{str(item_count)}"] = curr_item
                item_count += 1

        return options
