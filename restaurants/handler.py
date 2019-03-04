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
    cancel,
    msg,
    log_request,
    reply_keyboard_restaurants,
)


@log_request
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
        update.message.reply_text(
            msg["wait_a_moment"],
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard_restaurants, resize_keyboard=True
            ),
        )
        Vangog.menu(update, context)
        return STATE["RESTAURANT"]


conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^(материк|вангог)$"), restaurant)],
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
        STATE["VANGOG"]: [MessageHandler(Filters.regex("^(вангог)$"), Vangog.menu)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
