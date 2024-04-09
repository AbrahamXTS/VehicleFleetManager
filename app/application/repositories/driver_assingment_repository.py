from app.domain.models.driver_assignment import DriverAssignmentModel, LocationModel, DriverAssignmentIdModel
from datetime import date


class DriverAssignmentRepository:
    def assign_driver_to_vehicle(self, driver_assignment: DriverAssignmentModel) -> DriverAssignmentModel:
        raise NotImplementedError(
            "Method assign_driver_to_vehicle hasn't been implemented yet."
        )

    def get_driver_assignments(self, only_actives: bool) -> list[DriverAssignmentModel]:
        raise NotImplementedError(
            "Method get_driver_assignments hasn't been implemented yet."
        )

    def get_active_driver_assignments_with_driver_id_or_vehicle_id_at_date(
            self, driver_id: int, vehicle_id: int, travel_date: date
    ) -> list[DriverAssignmentModel]:
        raise NotImplementedError(
            "Method get_driver_assignments_with_driver_id_or_vehicle_id_at_date hasn't been implemented yet."
        )

    def get_driver_assignment(self, driver_id: int, vehicle_id: int, travel_date: date) -> DriverAssignmentModel:
        raise NotImplementedError(
            "Method get_driver_assignment hasn't been implemented yet."
        )

    def get_active_driver_assignment_by_destination_location_at_date(
            self, location: LocationModel, travel_date: date, exclude_assignment: DriverAssignmentIdModel
    ) -> DriverAssignmentModel:
        raise NotImplementedError(
            "Method get_driver_assignment_by_destination_location_at_date hasn't been implemented yet."
        )
    
    def update_driver_assignment(self, driver_assignment: DriverAssignmentModel) -> DriverAssignmentModel:
        raise NotImplementedError(
            "Method update_driver_assignment hasn't been implemented yet."
        )
    
    def set_driver_assignment_as_inactive(self, driver_id: int, vehicle_id: int, travel_date: date) -> None:
        raise NotImplementedError(
            "Method delete_driver_assignment hasn't been implemented yet."
        )
