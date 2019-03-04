#!/usr/bin/env python

from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CommandHandler,
)

from config import telegram_bot
from util import error_callback, unknown, start
from restaurants import conv_handler, notification_conversation


def main():
    updater = Updater(telegram_bot["token"], use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(notification_conversation)
    dispatcher.add_handler(conv_handler)

    dispatcher.add_error_handler(error_callback)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
