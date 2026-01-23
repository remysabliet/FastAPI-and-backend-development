"""Shipment API endpoints."""

from fastapi import APIRouter, Path

from app.schemas.shipment import (
    Shipment,
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentPatch,
    ShipmentStatus,
)
from app.services.shipment_service import ShipmentService

router = APIRouter()

# Instantiate service (could also use FastAPI Depends for DI)
shipment_service = ShipmentService()


@router.get(
    "/latest",
    response_model=Shipment,
    summary="Get latest shipment",
    description="Retrieve the most recently created shipment",
)
def get_latest_shipment() -> Shipment:
    """Get the most recently created shipment."""
    return shipment_service.get_latest_shipment()


@router.get(
    "/{shipment_id}",
    response_model=Shipment,
    summary="Get shipment by ID",
    description="Retrieve a specific shipment by its ID",
)
def get_shipment_by_id(
    shipment_id: int = Path(
        ..., description="The ID of the shipment to retrieve", gt=0
    ),
) -> Shipment:
    """Get a shipment by ID."""
    return shipment_service.get_shipment(shipment_id)


@router.get(
    "",
    response_model=dict[int, Shipment],
    summary="List all shipments",
    description="Retrieve a list of all shipments",
)
def list_shipments() -> dict[int, Shipment]:
    """List all shipments."""
    return shipment_service.list_all_shipments()


@router.get(
    "/{shipment_id}/fields/{field_name}",
    summary="Get shipment field",
    description="Retrieve a specific field value from a shipment",
)
def get_shipment_field(
    shipment_id: int = Path(..., description="The ID of the shipment", gt=0),
    field_name: str = Path(..., description="The name of the field to retrieve"),
) -> str | float | int | ShipmentStatus:
    """Get a specific field from a shipment."""
    return shipment_service.get_shipment_field(shipment_id, field_name)


@router.post(
    "",
    response_model=Shipment,
    status_code=201,
    summary="Create shipment",
    description="Create a new shipment",
)
def create_shipment(data: ShipmentCreate) -> Shipment:
    """Create a new shipment."""
    return shipment_service.create_shipment(data)


@router.put(
    "/{shipment_id}",
    response_model=Shipment,
    summary="Update shipment",
    description="Update all fields of a shipment (full replacement)",
)
def update_shipment(
    body: ShipmentUpdate,
    shipment_id: int = Path(..., description="The ID of the shipment to update", gt=0),
) -> Shipment:
    """Update all fields of a shipment."""
    return shipment_service.update_shipment(shipment_id, body)


@router.patch(
    "/{shipment_id}",
    response_model=Shipment,
    summary="Partially update shipment",
    description="Update specific fields of a shipment",
)
def patch_shipment(
    body: ShipmentPatch,
    shipment_id: int = Path(..., description="The ID of the shipment to update", gt=0),
) -> Shipment:
    """Partially update a shipment."""
    return shipment_service.patch_shipment(shipment_id, body)


@router.delete(
    "/{shipment_id}",
    status_code=204,
    summary="Delete shipment",
    description="Delete a shipment by its ID",
)
def delete_shipment(
    shipment_id: int = Path(..., description="The ID of the shipment to delete", gt=0),
) -> None:
    """Delete a shipment by ID."""
    shipment_service.delete_shipment(shipment_id)
