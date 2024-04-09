from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime


class LocationDTO(BaseModel):
    latitude: Decimal
    longitude: Decimal


class RouteFieldsDTO(BaseModel):
    route_name: str
    origin_location: LocationDTO
    destination_location: LocationDTO
    completed_successfully: bool = False
    problem_description: str | None = None
    comments: str | None = None


class DriverAssignmentRequestDTO(RouteFieldsDTO):
    driver_id: int
    vehicle_id: int
    travel_date: date


class DriverAssignmentResponseDTO(DriverAssignmentRequestDTO):
    creation_date: datetime
    active: bool

