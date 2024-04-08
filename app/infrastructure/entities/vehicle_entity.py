from sqlmodel import Field, SQLModel
from datetime import datetime, timezone

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