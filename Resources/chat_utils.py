import sqlite3
from datetime import datetime

DB_FILE = 'chat.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            message TEXT,
            ticket_id INTEGER NOT NULL,
            image BLOB,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_message(sender, receiver, message, ticket_id, image):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (sender, receiver, message, ticket_id, image, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (sender, receiver, message, ticket_id, image, datetime.now()))
    conn.commit()
    conn.close()

def get_messages(user1, user2, ticket_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sender, message, image, timestamp FROM messages
        WHERE ((sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)) AND (ticket_id = ?)
        ORDER BY timestamp
    ''', (user1, user2, user2, user1, ticket_id))
    messages = cursor.fetchall()
    conn.close()
    return messages
