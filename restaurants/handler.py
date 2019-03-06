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
    STATE,
    cancel,
    msg,
    log_request,
    reply_keyboard_restaurants,
    kb_notifications,
)


@log_request
def menu_materik(update: Update, context: CallbackContext):
    Materik.get_menu(update, context)


@log_request
def menu_vangog(update: Update, context: CallbackContext):
    update.message.reply_text(
        msg["wait_a_moment"],
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_restaurants, resize_keyboard=True
        ),
    )
    Vangog.menu(update, context)


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


@log_request
def notify_materik(update: Update, context: CallbackContext):
    action = update.message.text.strip().lower()
    handle_action(update=update, restaurant="materik", action=action)
    return ConversationHandler.END


@log_request
def notify_vangog(update: Update, context: CallbackContext):
    action = update.message.text.strip().lower()
    handle_action(update=update, restaurant="vangog", action=action)
    return ConversationHandler.END


@log_request
def handle_action(update, restaurant, action):
    msg = ""
    if action.startswith("включить"):
        msg = f"уведомления включены для {restaurant}"
    if action.startswith("отключить"):
        msg = f"уведомления отключены для {restaurant}"
    update.message.reply_text(
        msg,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_restaurants, resize_keyboard=True
        ),
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
            MessageHandler(Filters.regex("^(включить.*|отключить.*)$"), notify_materik)
        ],
        STATE["NOTIFY_VANGOG"]: [
            MessageHandler(Filters.regex("^(включить.*|отключить.*)$"), notify_vangog)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
