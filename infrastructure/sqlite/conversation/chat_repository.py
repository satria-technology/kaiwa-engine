import sqlite3
from domain.conversation.model import Message
from domain.conversation.repository import ChatRepository

class SQLiteChatRepository(ChatRepository):
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    receiver TEXT NOT NULL,
                    message TEXT NOT NULL,
                    sent_at TEXT NOT NULL
                )
            ''')

    def save_outgoing_message(self, message: Message):
        with self.connection:
            self.connection.execute('''
                INSERT INTO messages (sender, receiver, message, sent_at)
                VALUES (?, ?, ?, ?)
            ''', (message.sender, message.receiver, message.message, message.sent_at.isoformat()))

    def save_incoming_message(self, message: Message):
        self.save_outgoing_message(message)

    def retrieve_last_messages(self, limit: int) -> list[Message]:
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT sender, receiver, message, sent_at
            FROM messages
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        return [Message(sender=row[0], receiver=row[1], message=row[2], sent_at=datetime.fromisoformat(row[3])) for row in rows]