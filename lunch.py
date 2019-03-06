#!/usr/bin/env python

from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackQueryHandler,
)

from config import telegram_bot
from util import error_callback, unknown, start
from restaurants import notification_conversation, Materik, menu_materik, menu_vangog


def main():
    updater = Updater(telegram_bot["token"], use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    materik_handler = MessageHandler(Filters.regex("^(материк)$"), menu_materik)
    vangog_handler = MessageHandler(Filters.regex("^(вангог)$"), menu_vangog)
    dispatcher.add_handler(materik_handler)
    dispatcher.add_handler(vangog_handler)
    dispatcher.add_handler(
        CallbackQueryHandler(Materik.menu_handler, pass_user_data=True)
    )
    dispatcher.add_handler(notification_conversation)

    dispatcher.add_error_handler(error_callback)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
