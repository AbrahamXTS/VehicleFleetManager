from datetime import date
from app.application.repositories.driver_assingment_repository import DriverAssignmentRepository
from app.domain.exceptions.conflict_with_existing_resource_exception import ConflictWithExistingResourceException
from app.domain.exceptions.invalid_argument_exception import InvalidArgumentException
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.domain.models.driver_assignment import DriverAssignmentModel, DriverAssignmentIdModel, LocationModel


class DriverAssignmentService:
    def __init__(self, driver_assignment_repository: DriverAssignmentRepository) -> None:
        self.driver_assignment_repository = driver_assignment_repository

    def is_driver_assignment_location_taken_at_date(
            self, location: LocationModel, travel_date: date,
            exclude_assignment: DriverAssignmentIdModel | None = None
    ) -> bool:
        assignment = self.driver_assignment_repository.get_active_driver_assignment_by_destination_location_at_date(
            location, travel_date, exclude_assignment
        )
        return assignment is not None
    
    def is_driver_assignment_editable(self, driver_assignment: DriverAssignmentModel) -> bool:
        today = date.today()
        if driver_assignment.travel_date > today:
            return True
        else:
            return driver_assignment.completed_successfully

    def assign_driver_to_vehicle(self, driver_assignment: DriverAssignmentModel) -> DriverAssignmentModel:
        if self.driver_assignment_repository.get_active_driver_assignments_with_driver_id_or_vehicle_id_at_date(
                driver_assignment.driver_id, driver_assignment.vehicle_id, driver_assignment.travel_date
        ):
            raise ConflictWithExistingResourceException(
                "Driver assignment vehicle is already taken by another driver assignment at the same day"
            )
        if self.is_driver_assignment_location_taken_at_date(
                driver_assignment.destination_location, driver_assignment.travel_date
        ):
            raise ConflictWithExistingResourceException(
                "Driver assignment route is already taken by another driver assignment at the same day"
            )
        return self.driver_assignment_repository.assign_driver_to_vehicle(driver_assignment)

    def get_driver_assignments(self, only_actives: bool = False) -> list[DriverAssignmentModel]:
        return self.driver_assignment_repository.get_driver_assignments(only_actives)

    def get_driver_assignment(self, driver_id: int, vehicle_id: int, travel_date: date) -> DriverAssignmentModel:
        driver_assignment = self.driver_assignment_repository.get_driver_assignment(driver_id, vehicle_id, travel_date)
        if not driver_assignment:
            raise ResourceNotFoundException("Driver assignment not found")
        return driver_assignment

    def update_driver_assignment(self, driver_assignment: DriverAssignmentModel) -> DriverAssignmentModel:
        if assignment := self.get_driver_assignment(
                driver_assignment.driver_id, driver_assignment.vehicle_id, driver_assignment.travel_date
        ):
            if not self.is_driver_assignment_editable(assignment):
                raise InvalidArgumentException(
                    "Driver assignment is not editable"
                )
            if self.is_driver_assignment_location_taken_at_date(
                    driver_assignment.destination_location, driver_assignment.travel_date,
                    DriverAssignmentIdModel(
                        driver_assignment.driver_id, driver_assignment.vehicle_id, driver_assignment.travel_date
                    )
            ):
                raise ConflictWithExistingResourceException(
                    "Driver assignment route is already taken by another driver assignment at the same day"
                )
            return self.driver_assignment_repository.update_driver_assignment(driver_assignment)