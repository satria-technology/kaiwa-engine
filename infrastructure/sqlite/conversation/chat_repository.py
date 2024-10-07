from contextlib import contextmanager
from datetime import datetime
from functools import lru_cache
import sqlite3

import structlog
from domain.conversation.model import Message, Participant
from domain.conversation.repository import ChatRepository, ParticipantNotFoundError

log = structlog.get_logger()


@contextmanager
def db_transaction(connection):
    try:
        with connection as conn:
            yield conn
    except sqlite3.IntegrityError as e:
        log.error(f"Integrity error", error=str(e), exc_info=True)
        raise
    except sqlite3.Error as e:
        log.error(f"Database error", error=str(e), exc_info=True)
        raise
    except Exception as e:
        log.error(f"Unexpected error", error=str(e), exc_info=True)
        raise


class SQLiteChatRepository(ChatRepository):
    def __init__(self, db_file: str):
        self.connection = sqlite3.connect(db_file)
        self.__create_tables()

    def __create_tables(self):
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS participants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT
                    , external_id VARCHAR(20) NOT NULL
                    , name VARCHAR(255) NOT NULL
                    , channel VARCHAR(50) NOT NULL
                );
            """
            )

            self.connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_participants_external_id
                ON participants (external_id);
            """
            )

            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT
                    , sender_id INTEGER
                    , receiver_id INTEGER
                    , message TEXT NOT NULL
                    , sent_at TEXT NOT NULL
                    , FOREIGN KEY(sender_id) REFERENCES participants(id)
                    , FOREIGN KEY(receiver_id) REFERENCES participants(id)
                );
            """
            )

    def save_messages(self, messages: list[Message]):
        with db_transaction(self.connection) as conn:
            cursor = conn.cursor()
            cursor.executemany(
                """
                INSERT INTO messages (sender_id, receiver_id, message, sent_at)
                VALUES (?, ?, ?, ?)
            """,
                [
                    (
                        msg.sender.id,
                        msg.receiver.id,
                        msg.message,
                        msg.sent_at.isoformat(),
                    )
                    for msg in messages
                ],
            )
            conn.commit()

    def create_participant(self, participant: Participant):
        with db_transaction(self.connection) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO participants (external_id, name, channel)
                VALUES (?, ?, ?)
            """,
                (participant.external_id, participant.name, participant.channel),
            )
            conn.commit()
            participant.id = cursor.lastrowid
            return participant
    
    def get_number_of_participants(self) -> int:
        with db_transaction(self.connection) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM participants
            """
            )
            return int(cursor.fetchone()[0])

    def get_participant_by_external_id(self, external_id: str, channel: str) -> Participant:
        with db_transaction(self.connection) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, external_id, name, channel
                FROM participants
                WHERE external_id = ? AND channel = ?
            """,
                (external_id, channel),
            )
            row = cursor.fetchone()
            if row:
                return Participant(
                    id=row[0], external_id=row[1], name=row[2], channel=row[3]
                )
            raise ParticipantNotFoundError
    
    @lru_cache(maxsize=128)
    def __get_participant_by_id(self, id: int) -> Participant:
        with db_transaction(self.connection) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, external_id, name, channel
                FROM participants
                WHERE id = ?
            """,
                (id,),
            )
            row = cursor.fetchone()
            if row:
                return Participant(
                    id=row[0], external_id=row[1], name=row[2], channel=row[3]
                )
            raise ParticipantNotFoundError

    def get_last_messages_to_participant(
        self, participant: Participant, n: int, datetime: datetime
    ) -> list[Message]:
        with db_transaction(self.connection) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, sender_id, receiver_id, message, sent_at
                FROM messages
                WHERE receiver_id = ? OR sender_id = ? AND sent_at <= ?
                ORDER BY sent_at DESC
                LIMIT ?
            """,
                (participant.id, participant.id, datetime.isoformat(), n),
            )
            rows = cursor.fetchall()
            return [
                Message(
                    id=row[0],
                    sender=self.__get_participant_by_id(row[1]),
                    receiver=self.__get_participant_by_id(row[2]),
                    message=row[3],
                    sent_at=datetime.fromisoformat(row[4]),
                )
                for row in rows
            ]
