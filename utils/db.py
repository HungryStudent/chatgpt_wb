from contextlib import closing
import sqlite3
import time

database = "utils/database.db"


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INT, username TEXT, first_name TEXT, reg_time INT)")
        connection.commit()


def get_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()


def get_users():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users")
        return cursor.fetchall()


def add_user(user_id, username, first_name):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        reg_time = int(time.time())
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                       (user_id, username, first_name, reg_time))
        connection.commit()
