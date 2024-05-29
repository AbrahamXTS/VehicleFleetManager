from datetime import date

from pydantic import BaseModel


class DriverDTO(BaseModel):
    id: int
    name: str
    last_name: str
    birth_date: date
    curp: str
    address: str
    monthly_salary: float
    driving_license: str
    registration_date: date
