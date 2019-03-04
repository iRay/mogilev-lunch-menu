from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from util import STATE, reply_keyboard_restaurants, log_request

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


@log_request
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Выберите ресторан",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_restaurants, resize_keyboard=True, one_time_keyboard=True
        ),
    )


@log_request
def start_conversation(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Выберите ресторан",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_restaurants, resize_keyboard=True
        ),
    )
    return STATE["RESTAURANT"]


@log_request
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Выберите ресторан",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard_restaurants, resize_keyboard=True
        ),
    )
    return ConversationHandler.END


@log_request
def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


@log_request
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Нет, нет такой команды... ¯\_(ツ)_/¯", reply_markup=reply_keyboard_restaurants
    )
