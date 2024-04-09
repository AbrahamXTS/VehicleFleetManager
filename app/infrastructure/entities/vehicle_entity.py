from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.infrastructure.entities.driver_assignment_entity import DriverAssignment


class Vehicle(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    brand: str
    model: str
    vin: str = Field(unique=True)
    plate: str = Field(unique=True)
    purchase_date: datetime
    cost: float
    picture: str
    entry_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    assignment: Optional["DriverAssignment"] = Relationship(back_populates="vehicle")
