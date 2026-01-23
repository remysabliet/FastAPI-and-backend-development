"""Repository for shipment database operations."""

from typing import Optional
from app.db.database import get_db


class ShipmentRepository:
    """Repository pattern for shipment data access layer."""

    def __init__(self, db_connection=None):
        """Initialize repository with optional database connection.

        Args:
            db_connection: Optional database connection for dependency injection
        """
        self.db_connection = db_connection

    def _get_connection(self):
        """Get database connection (injected or default)."""
        return self.db_connection if self.db_connection else get_db()

    def find_by_id(self, shipment_id: int) -> Optional[dict]:
        """Fetch a shipment by its ID.

        Args:
            shipment_id: The ID of the shipment to fetch

        Returns:
            Dictionary containing shipment data, or None if not found
        """
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM shipments WHERE id = ?", (shipment_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def find_all(self) -> list[dict]:
        """Fetch all shipments from the database.

        Returns:
            List of dictionaries containing shipment data
        """
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM shipments")
            return [dict(row) for row in cur.fetchall()]

    def find_latest(self) -> Optional[dict]:
        """Fetch the most recently created shipment.

        Returns:
            Dictionary containing shipment data, or None if no shipments exist
        """
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM shipments ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            return dict(row) if row else None

    def insert(self, content: str, weight: float, status: str, destination: int) -> int:
        """Insert a new shipment into the database.

        Args:
            content: Content description of the shipment
            weight: Weight in kilograms
            status: Current status of the shipment
            destination: Destination code

        Returns:
            The ID of the newly inserted shipment

        Raises:
            ValueError: If the insert operation fails
        """
        with self._get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO shipments (content, weight, status, destination) VALUES (?, ?, ?, ?)",
                (content, weight, status, destination),
            )
            last_id = cur.lastrowid
            if last_id is None:
                raise ValueError("Failed to insert shipment")
            return last_id

    def update_by_id(
        self,
        shipment_id: int,
        content: str,
        weight: float,
        status: str,
        destination: int,
    ) -> None:
        """Update a shipment by its ID (full update).

        Args:
            shipment_id: The ID of the shipment to update
            content: New content description
            weight: New weight
            status: New status
            destination: New destination code
        """
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE shipments SET content = ?, weight = ?, status = ?, destination = ? WHERE id = ?",
                (content, weight, status, destination, shipment_id),
            )

    def patch_by_id(self, shipment_id: int, update_data: dict) -> None:
        """Partially update a shipment by its ID.

        Args:
            shipment_id: The ID of the shipment to update
            update_data: Dictionary containing fields to update
        """
        if not update_data:
            return

        fields = ", ".join(f"{key} = ?" for key in update_data.keys())
        values = list(update_data.values()) + [shipment_id]

        with self._get_connection() as conn:
            conn.execute(
                f"UPDATE shipments SET {fields} WHERE id = ?",
                values,
            )

    def delete_by_id(self, shipment_id: int) -> None:
        """Delete a shipment by its ID.

        Args:
            shipment_id: The ID of the shipment to delete
        """
        with self._get_connection() as conn:
            conn.execute("DELETE FROM shipments WHERE id = ?", (shipment_id,))

    def exists(self, shipment_id: int) -> bool:
        """Check if a shipment exists.

        Args:
            shipment_id: The ID of the shipment to check

        Returns:
            True if the shipment exists, False otherwise
        """
        with self._get_connection() as conn:
            cur = conn.execute(
                "SELECT 1 FROM shipments WHERE id = ? LIMIT 1", (shipment_id,)
            )
            return cur.fetchone() is not None
