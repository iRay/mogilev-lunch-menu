from datetime import datetime
from config import database
import sqlite3

from util import restaurant_name


def get_users_to_notify():
    """
    Get users for sending restaurants notifications
    :return:
    """
    db = sqlite3.connect(database)
    cursor = db.cursor()
    query = "SELECT chat_id, notify_at, restaurant_id FROM notifications WHERE status=1"
    users = cursor.execute(query)
    result = users.fetchall()
    selected_users = [
        {"chat_id": list(user)[0], "time": list(user)[1], "restaurant": list(user)[2]}
        for user in result
    ]
    db.close()

    return selected_users


def set_user_notification(notification_data):
    """
    Set user notification status
    :return:
    """
    if not notification_data:
        return
    chat_id = notification_data["chat_id"]
    status = notification_data["status"]
    notify_at = notification_data["time"]
    restaurant_id = notification_data["restaurant"].split("_")[1]

    notify_info = {
        "status": "включены" if int(status) else "выключены",
        "restaurant": restaurant_name[restaurant_id],
    }

    db = sqlite3.connect(database)
    cursor = db.cursor()

    find_notify_record = f"SELECT id FROM notifications WHERE chat_id={chat_id} AND restaurant_id={restaurant_id}"
    notify_record = cursor.execute(find_notify_record)
    if len(notify_record.fetchall()):
        query_update = (
            f"UPDATE notifications SET notify_at='{notify_at}', updated_at='{datetime.now()}', status='{status}' "
            f" WHERE chat_id='{chat_id}' AND restaurant_id='{restaurant_id}'"
        )
        cursor.execute(query_update)
    else:
        query_insert = (
            f"INSERT OR IGNORE INTO notifications ('chat_id', 'restaurant_id', 'status', 'notify_at', 'created_at', 'updated_at')"
            f" VALUES ('{chat_id}', '{restaurant_id}', '{status}', '{notify_at}', '{datetime.now()}', '{datetime.now()}')"
        )
        cursor.execute(query_insert)

    db.commit()
    db.close()

    return notify_info
