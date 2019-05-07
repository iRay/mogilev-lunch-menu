import re
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext

from .materik import Materik
from .vangog import Vangog
from .pizzaroni import Pizzaroni
from .kinza import Kinza
from .db import set_user_notification
from .models import RestaurantMenuImage

from util import msg, kb_restaurants, restaurants


def callback_context_handler(update: Update, context: CallbackContext):
    user_context = context.user_data["context"]
    if user_context == "kinza":
        Kinza.menu_handler(update=update, context=context)
    if user_context == "materik":
        Materik.menu_handler(update=update, context=context)
    if user_context == "notifications":
        notifications_handler(update=update, context=context)


def notify_user(notify, updater):
    """
    Send notification to user
    :param notify:
    :param updater:
    :return:
    """
    if notify.restaurant in ["vangog", "pizzaroni"]:
        restaurant_menu = RestaurantMenuImage(notify.restaurant).fetch_menu()
        updater.bot.send_photo(
            notify.chat_id,
            photo=restaurant_menu,
            caption=notify.msg,
            reply_markup=ReplyKeyboardMarkup(kb_restaurants, resize_keyboard=True),
        )
    else:
        updater.bot.send_message(
            notify.chat_id,
            notify.msg,
            reply_markup=ReplyKeyboardMarkup(kb_restaurants, resize_keyboard=True),
        )


def menu_materik(update: Update, context: CallbackContext):
    """
    Get materik menu
    :param update:
    :param context:
    :return:
    """
    clean_current_context(update=update, context=context)
    Materik.get_menu(update, context)


def menu_vangog(update: Update, context: CallbackContext):
    """
    Get vangog menu
    :param update:
    :param context:
    :return:
    """
    update.message.reply_text(
        msg["wait_a_moment"],
        reply_markup=ReplyKeyboardMarkup(kb_restaurants, resize_keyboard=True),
    )
    Vangog(update=update, context=context)


def menu_pizzaroni(update: Update, context: CallbackContext):
    """
    Get pizzaroni menu
    :param update:
    :param context:
    :return:
    """
    update.message.reply_text(
        msg["wait_a_moment"],
        reply_markup=ReplyKeyboardMarkup(kb_restaurants, resize_keyboard=True),
    )
    Pizzaroni(update=update, context=context)


def menu_kinza(update: Update, context: CallbackContext):
    """
    Get kinza menu
    :param update:
    :param context:
    :return:
    """
    clean_current_context(update=update, context=context)
    Kinza.menu(update=update, context=context)


def restaurant_notifications(update: Update, context: CallbackContext):
    """
    Restaurants notifications menu
    :param update:
    :param context:
    :return:
    """
    context.user_data["context"] = "notifications"
    context.user_data["notify"] = {
        "chat_id": update.message.chat_id,
        "time": "",
        "restaurant": "",
        "status": "",
    }
    buttons = [
        [
            InlineKeyboardButton(
                "материк", callback_data=f'restaurant_{restaurants["MATERIK"]}'
            ),
            InlineKeyboardButton(
                "вангог", callback_data=f'restaurant_{restaurants["VANGOG"]}'
            )
        ], [
            InlineKeyboardButton(
                "пиццарони", callback_data=f'restaurant_{restaurants["PIZZARONI"]}'
            ),
            InlineKeyboardButton(
                "кинза", callback_data=f'restaurant_{restaurants["KINZA"]}'
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Выберите заведение", reply_markup=reply_markup)


def notifications_handler(update: Update, context: CallbackContext):
    """
    User's notification handler
    :param update:
    :param context:
    :return:
    """
    query = update.callback_query
    if query.data.startswith("restaurant_"):
        context.user_data["notify"]["restaurant"] = query.data
        reply_text = "Выберите действие"
        buttons = [
            [
                InlineKeyboardButton("включить 🔔", callback_data="notify_1"),
                InlineKeyboardButton("отключить 🔕", callback_data="notify_0"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        query.edit_message_text(text=reply_text, reply_markup=reply_markup)

    if query.data.startswith("notify_"):
        """ Check user's notification status selection """
        status = int(query.data.split("_")[1])
        context.user_data["notify"]["status"] = status
        if not status:
            notify_info = set_user_notification(context.user_data["notify"])
            query.message.reply_text(
                f'уведомления {notify_info["status"]} для заведения {notify_info["restaurant"]}',
                reply_markup=ReplyKeyboardMarkup(kb_restaurants, resize_keyboard=True),
            )
            del context.user_data["notify"]
        else:
            query.message.reply_text(
                "введите время для уведомлений, например: 11:50",
                reply_markup=ReplyKeyboardMarkup(kb_restaurants, resize_keyboard=True),
            )


def notify_time(update: Update, context: CallbackContext):
    """
    Set user's notification time
    :param update:
    :param context:
    :return:
    """
    time = re.compile(r"[\.:\s+,]").split(update.message.text.strip())
    hours, minutes = list(filter(None, time))
    if int(hours) > 24 or int(minutes) > 59:
        update.message.reply_text(
            "Вы, видимо, ошиблись при вводе времени. Начните заново.",
            reply_markup=ReplyKeyboardMarkup(kb_restaurants, resize_keyboard=True),
        )
    if "notify" in context.user_data:
        context.user_data["notify"]["time"] = f"{hours}:{minutes}"
        notify_info = set_user_notification(context.user_data["notify"])
        update.message.reply_text(
            f'уведомления {notify_info["status"]} для заведения {notify_info["restaurant"]}',
            reply_markup=ReplyKeyboardMarkup(kb_restaurants, resize_keyboard=True),
        )
        del context.user_data["notify"]


def clean_current_context(update: Update, context: CallbackContext):
    """
    Clean current user context for handling callbacks
    :param update:
    :param context:
    :return:
    """
    context.user_data["context"] = ""
    context.user_data["menu_options"] = {}
    context.user_data["menu_options_selected"] = {}
    context.user_data["menu_price"] = 0
