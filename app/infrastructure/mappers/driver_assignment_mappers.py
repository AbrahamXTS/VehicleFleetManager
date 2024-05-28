from app.domain.models.driver_assignment import Driver, DriverAssignmentModel, LocationModel, Vehicle
from app.infrastructure.dto.driver_assignment_dto import DriverAssignmentRequestDTO, DriverAssignmentResponseDTO, DriverDTO, LocationDTO, VehicleDTO
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
        driver=DriverDTO(
            first_name=driver_assignment.driver.first_name,
            last_name=driver_assignment.driver.last_name,
            curp=driver_assignment.driver.curp,
            license_number=driver_assignment.driver.license_number,
        ),
        vehicle=VehicleDTO(
            brand=driver_assignment.vehicle.brand,
            model=driver_assignment.vehicle.model,
            vin=driver_assignment.vehicle.vin,
            plate=driver_assignment.vehicle.plate,
        ),
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
        driver=Driver(
            first_name=driver_assignment_entity.driver.first_name,
            last_name=driver_assignment_entity.driver.last_name,
            curp=driver_assignment_entity.driver.curp,
            license_number=driver_assignment_entity.driver.license_number,
        ),
        vehicle=Vehicle(
            brand=driver_assignment_entity.vehicle.brand,
            model=driver_assignment_entity.vehicle.model,
            vin=driver_assignment_entity.vehicle.vin,
            plate=driver_assignment_entity.vehicle.plate,
        ),
    )
