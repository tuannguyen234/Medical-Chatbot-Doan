import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
HISTORY_DB_PATH = os.getenv("HISTORY_DB_PATH", "app/database/history_dialogs/chat_history.db")

# Lưu vào database
def save_message(user, message, image_path=None):
    conn = sqlite3.connect(HISTORY_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chats (user, message, image_path, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user, message, image_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# Take last messages
def get_last_messages(limit=5):
    conn = sqlite3.connect(HISTORY_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user, message, image_path FROM chats
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]  # đảo ngược lại cho đúng thứ tự

# Take last user queries
def get_last_user_queries(limit = 5):
    conn = sqlite3.connect(HISTORY_DB_PATH)
    cursor = conn.                                                                                                                                                            cursor()
    cursor.execute("""
        SELECT message FROM chats
        WHERE user = 'user'
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows][::-1]  # đảo ngược lại cho đúng thứ tự

