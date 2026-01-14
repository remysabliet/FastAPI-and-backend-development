from typing import TypedDict
from fastapi import FastAPI, HTTPException, Path, Query
from scalar_fastapi import get_scalar_api_reference
from schemas import Shipment, ShipmentCreate, ShipmentUpdate, ShipmentPatch
from enum import Enum
import random

app = FastAPI(
    title="Shipment API",
    description="API for managing shipments",
    version="1.0.0"
)


class ShipmentDict(TypedDict):
    weight: float
    content: str
    status: str
    destination: int


shipments: dict[int, ShipmentDict] = {
    12701: {
        "weight": 0.6,
        "content": "House",
        "status": "delivered",
        "destination": 11234,
    }
}

_contents = [
    "books",
    "electronics",
    "clothes",
    "furniture",
    "toys",
    "kitchenware",
    "tools",
]
_statuses = ["pending", "in transit", "delivered", "delayed", "returned"]


class ShipmentStatus(Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


# Add five testable shipments with fixed unique IDs; contents/status are random
for sid in (12702, 12703, 12704, 12705, 12706):
    shipments[sid] = {
        "weight": round(random.uniform(0.1, 15.0), 2),
        "content": random.choice(_contents),
        "status": random.choice(_statuses),
        "destination": random.randint(11000, 11999),
    }


@app.get(
    "/shipments/latest",
    response_model=Shipment,
    summary="Get latest shipment",
    description="Retrieve the most recently created shipment"
)
def get_latest_shipment() -> Shipment:
    """Get the most recently created shipment."""
    shipment_id = max(shipments.keys())
    return Shipment(**shipments[shipment_id])


@app.get(
    "/shipments/{shipment_id}",
    response_model=Shipment,
    summary="Get shipment by ID",
    description="Retrieve a specific shipment by its ID"
)
def get_shipment_by_id(
    shipment_id: int = Path(..., description="The ID of the shipment to retrieve", gt=0)
) -> Shipment:
    """Get a shipment by ID."""
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=404,
            detail=f"Shipment with ID {shipment_id} not found"
        )
    return Shipment(**shipments[shipment_id])


@app.get(
    "/shipment",
    response_model=Shipment,
    summary="Get shipment by ID (query param)",
    description="Retrieve a specific shipment by its ID using query parameter"
)
def get_shipment(
    id: int = Query(..., description="The ID of the shipment to retrieve", gt=0)
) -> Shipment:
    """Get a shipment by ID using query parameter."""
    if id not in shipments:
        raise HTTPException(
            status_code=404,
            detail=f"Shipment with ID {id} not found"
        )
    return Shipment(**shipments[id])


@app.get(
    "/shipments",
    response_model=dict[int, Shipment],
    summary="List all shipments",
    description="Retrieve a list of all shipments"
)
def list_shipments() -> dict[int, Shipment]:
    """List all shipments."""
    return {sid: Shipment(**data) for sid, data in shipments.items()}


@app.get(
    "/shipments/{shipment_id}/fields/{field_name}",
    summary="Get shipment field",
    description="Retrieve a specific field value from a shipment"
)
def get_shipment_field(
    shipment_id: int = Path(..., description="The ID of the shipment", gt=0),
    field_name: str = Path(..., description="The name of the field to retrieve")
) -> str | float | int:
    """Get a specific field from a shipment."""
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=404,
            detail=f"Shipment with ID {shipment_id} not found"
        )
    
    shipment = shipments[shipment_id]
    
    # Access fields directly with proper type narrowing
    if field_name == "weight":
        return shipment["weight"]
    elif field_name == "content":
        return shipment["content"]
    elif field_name == "status":
        return shipment["status"]
    elif field_name == "destination":
        return shipment["destination"]
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Field '{field_name}' does not exist. Valid fields: weight, content, status, destination"
        )


@app.post(
    "/shipments",
    response_model=Shipment,
    status_code=201,
    summary="Create shipment",
    description="Create a new shipment"
)
def create_shipment(data: ShipmentCreate) -> Shipment:
    """Create a new shipment."""
    if data.weight > 25:
        raise HTTPException(
            status_code=406,
            detail="Maximum weight limit is 25 kgs."
        )
    new_id = max(shipments.keys()) + 1
    # Generate destination if not provided
    destination = data.destination if data.destination is not None else random.randint(11000, 11999)
    shipments[new_id] = {
        "content": data.content,
        "weight": data.weight,
        "status": data.status,
        "destination": destination,
    }
    return Shipment(**shipments[new_id])


@app.put(
    "/shipments/{shipment_id}",
    response_model=Shipment,
    summary="Update shipment",
    description="Update all fields of a shipment (full replacement)"
)
def update_shipment(
    body: ShipmentUpdate,
    shipment_id: int = Path(..., description="The ID of the shipment to update", gt=0)
) -> Shipment:
    """Update all fields of a shipment."""
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=404,
            detail=f"Shipment with ID {shipment_id} not found"
        )
    shipments[shipment_id] = {
        "content": body.content,
        "weight": body.weight,
        "status": body.status,
        "destination": body.destination,
    }
    return Shipment(**shipments[shipment_id])


@app.patch(
    "/shipments/{shipment_id}",
    response_model=Shipment,
    summary="Partially update shipment",
    description="Update specific fields of a shipment"
)
def patch_shipment(
    body: ShipmentPatch,
    shipment_id: int = Path(..., description="The ID of the shipment to update", gt=0)
) -> Shipment:
    """Partially update a shipment."""
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=404,
            detail=f"Shipment with ID {shipment_id} not found"
        )

    shipment = shipments[shipment_id]
    update_data = body.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        if key in shipment:
            shipment[key] = value  # type: ignore
    
    shipments[shipment_id] = shipment
    return Shipment(**shipments[shipment_id])


@app.delete(
    "/shipments/{shipment_id}",
    status_code=204,
    summary="Delete shipment",
    description="Delete a shipment by its ID"
)
def delete_shipment(
    shipment_id: int = Path(..., description="The ID of the shipment to delete", gt=0)
) -> None:
    """Delete a shipment by ID."""
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=404,
            detail=f"Shipment with ID {shipment_id} not found"
        )
    shipments.pop(shipment_id)


@app.get("/docs/scalar", include_in_schema=False)
def get_scalar_docs():
    """Get Scalar API documentation."""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title
    )