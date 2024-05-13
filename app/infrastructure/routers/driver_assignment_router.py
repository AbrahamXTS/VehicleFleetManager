from fastapi import APIRouter, HTTPException, status, Depends
from datetime import date

from app.application.services.driver_assignment_service import DriverAssignmentService
from app.domain.exceptions.conflict_with_existing_resource_exception import (
    ConflictWithExistingResourceException,
)
from app.domain.exceptions.invalid_argument_exception import InvalidArgumentException
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.infrastructure.dto.driver_assignment_dto import (
    DriverAssignmentRequestDTO,
    DriverAssignmentResponseDTO,
    RouteFieldsDTO,
)
from app.infrastructure.mappers.driver_assignment_mappers import (
    map_driver_assignment_dto_to_driver_assignment_model,
    map_driver_assignment_model_to_driver_assignment_dto,
)
from app.infrastructure.middlewares.protect_route_middleware import (
    protect_route_middlware,
)
from app.infrastructure.repositories.relational_database_driver_assignment_repository_impl import (
    RelationalDatabaseDriverAssignmentRepositoryImpl,
)

driver_assignment_router = APIRouter(dependencies=[Depends(protect_route_middlware)])
driver_assignment_service = DriverAssignmentService(
    driver_assignment_repository=RelationalDatabaseDriverAssignmentRepositoryImpl()
)


@driver_assignment_router.post("", status_code=status.HTTP_201_CREATED)
def assign_driver(
    driver_assignment_request: DriverAssignmentRequestDTO,
) -> DriverAssignmentResponseDTO:
    try:
        driver_assignment = driver_assignment_service.assign_driver_to_vehicle(
            map_driver_assignment_dto_to_driver_assignment_model(
                driver_assignment_request
            )
        )
        return map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)
    except ConflictWithExistingResourceException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@driver_assignment_router.get("")
def get_driver_assignments(
    travel_date: date | None = None,
) -> list[DriverAssignmentResponseDTO]:
    return [
        map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)
        for driver_assignment in driver_assignment_service.get_driver_assignments(
            travel_date
        )
    ]


@driver_assignment_router.get("/active")
def get_active_driver_assignments(
    travel_date: date | None = None,
) -> list[DriverAssignmentResponseDTO]:
    return [
        map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)
        for driver_assignment in driver_assignment_service.get_driver_assignments(
            only_actives=True, travel_date=travel_date
        )
    ]


@driver_assignment_router.get("/{driver_id}/{vehicle_id}/{travel_date}")
def get_driver_assignment(
    driver_id: int, vehicle_id: int, travel_date: date
) -> DriverAssignmentResponseDTO:
    try:
        driver_assignment = driver_assignment_service.get_driver_assignment(
            driver_id, vehicle_id, travel_date
        )
        return map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@driver_assignment_router.put("/{driver_id}/{vehicle_id}/{travel_date}")
async def update_driver_assignment(
    driver_id: int,
    vehicle_id: int,
    travel_date: date,
    assignment_updates: RouteFieldsDTO,
) -> DriverAssignmentResponseDTO:
    try:
        driver_assignment = driver_assignment_service.update_driver_assignment(
            map_driver_assignment_dto_to_driver_assignment_model(
                DriverAssignmentRequestDTO(
                    driver_id=driver_id,
                    vehicle_id=vehicle_id,
                    travel_date=travel_date,
                    **assignment_updates.model_dump(),
                )
            )
        )
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidArgumentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConflictWithExistingResourceException as e:
        raise HTTPException(status_code=409, detail=str(e))
    else:
        return map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)


@driver_assignment_router.delete("/{driver_id}/{vehicle_id}/{travel_date}")
def delete_driver_assignment(driver_id: int, vehicle_id: int, travel_date: date):
    try:
        driver_assignment_service.set_driver_assignment_as_inactive(
            driver_id, vehicle_id, travel_date
        )
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    else:
        return {"message": "Driver assignment marked as inactive"}


@driver_assignment_router.get("/driver_history/{driver_id}")
def get_driver_history(driver_id: int) -> list[DriverAssignmentResponseDTO]:
    return [
        map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)
        for driver_assignment in driver_assignment_service.get_assignments_history_for_driver(
            driver_id
        )
    ]


@driver_assignment_router.get("/vehicle_history/{vehicle_id}")
def get_vehicle_history(vehicle_id: int) -> list[DriverAssignmentResponseDTO]:
    return [
        map_driver_assignment_model_to_driver_assignment_dto(driver_assignment)
        for driver_assignment in driver_assignment_service.get_assignments_history_for_vehicle(
            vehicle_id
        )
    ]
