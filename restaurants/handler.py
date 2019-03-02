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
    start,
    cancel,
    msg
)


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
        update.message.reply_text(msg["wait_a_moment"])
        Vangog.menu(update, context)


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, start)],
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
        STATE["VANGOG"]: [MessageHandler(Filters.text, Vangog.menu)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
