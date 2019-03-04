from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    Filters,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
)

from .materik import Materik
from .vangog import Vangog

from util import (
    kb_materik_menu_select,
    STATE,
    cancel,
    msg,
    log_request,
    reply_keyboard_restaurants,
    kb_notifications,
    start_conversation)


@log_request
def restaurant(update: Update, context: CallbackContext):
    selected_restaurant = update.message.text.strip().lower()
    if selected_restaurant == "материк":
        update.message.reply_text(
            "выберите меню",
            reply_markup=ReplyKeyboardMarkup(
                kb_materik_menu_select, resize_keyboard=True
            ),
        )
        return STATE["MATERIK"]

    if selected_restaurant == "вангог":
        update.message.reply_text(
            msg["wait_a_moment"],
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_restaurants, resize_keyboard=True
            ),
        )
        Vangog.menu(update, context)
        return STATE["RESTAURANT"]


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^(материк|вангог)$"), start_conversation)],
    states={
        STATE["RESTAURANT"]: [
            MessageHandler(Filters.regex("^(материк|вангог)$"), restaurant)
        ],
        STATE["MATERIK"]: [
            MessageHandler(
                Filters.regex("^(меню\sна\sсегодня.+|меню\sна\sнеделю.+)$"),
                Materik.menu,
            )
        ],
        STATE["VANGOG"]: [MessageHandler(Filters.regex("^(вангог)$"), Vangog.menu)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)


@log_request
def restaurant_notifications(update: Update, context: CallbackContext):
    selected_restaurant = update.message.text.strip().lower()
    if selected_restaurant == "материк":
        update.message.reply_text(
            "materik notifications",
            reply_markup=ReplyKeyboardMarkup(kb_notifications, resize_keyboard=True),
        )
        return STATE["NOTIFY_MATERIK"]

    if selected_restaurant == "вангог":
        update.message.reply_text(
            "vangog notifications",
            reply_markup=ReplyKeyboardMarkup(kb_notifications, resize_keyboard=True),
        )
        return STATE["NOTIFY_VANGOG"]


def notify_materik(update: Update, context: CallbackContext):
    action = update.message.text.strip().lower()
    handle_action(update=update, restaurant="materik", action=action)
    return ConversationHandler.END


def notify_vangog(update: Update, context: CallbackContext):
    action = update.message.text.strip().lower()
    handle_action(update=update, restaurant="vangog", action=action)
    return ConversationHandler.END


def handle_action(update, restaurant, action):
    msg = ""
    if action.startswith("включить"):
        msg = f"уведомления включены для {restaurant}"
    if action.startswith("отключить"):
        msg = f"уведомления отключены для {restaurant}"
    update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard_restaurants, resize_keyboard=True),
    )


def notify_conversation(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Для какого заведения включить уведомления?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_restaurants, resize_keyboard=True
        ),
    )
    return STATE["NOTIFICATIONS"]


notification_conversation = ConversationHandler(
    entry_points=[CommandHandler("notify", notify_conversation)],
    states={
        STATE["NOTIFICATIONS"]: [
            MessageHandler(
                Filters.regex("^(материк|вангог)$"), restaurant_notifications
            )
        ],
        STATE["NOTIFY_MATERIK"]: [
            MessageHandler(
                Filters.regex("^(включить.*|отключить.*)$"), notify_materik
            )
        ],
        STATE["NOTIFY_VANGOG"]: [
            MessageHandler(
                Filters.regex("^(включить.*|отключить.*)$"), notify_vangog
            )
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
