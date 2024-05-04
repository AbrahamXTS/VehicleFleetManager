from app.application.repositories.driver_assingment_repository import DriverAssignmentRepository
from app.application.repositories.driver_repository import DriverRepository
from app.application.repositories.user_repository import UserRepository
from app.application.repositories.vehicle_repository import VehicleRepository


class MetricsService():

    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        user_repository: UserRepository,
        driver_repository: DriverRepository,
        driver_assignment_repository: DriverAssignmentRepository
  
    ) -> None:
        self.vehicle_repository = vehicle_repository
        self.user_repository = user_repository
        self.driver_repository = driver_repository
        self.driver_assignment_repository = driver_assignment_repository
        

    def get_metrics(self): 
        return {
            "number of vehicles": self.vehicle_repository.get_number_of_vehicles(),
            "number of users":self.user_repository.get_number_of_users(),
            "number of drivers":self.driver_repository.get_number_of_drivers(),
            "number of today assigment":self.driver_assignment_repository.get_number_of_today_assignments()
        }