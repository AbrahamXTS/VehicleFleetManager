from datetime import date, datetime
from decimal import Decimal


class LocationModel:
    def __init__(self, latitude: Decimal, longitude: Decimal) -> None:
        self.latitude = latitude
        self.longitude = longitude
        
class Driver:
    def __init__(self, first_name: str, last_name: str, curp: str, license_number: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.curp = curp
        self.license_number = license_number
        
class Vehicle:
    def __init__(self, brand: str, model: str, vin: str, plate: str) -> None:
        self.brand = brand
        self.model = model
        self.vin = vin
        self.plate = plate


class DriverAssignmentModel:
    def __init__(
        self,
        driver_id: int,
        vehicle_id: int,
        travel_date: date,
        route_name: str,
        origin_location: LocationModel,
        destination_location: LocationModel,
        creation_date: datetime | None = None,
        completed_successfully: bool = False,
        problem_description: str | None = None,
        comments: str | None = None,
        active: bool = True,
        driver: Driver | None = None,
        vehicle: Vehicle | None = None
    ) -> None:
        self.driver_id = driver_id
        self.vehicle_id = vehicle_id
        self.travel_date = travel_date
        self.route_name = route_name
        self.origin_location = origin_location
        self.destination_location = destination_location
        self.creation_date = creation_date
        self.completed_successfully = completed_successfully
        self.problem_description = problem_description
        self.comments = comments
        self.active = active
        self.driver = driver
        self.vehicle = vehicle


class DriverAssignmentIdModel:
    def __init__(
        self,
        driver_id: int,
        vehicle_id: int,
        travel_date: date
    ) -> None:
        self.driver_id = driver_id
        self.vehicle_id = vehicle_id
        self.travel_date = travel_date
