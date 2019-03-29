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
from restaurants.handler import notifications_handler, notify_time
from util import error_callback, unknown, start
from restaurants import (
    restaurant_notifications,
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

    notify_command_handler = CommandHandler(
        "notify", restaurant_notifications, pass_user_data=True
    )
    dispatcher.add_handler(notify_command_handler)

    dispatcher.add_handler(
        CallbackQueryHandler(notifications_handler, pass_user_data=True)
    )
    notify_time_handler = MessageHandler(
        Filters.regex(r"^\d{1,2}\s*[\.:\s+,]\s*\d{1,2}$"), notify_time
    )
    dispatcher.add_handler(notify_time_handler)

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
