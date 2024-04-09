from datetime import date, datetime, timezone
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.infrastructure.entities.driver_assignment_entity import DriverAssignment


class Driver(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    birth_date: date
    curp: str = Field(unique=True)
    address: str
    monthly_salary: float
    license_number: str = Field(unique=True)
    entry_date: date = Field(default_factory=lambda: datetime.now(timezone.utc))
    assignment: Optional["DriverAssignment"] = Relationship(back_populates="driver")
