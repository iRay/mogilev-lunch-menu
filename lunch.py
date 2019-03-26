#!/usr/bin/env python

from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackQueryHandler,
    TypeHandler,
)

from config import telegram_bot
from restaurants.models import UserNotification
from util import error_callback, unknown, start
from restaurants import (
    notification_conversation,
    Materik,
    menu_materik,
    menu_vangog,
    menu_pizzaroni,
    ScheduleMenu,
)
from restaurants.handler import notify_user


def main():
    updater = Updater(telegram_bot["token"], use_context=True)
    dispatcher = updater.dispatcher

    ScheduleMenu(dispatcher)
    notification_dispatch_handler = TypeHandler(UserNotification, notify_user, updater)
    dispatcher.add_handler(notification_dispatch_handler)

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(notification_conversation)

    materik_handler = MessageHandler(Filters.regex("^(материк)$"), menu_materik)
    vangog_handler = MessageHandler(Filters.regex("^(вангог)$"), menu_vangog)
    pizzaroni_handler = MessageHandler(Filters.regex("^(пиццарони)$"), menu_pizzaroni)

    dispatcher.add_handler(materik_handler)
    dispatcher.add_handler(vangog_handler)
    dispatcher.add_handler(pizzaroni_handler)
    dispatcher.add_handler(
        CallbackQueryHandler(Materik.menu_handler, pass_user_data=True)
    )

    dispatcher.add_error_handler(error_callback)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
