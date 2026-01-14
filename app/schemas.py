from random import randint
from pydantic import BaseModel, Field
from typing import Optional


def random_destination():
    """Generate a random destination code."""
    return randint(11000, 11999)


class ShipmentBase(BaseModel):
    """Base model with common shipment fields."""

    content: str = Field(
        ...,
        description="Content of the shipment",
        max_length=100,
        examples=["books", "electronics"],
    )
    weight: float = Field(
        ...,
        description="Weight of the shipment in kg",
        gt=0,
        lt=25,
        examples=[5.5, 12.3],
    )
    status: str = Field(
        ...,
        description="Current status of the shipment",
        examples=["pending", "in transit", "delivered"],
    )


class ShipmentCreate(ShipmentBase):
    """Model for creating a new shipment (POST)."""

    destination: Optional[int] = Field(
        default=None,
        description="Destination code of the shipment",
        ge=11000,
        le=11999,
        examples=[11234, 11567],
    )


class Shipment(ShipmentBase):
    """Model for a complete shipment (response model)."""

    destination: int = Field(
        ..., description="Destination code of the shipment", ge=11000, le=11999
    )


class ShipmentUpdate(ShipmentBase):
    """Model for full shipment update (PUT) - all fields required."""

    destination: int = Field(
        ..., description="Destination code of the shipment", ge=11000, le=11999
    )


class ShipmentPatch(BaseModel):
    """Model for partial shipment update (PATCH) - all fields optional."""

    content: Optional[str] = Field(
        default=None, description="Content of the shipment", max_length=100
    )
    weight: Optional[float] = Field(
        default=None, description="Weight of the shipment in kg", gt=0, lt=25
    )
    status: Optional[str] = Field(
        default=None, description="Current status of the shipment"
    )
    destination: Optional[int] = Field(
        default=None, description="Destination code of the shipment", ge=11000, le=11999
    )
