"""Database connection and utilities."""

import sqlite3
from contextlib import contextmanager
from typing import Optional
from app.core.config import settings


@contextmanager
def get_db():
    """Get database connection with automatic cleanup."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def dict_from_row(row: Optional[sqlite3.Row]) -> Optional[dict]:
    """Convert sqlite3.Row to dictionary.

    Args:
        row: A sqlite3.Row object or None

    Returns:
        Dictionary representation of the row, or None if row is None
    """
    return dict(row) if row else None
