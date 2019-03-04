import sqlite3
from datetime import datetime
from config import database


def save_req_info(user):
    user_id = user.id
    user_name = user.username
    first_name = user.first_name
    last_name = user.last_name
    request_text = user.text

    db = sqlite3.connect(database)
    cursor = db.cursor()
    query = (
        f"INSERT INTO users ('chat_id', 'user_name', 'first_name', 'last_name', 'request_text', 'created_at', 'updated_at')"
        f" VALUES ('{user_id}', '{user_name}', '{first_name}', '{last_name}','{request_text}', '{datetime.now()}', '{datetime.now()}')"
    )
    cursor.execute(query)
    db.commit()
    db.close()
