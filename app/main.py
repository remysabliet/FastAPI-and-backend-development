from typing import Any
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference


import random

app = FastAPI()

shipments = {12701: {"weight": 0.6, "content": "House", "status": "delivered"}}

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

# add five testable shipments with fixed unique IDs; contents/status are random
for sid in (12702, 12703, 12704, 12705, 12706):
    shipments[sid] = {
        "weight": round(random.uniform(0.1, 15.0), 2),
        "content": random.choice(_contents),
        "status": random.choice(_statuses),
    }


@app.get("/shipment/latest")
def get_latest_shipment():
    id = max(shipments.keys())
    return shipments[id]


# /shipment/12701
@app.get("/shipment", status_code=status.HTTP_200_OK)
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist")
    return shipments[id]


@app.post("/shipment")
def post_shipment(weight: float, data: dict[str, str]) -> dict[str, int]:
    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="maximum weight limit is 25 kgs.",
        )
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        "content": data["content"],
        "weight": weight,
        "status": "placed",
    }

    return {"id": new_id}


@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> Any:
    return shipments[id][field]


# We use PUT when we want to update all the fields
@app.put("/shipment")
def shipment_update(
    id: int, content: str, weight: float, status: str
) -> dict[str, Any]:
    shipments[id] = {"content": content, "weight": weight, "status": status}
    return shipments[id]


# Want to update a subset of field
# Scalar is buggy with Patch method. Getting always WARNING:  Invalid HTTP request received.
@app.patch("/shipment")
def shipment_patch(id: int, body: dict[str, Any]) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist")

    shipment = shipments[id]
    shipment.update(body)
    shipments[id] = shipment
    return shipment


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipment = shipments.pop(id)
    return shipment

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
