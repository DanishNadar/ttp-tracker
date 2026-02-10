import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, request, redirect, send_file, abort
from io import BytesIO

DB_PATH = os.getenv("TRACK_DB_PATH", "email_tracking.db")
SECRET = os.getenv("TRACKER_SECRET", "")

app = Flask(__name__)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT NOT NULL,
            event_type TEXT NOT NULL,   -- 'open' or 'click'
            ts_utc TEXT NOT NULL,
            ip TEXT,
            user_agent TEXT,
            referrer TEXT,
            target_url TEXT
        )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_message ON events(message_id)")
        conn.commit()

@app.before_first_request
def _startup():
    init_db()

def _auth_ok():
    if not SECRET:
        return True
    return request.args.get("k", "") == SECRET

def log_event(message_id: str, event_type: str, target_url: str | None = None):
    ts = datetime.now(timezone.utc).isoformat()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent")
    ref = request.headers.get("Referer")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO events (message_id, event_type, ts_utc, ip, user_agent, referrer, target_url) VALUES (?,?,?,?,?,?,?)",
            (message_id, event_type, ts, ip, ua, ref, target_url)
        )
        conn.commit()

@app.get("/pixel/<message_id>.png")
def pixel(message_id):
    if not _auth_ok():
        abort(403)
    if not message_id or len(message_id) > 120:
        abort(400)
    log_event(message_id, "open")

    pixel_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc`\x00\x00"
        b"\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return send_file(BytesIO(pixel_bytes), mimetype="image/png")

@app.get("/l/<message_id>")
def link(message_id):
    if not _auth_ok():
        abort(403)
    target = request.args.get("u", "")
    if not (target.startswith("http://") or target.startswith("https://")):
        abort(400)
    log_event(message_id, "click", target_url=target)
    return redirect(target, code=302)

@app.get("/health")
def health():
    return {"ok": True}

if __name__ == "__main__":
    port = int(os.getenv("TRACKER_PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
