from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class VehicleRequestDTO(BaseModel):
    brand: str
    model: str 
    vin: str
    plate: str
    purchase_date: str | datetime
    cost: float
    picture: str

    @validator('purchase_date', pre=True, always=True)
    def parse_purchase_date(cls, value):
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            raise ValueError('Invalid datetime format for purchase_date')