import re
from typing import Optional, List, Dict
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from util import STATE, reply_keyboard_restaurants, ru_month, msg
from config import restaurant


class Materik:
    @classmethod
    def menu(cls, update: Update, context: CallbackContext):
        menu_for = update.message.text.strip().lower()
        if menu_for.startswith("меню на сегодня"):
            day, month, menu = cls.fetch_menu("today")
            if day is None or month is None:
                update.message.reply_text(
                    menu,
                    reply_markup=ReplyKeyboardMarkup(
                        reply_keyboard_restaurants, resize_keyboard=True
                    ),
                )
            else:
                today = f"{int(day)}е {ru_month[int(month)]}"
                update.message.reply_text(
                    f"меню ♨ на *{today}* \n" f"{menu}",
                    reply_markup=ReplyKeyboardMarkup(
                        reply_keyboard_restaurants, resize_keyboard=True
                    ),
                )
        if menu_for.startswith("меню на неделю"):
            menu = cls.fetch_menu("week")
            update.message.reply_text(
                f"меню ♨ на *неделю* \n" f"{menu}",
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard_restaurants, resize_keyboard=True
                ),
            )

        return STATE["RESTAURANT"]

    @classmethod
    def get_date(cls, day=None) -> Optional[str]:
        if day is not None:
            requested_day = day.strip().lower()
            if requested_day == "today":
                return str(datetime.now().day) + "." + str(datetime.now().month)
            if requested_day == "week":
                return "week"
        return None

    @classmethod
    def fetch_menu(cls, day=None):
        response_index = requests.get(restaurant["materik"]["site_url"])
        soup_index = BeautifulSoup(response_index.text, features="html.parser")

        pattern_menu = re.compile("^https?://materik.by/obedennoe-menyu")
        new_menu_url = [
            el["href"]
            for el in soup_index.findAll("a")
            if re.match(pattern_menu, el["href"])
        ]

        response_menu_page = requests.get(new_menu_url[0])

        pattern = re.compile("(\d{1,2}\.\d{1,2})")

        soup_menu_page = BeautifulSoup(response_menu_page.text, features="html.parser")
        content = soup_menu_page.find_all(
            "div", {"class": "apachkin-postcontent clearfix"}
        )
        menu = content[1].text

        elements = [el for el in re.split(pattern, menu) if el]

        def get_days(items) -> List:
            group = []
            for idx, el in enumerate(items):
                if re.match(pattern, el):
                    group.extend([el, items[idx + 1]])
                    yield group
                    group = []

        week_days = dict(get_days(elements))
        menu_for = cls.get_date(day)
        if menu_for is None:
            return None, None, msg["sorry_no_menu"]
        elif menu_for == "week":
            return "".join(
                f"меню ♨ на *{key}*{val} \n" for key, val in week_days.items()
            )

        lead_zero_day, lead_zero_month = menu_for.split(".")
        day = set(week_days.keys()) & {
            menu_for,
            f"0{menu_for}",
            f"0{lead_zero_day}.{lead_zero_month}",
            f"{lead_zero_day}.0{lead_zero_month}",
        }
        menu = None
        if len(day):
            menu = week_days.get(day.pop(), None)

        if menu is None:
            return None, None, msg["sorry_no_menu"]

        curr_day, curr_month = menu_for.split(".")
        return curr_day, curr_month, menu

    @classmethod
    def menu_handler(cls, update: Update, context: CallbackContext):
        query = update.callback_query
        options = context.user_data["menu_options"]
        added_options = context.user_data["menu_options_selected"]

        option_price = re.findall(r"(\d+)р\.(\d+)к", options[query.data]).pop()
        item_price = int(option_price[0]) + float(option_price[1]) / 100

        if query.data in added_options:
            context.user_data["menu_price"] -= item_price
            options[query.data] = added_options[query.data]
            del added_options[query.data]
        else:
            added_options[query.data] = options[query.data]
            options[query.data] = f"✅ {options[query.data]}"
            context.user_data["menu_price"] += item_price

        price = "{0:.2f}".format(context.user_data["menu_price"])

        buttons = [[InlineKeyboardButton(v, callback_data=k)] for k, v in options.items()]
        reply_markup = InlineKeyboardMarkup(list(buttons))

        query.edit_message_text(text=f"Цена обеда: {price}", reply_markup=reply_markup)

    @classmethod
    def test_menu(cls, update: Update, context):
        options = cls.parse_menu()
        buttons = [[InlineKeyboardButton(v, callback_data=k)] for k, v in options.items()]
        reply_markup = InlineKeyboardMarkup(list(buttons))

        context.user_data["menu_options"] = options
        context.user_data["menu_options_selected"] = {}
        context.user_data["menu_price"] = 0
        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    @classmethod
    def parse_menu(cls) -> Dict[str, str]:
        menu = cls.fetch_menu(day="today")
        items_string = menu[2:]
        items = re.split(r"\.\n", items_string[0])
        options = {}
        for idx, item in enumerate(items):
            options[str(idx)] = item.strip()

        return options

