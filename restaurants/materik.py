import re
from typing import Optional, List
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from telegram import Update, ReplyKeyboardMarkup
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
