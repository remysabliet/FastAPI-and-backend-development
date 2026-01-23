"""Business logic for shipment operations."""

from random import randint
from typing import Optional
from fastapi import HTTPException

from app.schemas.shipment import (
    Shipment,
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentPatch,
)
from app.repositories.shipment_repository import ShipmentRepository


class ShipmentService:
    """Service layer for shipment business logic."""

    def __init__(self, repository: Optional[ShipmentRepository] = None):
        """Initialize service with repository.

        Args:
            repository: Optional ShipmentRepository for dependency injection
        """
        self.repository = repository or ShipmentRepository()

    def get_shipment(self, shipment_id: int) -> Shipment:
        """Get a shipment by ID.

        Args:
            shipment_id: The ID of the shipment to retrieve

        Returns:
            Shipment model

        Raises:
            HTTPException: If shipment is not found
        """
        shipment = self.repository.find_by_id(shipment_id)
        if not shipment:
            raise HTTPException(
                status_code=404, detail=f"Shipment with ID {shipment_id} not found"
            )
        return Shipment(**shipment)

    def get_latest_shipment(self) -> Shipment:
        """Get the most recently created shipment.

        Returns:
            Shipment model

        Raises:
            HTTPException: If no shipments exist
        """
        shipment = self.repository.find_latest()
        if not shipment:
            raise HTTPException(status_code=404, detail="No shipments found")
        return Shipment(**shipment)

    def list_all_shipments(self) -> dict[int, Shipment]:
        """List all shipments.

        Returns:
            Dictionary mapping shipment IDs to Shipment models
        """
        shipments = self.repository.find_all()
        return {s["id"]: Shipment(**s) for s in shipments}

    def create_shipment(self, data: ShipmentCreate) -> Shipment:
        """Create a new shipment.

        Args:
            data: ShipmentCreate model with shipment data

        Returns:
            Created Shipment model

        Raises:
            HTTPException: If weight exceeds limit
        """
        # Business logic: validate weight
        if data.weight > 25:
            raise HTTPException(
                status_code=406, detail="Maximum weight limit is 25 kgs."
            )

        # Generate destination if not provided
        destination = (
            data.destination if data.destination is not None else randint(11000, 11999)
        )

        # Insert into database
        new_id = self.repository.insert(
            content=data.content,
            weight=data.weight,
            status=data.status.value,
            destination=destination,
        )

        # Return created shipment
        return self.get_shipment(new_id)

    def update_shipment(self, shipment_id: int, data: ShipmentUpdate) -> Shipment:
        """Fully update a shipment (PUT).

        Args:
            shipment_id: The ID of the shipment to update
            data: ShipmentUpdate model with new data

        Returns:
            Updated Shipment model

        Raises:
            HTTPException: If shipment is not found
        """
        if not self.repository.exists(shipment_id):
            raise HTTPException(
                status_code=404, detail=f"Shipment with ID {shipment_id} not found"
            )

        self.repository.update_by_id(
            shipment_id=shipment_id,
            content=data.content,
            weight=data.weight,
            status=data.status.value,
            destination=data.destination,
        )

        return self.get_shipment(shipment_id)

    def patch_shipment(self, shipment_id: int, data: ShipmentPatch) -> Shipment:
        """Partially update a shipment (PATCH).

        Args:
            shipment_id: The ID of the shipment to update
            data: ShipmentPatch model with fields to update

        Returns:
            Updated Shipment model

        Raises:
            HTTPException: If shipment is not found
        """
        if not self.repository.exists(shipment_id):
            raise HTTPException(
                status_code=404, detail=f"Shipment with ID {shipment_id} not found"
            )

        # Get only the fields that were provided
        update_data = data.model_dump(exclude_unset=True)

        # Convert enum to value if status is being updated
        if "status" in update_data and update_data["status"] is not None:
            update_data["status"] = update_data["status"].value

        if update_data:
            self.repository.patch_by_id(shipment_id, update_data)

        return self.get_shipment(shipment_id)

    def delete_shipment(self, shipment_id: int) -> None:
        """Delete a shipment.

        Args:
            shipment_id: The ID of the shipment to delete

        Raises:
            HTTPException: If shipment is not found
        """
        if not self.repository.exists(shipment_id):
            raise HTTPException(
                status_code=404, detail=f"Shipment with ID {shipment_id} not found"
            )

        self.repository.delete_by_id(shipment_id)

    def get_shipment_field(self, shipment_id: int, field_name: str):
        """Get a specific field from a shipment.

        Args:
            shipment_id: The ID of the shipment
            field_name: The name of the field to retrieve

        Returns:
            The value of the requested field

        Raises:
            HTTPException: If shipment is not found or field doesn't exist
        """
        shipment = self.repository.find_by_id(shipment_id)
        if not shipment:
            raise HTTPException(
                status_code=404, detail=f"Shipment with ID {shipment_id} not found"
            )

        if field_name not in shipment:
            raise HTTPException(
                status_code=400,
                detail=f"Field '{field_name}' does not exist. Valid fields: {', '.join(shipment.keys())}",
            )

        return shipment[field_name]
