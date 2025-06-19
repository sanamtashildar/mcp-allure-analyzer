
import os
import sqlite3

db_path = os.getenv("DB_PATH", "failures.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS failures (
    id INTEGER PRIMARY KEY,
    name TEXT,
    message TEXT,
    reason TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

def save_failure(name, message, reason):
    cursor.execute("INSERT INTO failures (name, message, reason) VALUES (?, ?, ?)", (name, message, reason))
    conn.commit()

def fetch_failures():
    cursor.execute("SELECT name, message, reason, timestamp FROM failures ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    return [{"name": r[0], "message": r[1], "reason": r[2], "timestamp": r[3]} for r in rows]
