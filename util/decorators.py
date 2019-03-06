from functools import wraps
from telegram import ChatAction
from .db import save_req_info
from util.models import User


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=action
            )
            return func(bot, update, **kwargs)

        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)


def log_request(handler):
    """ Log request to DB """

    def wrapper(*args, **kwargs):
        if hasattr(args[0]["message"], "to_dict"):
            msg = args[0]["message"].to_dict()
            user = User()
            user.id = msg["from"].get("id", "n/a")
            user.username = msg["from"].get("username", "n/a")
            user.first_name = msg["from"].get("first_name", "n/a")
            user.last_name = msg["from"].get("last_name", "n/a")
            user.text = msg["text"]
            save_req_info(user)
        return handler(*args, **kwargs)

    return wrapper
