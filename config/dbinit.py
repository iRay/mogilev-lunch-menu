import sqlite3
from config import db

conn = sqlite3.connect(db)
cursor = conn.cursor()

create_users = """
CREATE TABLE IF NOT EXISTS users (
 id integer PRIMARY KEY,
 chat_id integer NOT NULL,
 user_name text NOT NULL,
 first_name text NOT NULL,
 last_name text NOT NULL,
 request_text text DEFAULT '',
 request_date text NOT NULL
);
"""

create_notifications = """
CREATE TABLE IF NOT EXISTS notifications (
 id integer PRIMARY KEY,
 chat_id integer NOT NULL UNIQUE,
 status integer DEFAULT 0,
 notify_at text DEFAULT '',
 updated_at text NOT NULL
);
"""

cursor.execute(create_users)
cursor.execute(create_notifications)
conn.commit()

conn.close()
