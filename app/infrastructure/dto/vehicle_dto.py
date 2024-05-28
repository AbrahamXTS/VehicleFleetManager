from pydantic import BaseModel, validator
from datetime import datetime


class VehicleDTO(BaseModel):
    id: int | None
    brand: str
    model: str
    vin: str
    plate: str
    purchase_date: str | datetime
    cost: float
    picture: str
    entry_date: str | datetime

    @validator("purchase_date", pre=True, always=True)
    def parse_purchase_date(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError("Invalid datetime format for purchase_date")

    @validator("entry_date", pre=True, always=True)
    def parse_entry_date(cls, value):
        if isinstance(value, datetime):
            return value
        print(value)
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError("Invalid datetime format for entry_date")
