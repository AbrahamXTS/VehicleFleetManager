from typing import Annotated, List
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.application.services.vehicle_service import VehicleService
from app.domain.exceptions.conflict_with_existing_resource_exception import (
    ConflictWithExistingResourceException,
)
from app.domain.exceptions.file_not_found_exception import FileNotFoundException
from app.domain.exceptions.invalid_file_exception import InvalidFileException
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.domain.exceptions.invalid_base64_encode_exception import (
    Invalid64EncodeException,
)
from app.infrastructure.services.base64_service import Base64Service
from app.infrastructure.services.storage_service import StorageService
from app.infrastructure.dto.authenticated_user_dto import AuthenticatedUserDTO
from app.infrastructure.dto.vehicle_dto import VehicleDTO
from app.infrastructure.dto.vehicle_request_dto import VehicleRequestDTO
from app.infrastructure.mappers.vehicle_mappers import (
    map_vehicle_dto_to_vehicle_model,
    map_vehicle_model_to_vehicle_dto,
)
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
base64_service = Base64Service()
vehicle_service = VehicleService(
    vehicle_repository=RelationalDatabaseVehicleRepositoryImpl(),
    user_repository=RelationalDatabaseUserRepositoryImpl(),
    storage_service=StorageService(base64_service, "pictures"),
)

@vehicle_router.post("", status_code=status.HTTP_201_CREATED)
def create_vehicule(
    vehicle_request_dto: VehicleRequestDTO,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
) -> VehicleDTO:
    try:
        logger.info("API REQUEST - POST /vehicles/")
        logger.debug(f"Request body: {vehicle_request_dto.model_dump()}")
        vehicle = vehicle_service.create_vehicle(
            vehicle=map_vehicle_dto_to_vehicle_model(vehicle_request_dto)
        )
        logger.success(f"API RESPONSE {status.HTTP_201_CREATED} - POST /vehicles/")
        return map_vehicle_model_to_vehicle_dto(vehicle)
    except ConflictWithExistingResourceException:
        error_detail = "There is already a vehicle with the license plate or VIN number provided."
        logger.warning(f"API RESPONSE {status.HTTP_409_CONFLICT} - POST /vehicles/ - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_detail,
        )
    except InvalidFileException:
        error_detail = "Invalid file format or content. Please upload a valid image."
        logger.warning(f"API RESPONSE {status.HTTP_400_BAD_REQUEST} - POST /vehicles/ - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail,
        )
    except Invalid64EncodeException:
        error_detail = "Invalid base64 encoding. Please provide a valid base64 encoded string."
        logger.warning(f"API RESPONSE {status.HTTP_400_BAD_REQUEST} - POST /vehicles/ - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail,
        )


@vehicle_router.put("/{vehicule_id}", status_code=status.HTTP_201_CREATED)
def edit_vehicle(
    vehicule_id: int,
    vehicle_request_dto: VehicleRequestDTO,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
) -> VehicleDTO:
    try:
        logger.info(f"API REQUEST - PUT /vehicles/{vehicule_id}")
        logger.debug(f"Request body: {vehicle_request_dto.model_dump()}")
        vehicle = vehicle_service.update_vehicle(
            id=vehicule_id,
            vehicle_update=map_vehicle_dto_to_vehicle_model(vehicle_request_dto),
        )
        logger.success(f"API RESPONSE {status.HTTP_201_CREATED} - PUT /vehicles/{vehicule_id}")
        return map_vehicle_model_to_vehicle_dto(vehicle)
    except ResourceNotFoundException:
        error_detail = "Vehicle not found"
        logger.warning(f"API RESPONSE {status.HTTP_404_NOT_FOUND} - PUT /vehicles/{vehicule_id} - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error_detail
        )
    except ConflictWithExistingResourceException:
        error_detail = "There is already a vehicle with the license plate or VIN number provided."
        logger.warning(f"API RESPONSE {status.HTTP_409_CONFLICT} - PUT /vehicles/{vehicule_id} - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_detail,
        )
    except InvalidFileException:
        error_detail = "Invalid file format or content. Please upload a valid image."
        logger.warning(f"API RESPONSE {status.HTTP_400_BAD_REQUEST} - PUT /vehicles/{vehicule_id} - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail,
        )
    except Invalid64EncodeException:
        error_detail = "Invalid base64 encoding. Please provide a valid base64 encoded string."
        logger.warning(f"API RESPONSE {status.HTTP_400_BAD_REQUEST} - PUT /vehicles/{vehicule_id} - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail,
        )

@vehicle_router.get("", status_code=status.HTTP_200_OK)
def get_vehicles(
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
) -> List[VehicleDTO]:
    logger.info("API REQUEST - GET /vehicles/")
    vehicles = vehicle_service.get_all_vehicles()
    logger.success(f"API RESPONSE {status.HTTP_200_OK} - GET /vehicles/")
    return [
        map_vehicle_model_to_vehicle_dto(vehicle)
        for vehicle in vehicles
    ]


@vehicle_router.get("/{vehicle_id}", status_code=status.HTTP_200_OK)
def get_vehicle(
    vehicle_id: int,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
) -> VehicleDTO:
    try:
        logger.info(f"API REQUEST - GET /vehicles/{vehicle_id}")
        vehicle = vehicle_service.get_vehicle_by_id(id=vehicle_id)
        logger.success(f"API RESPONSE {status.HTTP_200_OK} - GET /vehicles/{vehicle_id}")
        return map_vehicle_model_to_vehicle_dto(vehicle)
    except ResourceNotFoundException:
        error_detail = "Vehicle not found"
        logger.warning(f"API RESPONSE {status.HTTP_404_NOT_FOUND} - GET /vehicles/{vehicle_id} - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error_detail
        )


@vehicle_router.delete("/{vehicle_id}", status_code=status.HTTP_200_OK)
def remove_vehicle(
    vehicle_id: int,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
):
    try:
        logger.info(f"API REQUEST - DELETE /vehicles/{vehicle_id}")
        vehicle_service.remove_vehicle_by_id(id=vehicle_id)
        logger.success(f"API RESPONSE {status.HTTP_200_OK} - DELETE /vehicles/{vehicle_id}")
    except ResourceNotFoundException:
        error_detail = "Vehicle not found"
        logger.warning(f"API RESPONSE {status.HTTP_404_NOT_FOUND} - DELETE /vehicles/{vehicle_id} - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error_detail
        )


@vehicle_router.get("/{vehicle_vin}/picture", status_code=status.HTTP_200_OK)
def download_vehicle_picture(
    vehicle_vin: str,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
):
    try:
        logger.info(f"API REQUEST - GET /vehicles/{vehicle_vin}/picture")
        picture_bytes = vehicle_service.download_vehicle_picture(vehicle_vin)
        logger.success(f"API RESPONSE {status.HTTP_200_OK} - GET /vehicles/{vehicle_vin}/picture")
        return Response(picture_bytes)
    except FileNotFoundException:
        error_detail = "Picture not found for the specified vehicle VIN."
        logger.warning(f"API RESPONSE {status.HTTP_404_NOT_FOUND} - GET /vehicles/{vehicle_vin}/picture - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_detail,
        )
    except InvalidFileException:
        error_detail = "Invalid picture file. Please ensure the file format is supported."
        logger.warning(f"API RESPONSE {status.HTTP_400_BAD_REQUEST} - GET /vehicles/{vehicle_vin}/picture - {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail,
        )
