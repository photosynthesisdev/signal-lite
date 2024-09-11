import etcd3
import time
import json
from .models import ClientMessageRequest, ServerValidatedMessage

'''
NOTES:

This is just a super barebones wrapper for a SQLite Database. Simply does reads/writes.
'''

class SimpleMessagingDB:
    def __init__(self, db_file, watch_callback):
        self.conn = sqlite3.connect(
            db_file, 
            check_same_thread=False
        )
        self._watch_callback = watch_callback
        self.conn.row_factory = sqlite3.Row
        self.last_message_id = 0
        self._setup_table()
        self._watch_messages()

    # --------- PUBLIC METHODS ------------
    def close_connection(self):
        if self.conn:
            self.conn.close()

    def get_full_conversation_history(self) -> list[ServerValidatedMessage]:
        '''Called on bootup by the client to get the full length of message history.'''
        # Returns full history of conversation.
        ...

    def write_message(self, user: str, message : ClientMessageRequest):
        """Writes a message to the database."""
        with self.conn:
            self.conn.execute('''
                INSERT INTO messages (user, message)
                VALUES (?, ?)
            ''', (user, message))

    # --------- INTERNAL METHODS ---------
    def _setup_table(self):
        """Create the messages table if it doesn't exist."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def _watch_messages(self, interval : float = 1):
        """Polls the database for new messages at a given interval."""
        while True:
            new_messages = self._read_new_messages()
            if new_messages:
                self._watch_callback(new_messages)
            time.sleep(interval)

    def _read_new_messages(self) -> list[ServerValidatedMessage]:
        """Fetches new messages that have been added since the last poll."""
        with self.conn:
            cur = self.conn.execute('''SELECT * FROM messages WHERE id > ? ORDER BY id ASC''', (self.last_message_id,))
            messages = cur.fetchall()
            if messages:
                self.last_message_id = messages[-1]['id']
            return messages
