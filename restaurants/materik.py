import re
from typing import List, Dict, Tuple
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from util import ru_month, ru_weekday, msg
from config import restaurant


class Materik:
    @classmethod
    def fetch_menu(cls):
        """
        Fetching Materik menu
        :return:
        """
        response_index = requests.get(restaurant["materik"]["site_url"])
        soup_index = BeautifulSoup(response_index.text, features="html.parser")

        pattern_menu = re.compile("^https?://materik.by/obedennoe-menyu")
        new_menu_url = [
            el["href"]
            for el in soup_index.findAll("a")
            if re.match(pattern_menu, el["href"])
        ]

        response_menu_page = requests.get(new_menu_url[0])

        pattern = re.compile(r"(\d{1,2}\.\d{1,2})")
        named_days = False
        pattern_named = re.compile(r"([а-яА-Я]+\s+\d{1,2}\s+[а-яА-Я]+)")

        soup_menu_page = BeautifulSoup(response_menu_page.text, features="html.parser")
        content = soup_menu_page.find_all(
            "div", {"class": "apachkin-postcontent clearfix"}
        )
        menu = content[1].text

        elements = [el for el in re.split(pattern, menu) if el]
        if len(elements) == 1:
            named_days = True
            elements = [el for el in re.split(pattern_named, menu) if el]

        def get_days(items) -> List:
            group = []
            if named_days:
                pattern = pattern_named
            for idx, el in enumerate(items):
                if re.match(pattern, el):
                    group.extend([el, items[idx + 1]])
                    yield group
                    group = []

        week_days = dict(get_days(elements))
        menu_for = str(datetime.now().day) + "." + str(datetime.now().month)
        if named_days:
            curr_day = datetime.now().isoweekday()
            for day in week_days.keys():
                if ru_weekday[curr_day] in day:
                    menu_for = day

        curr_day = datetime.now().day
        curr_month = datetime.now().month
        day = set(week_days.keys()) & {
            menu_for,
            f"0{menu_for}",
            f"0{curr_day}.{curr_month}",
            f"{curr_day}.0{curr_month}",
        }
        if day:
            menu = week_days.get(day.pop(), None)
            if menu is None:
                return None, None, msg["sorry_no_menu"]

        return curr_day, curr_month, menu

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
            re_option_price = re.findall(r"(\d+)р\.(\d+)к", options[query.data])
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
                    [InlineKeyboardButton(v, callback_data=k)] for k, v in options.items()
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
        menu_for, options = cls.parse_menu_items()
        if not menu_for:
            menu_for = msg["lunch_menu"]
        buttons = [
            [InlineKeyboardButton(v, callback_data=k)] for k, v in options.items()
        ]
        reply_markup = InlineKeyboardMarkup(list(buttons))

        context.user_data["context"] = "materik"
        context.user_data["menu_options"] = options
        context.user_data["menu_options_selected"] = {}
        context.user_data["menu_price"] = 0
        update.message.reply_text(menu_for, reply_markup=reply_markup)

    @classmethod
    def parse_menu_items(cls) -> Tuple[str, Dict[str, str]]:
        """
        Parse menu items
        :return:
        """
        menu_for = ""
        options = {}
        day, month, menu = cls.fetch_menu()
        if day is not None and month is not None:
            today = f"{int(day)}е {ru_month[int(month)]}"
            menu_for = f"{msg['menu_for']} {today}"

        items = re.split(r"\.\n", menu)
        for idx, item in enumerate(items):
            options[f"materik_{str(idx)}"] = re.sub(r"\s+", " ", item.strip())

        return menu_for, options
