from fastapi import APIRouter, HTTPException, status, Depends
from datetime import date

from app.application.services.driver_assignment_service import DriverAssignmentService
from app.domain.exceptions.conflict_with_existing_resource_exception import ConflictWithExistingResourceException
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.infrastructure.dto.driver_assignment_dto import DriverAssignmentRequestDTO
from app.infrastructure.mappers.driver_assignment_mappers import map_driver_assignment_dto_to_driver_assignment_model, \
    map_driver_assignment_model_to_driver_assignment_dto
from app.infrastructure.middlewares.protect_route_middleware import protect_route_middlware
from app.infrastructure.repositories.relational_database_driver_assignment_repository_impl import \
    RelationalDatabaseDriverAssignmentRepositoryImpl

driver_assignment_router = APIRouter(dependencies=[Depends(protect_route_middlware)])
driver_assignment_service = DriverAssignmentService(
    driver_assignment_repository=RelationalDatabaseDriverAssignmentRepositoryImpl()
)


@driver_assignment_router.post("", status_code=status.HTTP_201_CREATED)
def assign_driver(
        driver_assignment_request: DriverAssignmentRequestDTO
):
    try:
        driver_assignment = driver_assignment_service.assign_driver_to_vehicle(
            map_driver_assignment_dto_to_driver_assignment_model(driver_assignment_request)
        )
        return map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)
    except ConflictWithExistingResourceException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@driver_assignment_router.get("")
def get_driver_assignments():
    return [
        map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)
        for driver_assignment in driver_assignment_service.get_driver_assignments()
    ]


@driver_assignment_router.get("/active")
def get_active_driver_assignments():
    return [
        map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)
        for driver_assignment in driver_assignment_service.get_driver_assignments(only_actives=True)
    ]


@driver_assignment_router.get("/{driver_id}/{vehicle_id}/{travel_date}")
def get_driver_assignment(driver_id: int, vehicle_id: int, travel_date: date):
    try:
        driver_assignment = driver_assignment_service.get_driver_assignment(driver_id, vehicle_id, travel_date)
        return map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
