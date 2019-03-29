from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from util import kb_restaurants

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Выберите ресторан",
        reply_markup=ReplyKeyboardMarkup(
            kb_restaurants, resize_keyboard=True, one_time_keyboard=True
        ),
    )


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Выберите ресторан",
        reply_markup=ReplyKeyboardMarkup(
            kb_restaurants, resize_keyboard=True
        ),
    )
    return ConversationHandler.END


def error_callback(update, context):
    if context.error.message == "Message is not modified":
        return
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Нет, нет такой команды... ¯\_(ツ)_/¯", reply_markup=kb_restaurants
    )
