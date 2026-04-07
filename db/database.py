"""
SQLite database for structured data storage.
Tables: tasks, schedules, notes
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "clintask.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            assigned_to TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            due_date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            start_time TEXT NOT NULL,
            end_time TEXT,
            location TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# --- Task CRUD ---
def create_task(title, description="", priority="medium", assigned_to="", due_date=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title,description,priority,assigned_to,due_date) VALUES (?,?,?,?,?)",
                (title, description, priority, assigned_to, due_date))
    conn.commit()
    tid = cur.lastrowid
    conn.close()
    return {"id": tid, "title": title, "status": "pending", "priority": priority}


def list_tasks(status=""):
    conn = get_connection()
    cur = conn.cursor()
    if status:
        cur.execute("SELECT * FROM tasks WHERE status=? ORDER BY created_at DESC", (status,))
    else:
        cur.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def update_task_status(task_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status=? WHERE id=?", (status, int(task_id)))
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return {"id": task_id, "new_status": status} if affected else {"error": f"Task {task_id} not found"}


def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (int(task_id),))
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return {"deleted": True} if affected else {"error": f"Task {task_id} not found"}


# --- Schedule CRUD ---
def create_schedule(title, start_time, end_time="", description="", location=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO schedules (title,start_time,end_time,description,location) VALUES (?,?,?,?,?)",
                (title, start_time, end_time, description, location))
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return {"id": sid, "title": title, "start_time": start_time}


def list_schedules():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM schedules ORDER BY start_time ASC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def delete_schedule(schedule_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM schedules WHERE id=?", (int(schedule_id),))
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return {"deleted": True} if affected else {"error": f"Schedule {schedule_id} not found"}


# --- Notes CRUD ---
def create_note(title, content, tags=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (title,content,tags) VALUES (?,?,?)", (title, content, tags))
    conn.commit()
    nid = cur.lastrowid
    conn.close()
    return {"id": nid, "title": title}


def list_notes(tag=""):
    conn = get_connection()
    cur = conn.cursor()
    if tag:
        cur.execute("SELECT * FROM notes WHERE tags LIKE ? ORDER BY created_at DESC", (f"%{tag}%",))
    else:
        cur.execute("SELECT * FROM notes ORDER BY created_at DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_note(note_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE id=?", (int(note_id),))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else {"error": f"Note {note_id} not found"}


def delete_note(note_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id=?", (int(note_id),))
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return {"deleted": True} if affected else {"error": f"Note {note_id} not found"}


init_db()
