"""
AegisLens - Local SQLite Vector & Action Storage
"""

import sqlite3

class LocalVectorIndex:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA journal_mode = WAL;")
        self._setup_schema()

    def _setup_schema(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS meeting_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    chunk_text TEXT NOT NULL,
                    is_action_item INTEGER DEFAULT 0
                )
            """)

    def add_entry(self, timestamp: str, text: str, is_task: bool = False):
        with self.conn:
            self.conn.execute(
                "INSERT INTO meeting_entries (timestamp, chunk_text, is_action_item) VALUES (?, ?, ?)",
                (timestamp, text, 1 if is_task else 0)
            )

    def query_actions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT timestamp, chunk_text FROM meeting_entries WHERE is_action_item = 1")
        return cursor.fetchall()

if __name__ == "__main__":
    index = LocalVectorIndex()
    index.add_entry("00:15", "Send the revised plan by Friday.", is_task=True)
    print("[Storage] Saved action:", index.query_actions())