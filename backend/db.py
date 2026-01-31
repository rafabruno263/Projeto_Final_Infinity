import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "wayne.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('employee','manager','security_admin'))
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL CHECK(tipo IN ('equipment','vehicle','security_device')),
        nome TEXT NOT NULL,
        descricao TEXT,
        status TEXT NOT NULL,
        atualizado_em TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        acao TEXT NOT NULL,
        entidade TEXT NOT NULL,
        entidade_id INTEGER,
        data_hora TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

def now_iso():
    return datetime.utcnow().isoformat(timespec="seconds")

def log_activity(user_id: int, acao: str, entidade: str, entidade_id: int | None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO activity_logs (user_id, acao, entidade, entidade_id, data_hora) VALUES (?,?,?,?,?)",
        (user_id, acao, entidade, entidade_id, now_iso())
    )
    conn.commit()
    conn.close()