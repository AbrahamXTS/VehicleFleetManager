from app.application.repositories.driver_assingment_repository import (
    DriverAssignmentRepository,
)
from app.application.repositories.driver_repository import DriverRepository
from app.application.repositories.user_repository import UserRepository
from app.application.repositories.vehicle_repository import VehicleRepository
import logging


class MetricsService:
    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        user_repository: UserRepository,
        driver_repository: DriverRepository,
        driver_assignment_repository: DriverAssignmentRepository,
    ) -> None:
        self.vehicle_repository = vehicle_repository
        self.user_repository = user_repository
        self.driver_repository = driver_repository
        self.driver_assignment_repository = driver_assignment_repository
        self.logger = logging.getLogger(__name__)

    def get_metrics(self):
        self.logger.info("Method get_metrics(), Getting metrics information")
        return {
            "number_of_vehicles": self.vehicle_repository.get_number_of_vehicles(),
            "number_of_users": self.user_repository.get_number_of_users(),
            "number_of_drivers": self.driver_repository.get_number_of_drivers(),
            "number_of_today_assigment": self.driver_assignment_repository.get_number_of_today_assignments(),
        }
