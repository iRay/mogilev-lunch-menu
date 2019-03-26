from datetime import datetime
from config import database
import sqlite3


def get_users_to_notify():
    """
    Get users for sending restaurants notifications
    :return:
    """
    db = sqlite3.connect(database)
    cursor = db.cursor()
    query = "SELECT chat_id, notify_at FROM notifications WHERE status=1"
    users = cursor.execute(query)
    result = users.fetchall()
    selected_users = [
        {"chat_id": list(user)[0], "time": list(user)[1]} for user in result
    ]
    db.close()

    return selected_users


def set_user_notification(notify, notify_flag=False):
    """
    Set user notification status
    :param notify:
    :param notify_flag:
    :return:
    """
    chat_id = notify.get("chat_id", 1)
    status = notify.get("status", notify_flag)
    notify_at = notify.get("notify_at", "")

    db = sqlite3.connect(database)
    cursor = db.cursor()

    query_update = (
        f"UPDATE notifications SET notify_at='{notify_at}', updated_at='{datetime.now()}', status='{status}' "
        f" WHERE chat_id='{chat_id}'"
    )
    cursor.execute(query_update)

    query_insert = (
        f"INSERT OR IGNORE INTO notifications ('chat_id', 'status', 'notify_at', 'updated_at')"
        f" VALUES ('{chat_id}', '{status}', '{notify_at}', '{datetime.now()}')"
    )
    cursor.execute(query_insert)

    db.commit()
    db.close()
