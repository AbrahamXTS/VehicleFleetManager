from datetime import date
from app.application.repositories.driver_assingment_repository import DriverAssignmentRepository
from app.domain.exceptions.conflict_with_existing_resource_exception import ConflictWithExistingResourceException
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

