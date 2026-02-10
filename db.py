import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.getenv("TRACK_DB_PATH", "email_tracking.db")

def ensure_tables():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            email TEXT,
            domain TEXT,
            scenario INTEGER,
            sent_ts_utc TEXT
        )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_email ON messages(email)")
        conn.commit()

def record_message(message_id: str, email: str, domain: str, scenario: int):
    ensure_tables()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO messages (message_id, email, domain, scenario, sent_ts_utc) VALUES (?,?,?,?,?)",
            (message_id, email, domain, scenario, datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
