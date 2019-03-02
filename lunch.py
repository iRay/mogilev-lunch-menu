#!/usr/bin/env python

from telegram.ext import Updater, MessageHandler, Filters

from config import telegram_bot
from util import error_callback, unknown
from restaurants import conv_handler


def main():
    updater = Updater(telegram_bot["token"], use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error_callback)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
