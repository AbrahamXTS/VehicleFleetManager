from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.services.vehicle_service import VehicleService
from app.domain.exceptions.conflict_with_existing_resource_exception import ConflictWithExistingResourceException
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.infrastructure.dto.authenticated_user_dto import AuthenticatedUserDTO
from app.infrastructure.dto.vehicle_dto import VehicleDTO
from app.infrastructure.dto.vehicle_request_dto import VehicleRequestDTO
from app.infrastructure.mappers.vehicle_mappers import map_vehicle_dto_to_vehicle_model, map_vehicle_model_to_vehicle_dto
from app.infrastructure.middlewares.protect_route_middleware import (
    protect_route_middlware,
)
from app.infrastructure.repositories.relational_database_vehicle_repository_impl import (
    RelationalDatabaseVehicleRepositoryImpl,
)
from app.infrastructure.repositories.relational_database_user_repository_impl import (
    RelationalDatabaseUserRepositoryImpl,
)


vehicle_router = APIRouter()
vehicle_service = VehicleService(
    vehicle_repository=RelationalDatabaseVehicleRepositoryImpl(),
    user_repository=RelationalDatabaseUserRepositoryImpl()
)

@vehicle_router.post("/", status_code=status.HTTP_201_CREATED)
def create_vehicule(
    vehicle_request_dto: VehicleRequestDTO,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
) -> VehicleDTO:
    try:
        return map_vehicle_model_to_vehicle_dto(
            vehicle_service.create_vehicle(
                vehicle=map_vehicle_dto_to_vehicle_model(
                    vehicle_request_dto
                )
            )
        )
    except ConflictWithExistingResourceException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a vehicle with the license plate or VIN number provided.",
        )

@vehicle_router.put("/{vehicule_id}", status_code=status.HTTP_201_CREATED)
def edit_vehicle(
    vehicule_id: int,
    vehicle_request_dto: VehicleRequestDTO,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ]
) -> VehicleDTO:
    try:
        return map_vehicle_model_to_vehicle_dto(
            vehicle_service.update_vehicle(
                id=vehicule_id, vehicle_update=map_vehicle_dto_to_vehicle_model(
                    vehicle_request_dto
                )
            )
        )
    except ResourceNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    except ConflictWithExistingResourceException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a vehicle with the license plate or VIN number provided.",
        )

@vehicle_router.get("/", status_code=status.HTTP_200_OK)
def get_vehicles(
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ]
) -> List[VehicleDTO]:
    return [
        map_vehicle_model_to_vehicle_dto(vehicle)
        for vehicle in vehicle_service.get_all_vehicles()
    ]

@vehicle_router.get("/{vehicle_id}", status_code=status.HTTP_200_OK)
def get_vehicle(
    vehicle_id: int,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ]
) -> VehicleDTO:
    try:
        return map_vehicle_model_to_vehicle_dto(
            vehicle_service.get_vehicle_by_id(id=vehicle_id)
        )
    except ResourceNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

@vehicle_router.delete("/{vehicle_id}", status_code=status.HTTP_200_OK)
def remove_vehicle(
    vehicle_id: int,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ]
):
    try:
        vehicle_service.remove_vehicle_by_id(id=vehicle_id)
    except ResourceNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
