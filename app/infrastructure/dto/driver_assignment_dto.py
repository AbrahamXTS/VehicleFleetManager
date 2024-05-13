from pydantic import BaseModel
from decimal import Decimal
from datetime import date, datetime


class LocationDTO(BaseModel):
    latitude: Decimal
    longitude: Decimal
    
class DriverDTO(BaseModel):
    first_name: str
    last_name: str
    curp: str
    license_number: str
    
class VehicleDTO(BaseModel):
    brand: str
    model: str
    vin: str
    plate: str


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
    driver: DriverDTO
    vehicle: VehicleDTO
