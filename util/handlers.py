from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from util import STATE, reply_keyboard_restaurants

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Выберите ресторан",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_restaurants, resize_keyboard=True
        ),
    )
    return STATE["RESTAURANT"]


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Выберите ресторан",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_restaurants, resize_keyboard=True
        ),
    )
    return ConversationHandler.END


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Нет, нет такой команды... ¯\_(ツ)_/¯", reply_markup=reply_keyboard_restaurants
    )
