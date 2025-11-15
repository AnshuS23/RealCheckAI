import sqlite3
from datetime import datetime

DB_NAME = "realcheck.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            input_text TEXT,
            filename TEXT,
            verdict TEXT,
            explanation TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

def insert_analysis(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO analyses (type, input_text, filename, verdict, explanation, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data.get('type'),
        data.get('input_text'),
        data.get('filename'),
        data.get('verdict'),
        data.get('explanation'),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def fetch_all_analyses():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM analyses ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]
