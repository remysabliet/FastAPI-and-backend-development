"""Database initialization."""

from app.db.database import get_db


def init_db():
    """Initialize database tables."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS shipments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                weight REAL NOT NULL,
                status TEXT NOT NULL,
                destination INTEGER NOT NULL
            )
        """)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
