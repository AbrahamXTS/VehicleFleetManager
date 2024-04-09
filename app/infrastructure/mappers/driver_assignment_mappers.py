from app.domain.models.driver_assignment import DriverAssignmentModel, LocationModel
from app.infrastructure.dto.driver_assignment_dto import DriverAssignmentRequestDTO, DriverAssignmentResponseDTO, LocationDTO
from app.infrastructure.entities.driver_assignment_entity import DriverAssignment


def map_driver_assignment_dto_to_driver_assignment_model(
    driver_assignment_req_dto: DriverAssignmentRequestDTO,
) -> DriverAssignmentModel:
    return DriverAssignmentModel(
        driver_id=driver_assignment_req_dto.driver_id,
        vehicle_id=driver_assignment_req_dto.vehicle_id,
        travel_date=driver_assignment_req_dto.travel_date,
        route_name=driver_assignment_req_dto.route_name,
        origin_location=LocationModel(
            latitude=driver_assignment_req_dto.origin_location.latitude,
            longitude=driver_assignment_req_dto.origin_location.longitude,
        ),
        destination_location=LocationModel(
            latitude=driver_assignment_req_dto.destination_location.latitude,
            longitude=driver_assignment_req_dto.destination_location.longitude,
        ),
        completed_successfully=driver_assignment_req_dto.completed_successfully,
        problem_description=driver_assignment_req_dto.problem_description,
        comments=driver_assignment_req_dto.comments,
    )


def map_driver_assignment_model_to_driver_assignment_dto(
    driver_assignment: DriverAssignmentModel,
) -> DriverAssignmentResponseDTO:
    return DriverAssignmentResponseDTO(
        creation_date=driver_assignment.creation_date,
        driver_id=driver_assignment.driver_id,
        vehicle_id=driver_assignment.vehicle_id,
        travel_date=driver_assignment.travel_date,
        route_name=driver_assignment.route_name,
        origin_location=LocationDTO(
            latitude=driver_assignment.origin_location.latitude,
            longitude=driver_assignment.origin_location.longitude,
        ),
        destination_location=LocationDTO(
            latitude=driver_assignment.destination_location.latitude,
            longitude=driver_assignment.destination_location.longitude,
        ),
        completed_successfully=driver_assignment.completed_successfully,
        problem_description=driver_assignment.problem_description,
        comments=driver_assignment.comments,
        active=driver_assignment.active,
    )


def map_driver_assignment_model_to_driver_assignment_entity(
    driver_assignment: DriverAssignmentModel,
) -> DriverAssignment:
    return DriverAssignment(
        driver_id=driver_assignment.driver_id,
        vehicle_id=driver_assignment.vehicle_id,
        travel_date=driver_assignment.travel_date,
        route_name=driver_assignment.route_name,
        origin_location_latitude=driver_assignment.origin_location.latitude,
        origin_location_longitude=driver_assignment.origin_location.longitude,
        destination_location_latitude=driver_assignment.destination_location.latitude,
        destination_location_longitude=driver_assignment.destination_location.longitude,
        completed_successfully=driver_assignment.completed_successfully,
        problem_description=driver_assignment.problem_description,
        comments=driver_assignment.comments,
    )


def map_driver_assignment_entity_to_driver_assignment_model(
    driver_assignment_entity: DriverAssignment,
) -> DriverAssignmentModel:
    return DriverAssignmentModel(
        driver_id=driver_assignment_entity.driver_id,
        vehicle_id=driver_assignment_entity.vehicle_id,
        travel_date=driver_assignment_entity.travel_date,
        route_name=driver_assignment_entity.route_name,
        origin_location=LocationModel(
            latitude=driver_assignment_entity.origin_location_latitude,
            longitude=driver_assignment_entity.origin_location_longitude,
        ),
        destination_location=LocationModel(
            latitude=driver_assignment_entity.destination_location_latitude,
            longitude=driver_assignment_entity.destination_location_longitude,
        ),
        creation_date=driver_assignment_entity.creation_date,
        completed_successfully=driver_assignment_entity.completed_successfully,
        problem_description=driver_assignment_entity.problem_description,
        comments=driver_assignment_entity.comments,
        active=driver_assignment_entity.active,
    )
