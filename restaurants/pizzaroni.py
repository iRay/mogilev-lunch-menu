from .models import InstagramMenu
from telegram.ext import CallbackContext
from telegram import Update


class Pizzaroni(InstagramMenu):
    def __init__(self, update: Update, context: CallbackContext):
        super().__init__("pizzaroni", update, context)
