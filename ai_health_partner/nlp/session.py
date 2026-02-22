import sqlite3
import json

# This will create a local file named 'wellsync.db' in the project folder
DB_FILE = "wellsync.db"


def get_db_connection():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def init_db():
    """Initializes the database tables if they don't exist yet."""
    with get_db_connection() as conn:
        # Table for active chat sessions
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                user_id TEXT PRIMARY KEY,
                step INTEGER,
                data TEXT
            )
        """)
        # Table for the 7-day patient history
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patient_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                report TEXT
            )
        """)
        conn.commit()


# To run this once when the module loads to ensure tables exist
init_db()


def get_state(user_id: str) -> dict:
    with get_db_connection() as conn:
        row = conn.execute("SELECT step, data FROM sessions WHERE user_id = ?", (user_id,)).fetchone()

        if row:
            # To convert the stored JSON text back into a Python dictionary
            return {"step": row["step"], "data": json.loads(row["data"])}
        else:
            return {"step": 0, "data": {}}


def update_state(user_id: str, step: int, key: str = None, value=None):
    # To fetch current state to modify it
    state = get_state(user_id)
    state["step"] = step

    if key is not None:
        state["data"][key] = value

    with get_db_connection() as conn:
        # To insert new user state, or update if the user_id already exists
        conn.execute("""
            INSERT INTO sessions (user_id, step, data) 
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET 
            step=excluded.step, data=excluded.data
        """, (user_id, step, json.dumps(state["data"])))
        conn.commit()


def save_daily_report(user_id: str, report: dict):
    with get_db_connection() as conn:
        # To insert the new daily report
        conn.execute("INSERT INTO patient_history (user_id, report) VALUES (?, ?)",
                     (user_id, json.dumps(report)))

        # To keep only the last 7 reports by deleting anything older
        conn.execute("""
            DELETE FROM patient_history 
            WHERE user_id = ? AND id NOT IN (
                SELECT id FROM patient_history 
                WHERE user_id = ? 
                ORDER BY id DESC LIMIT 7
            )
        """, (user_id, user_id))
        conn.commit()


def get_history(user_id: str) -> list:
    with get_db_connection() as conn:
        rows = conn.execute("SELECT report FROM patient_history WHERE user_id = ? ORDER BY id ASC",
                            (user_id,)).fetchall()

        # To convert all stored JSON text rows back into a list of dictionaries
        return [json.loads(row["report"]) for row in rows]