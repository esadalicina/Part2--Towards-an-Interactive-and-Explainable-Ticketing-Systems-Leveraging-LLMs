import sqlite3
from datetime import datetime

# Constants
DB_FILE = 'chat_agent.db'

def init_db():
    """Initialize the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            group_id TEXT NOT NULL,
            message TEXT,
            image BLOB,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_message(sender, receiver, group_id, message=None, image=None):
    """Add a message to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (sender, receiver, group_id, message, image, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (sender, receiver, group_id, message, image, datetime.now()))
    conn.commit()
    conn.close()

def get_messages(group_id):
    """Retrieve messages from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sender, message, image, timestamp FROM messages
        WHERE group_id = ?
        ORDER BY timestamp
    ''', (group_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages