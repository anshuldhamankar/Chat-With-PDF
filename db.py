import sqlite3

DB = "chat_history.db"


def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                question  TEXT NOT NULL,
                answer    TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_query(question: str, answer: str):
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO queries (question, answer) VALUES (?, ?)", (question, answer))


def get_history(limit: int = 20) -> list[dict]:
    with sqlite3.connect(DB) as conn:
        rows = conn.execute(
            "SELECT id, question, answer, timestamp FROM queries ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [{"id": r[0], "question": r[1], "answer": r[2], "timestamp": r[3]} for r in rows]
