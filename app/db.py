"""Tiny SQLite data-access layer for the demo API."""
import sqlite3

_DB_PATH = "shop.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def run_query(sql: str) -> list[sqlite3.Row]:
    """Execute a raw SQL string and return all rows.

    Callers build the SQL themselves and pass it here as a single string, so no
    parameter binding happens at this layer.
    """
    conn = get_connection()
    try:
        cursor = conn.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()
