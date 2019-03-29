import sqlite3

conn = sqlite3.connect("config/lunch.db")
cursor = conn.cursor()

create_users = """
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY,
 chat_id INTEGER NOT NULL,
 user_name VARCHAR(32) DEFAULT NULL,
 first_name VARCHAR(32) DEFAULT NULL,
 last_name VARCHAR(32) DEFAULT NULL,
 request_text TEXT DEFAULT '',
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL
);
"""

create_restaurants = """
CREATE TABLE IF NOT EXISTS restaurants (
 id INTEGER PRIMARY KEY,
 name VARCHAR(64) DEFAULT NULL,
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL
);
"""

create_notifications = """
CREATE TABLE IF NOT EXISTS notifications (
 id INTEGER PRIMARY KEY,
 chat_id INTEGER NOT NULL,
 restaurant_id INTEGER NOT NULL,
 status INTEGER DEFAULT 0,
 notify_at text DEFAULT '',
 created_at TEXT NOT NULL,
 updated_at TEXT NOT NULL
);
"""

cursor.execute(create_users)
cursor.execute(create_restaurants)
cursor.execute(create_notifications)
conn.commit()

conn.close()
