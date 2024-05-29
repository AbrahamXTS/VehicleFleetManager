from datetime import date, datetime, timezone
from sqlmodel import Field, SQLModel, Relationship
from decimal import Decimal

from app.infrastructure.entities.driver_entity import Driver
from app.infrastructure.entities.vehicle_entity import Vehicle


class DriverAssignment(SQLModel, table=True):
    driver_id: int | None = Field(foreign_key="driver.id", primary_key=True)
    vehicle_id: int | None = Field(foreign_key="vehicle.id", primary_key=True)
    travel_date: date = Field(primary_key=True)
    route_name: str
    origin_location_latitude: Decimal = Field(default=0, max_digits=9, decimal_places=6)
    origin_location_longitude: Decimal = Field(
        default=0, max_digits=9, decimal_places=6
    )
    destination_location_latitude: Decimal = Field(
        default=0, max_digits=9, decimal_places=6
    )
    destination_location_longitude: Decimal = Field(
        default=0, max_digits=9, decimal_places=6
    )
    completed_successfully: bool = Field(default=False)
    problem_description: str | None = None
    comments: str | None = None
    active: bool = Field(default=True)
    creation_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    driver: "Driver" = Relationship(back_populates="assignment")
    vehicle: "Vehicle" = Relationship(back_populates="assignment")
