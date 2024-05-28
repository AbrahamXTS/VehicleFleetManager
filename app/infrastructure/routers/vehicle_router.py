from typing import Annotated, List
import logging
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

logger = logging.getLogger(__name__)
vehicle_router = APIRouter()
base64_service = Base64Service()
vehicle_service = VehicleService(
    vehicle_repository=RelationalDatabaseVehicleRepositoryImpl(),
    user_repository=RelationalDatabaseUserRepositoryImpl(),
    storage_service=StorageService(base64_service, "pictures"),
)


@vehicle_router.post("/", status_code=status.HTTP_201_CREATED)
def create_vehicule(
    vehicle_request_dto: VehicleRequestDTO,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
) -> VehicleDTO:
    try:
        logger.info("POST /vehicles/")
        logger.debug(f"Request body: {vehicle_request_dto}")
        return map_vehicle_model_to_vehicle_dto(
            vehicle_service.create_vehicle(
                vehicle=map_vehicle_dto_to_vehicle_model(vehicle_request_dto)
            )
        )
    except ConflictWithExistingResourceException:
        logger.warning(
            f"POST /vehicles/ , Vehicle already exists. {status.HTTP_409_CONFLICT}"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a vehicle with the license plate or VIN number provided.",
        )
    except InvalidFileException:
        logger.warning(
            f"POST /vehicles/ , Invalid file format or content. {status.HTTP_400_BAD_REQUEST}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format or content. Please upload a valid image.",
        )
    except Invalid64EncodeException:
        logger.warning(
            f"POST /vehicles/ , Invalid base64 encoding. {status.HTTP_400_BAD_REQUEST}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid base64 encoding. Please provide a valid base64 encoded string.",
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
        logger.info(f"PUT /vehicles/{vehicule_id}")
        logger.debug(f"Request body: {vehicle_request_dto}")
        return map_vehicle_model_to_vehicle_dto(
            vehicle_service.update_vehicle(
                id=vehicule_id,
                vehicle_update=map_vehicle_dto_to_vehicle_model(vehicle_request_dto),
            )
        )
    except ResourceNotFoundException:
        logger.warning(
            f"PUT /vehicles/ , Vehicle with id {vehicule_id} not found. {status.HTTP_404_NOT_FOUND}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
        )
    except ConflictWithExistingResourceException:
        logger.warning(
            f"PUT /vehicles/ , Vehicle with id {vehicule_id} already exists. {status.HTTP_409_CONFLICT}"
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a vehicle with the license plate or VIN number provided.",
        )
    except InvalidFileException:
        logger.warning(
            f"PUT /vehicles/ , Invalid file format or content. {status.HTTP_400_BAD_REQUEST}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format or content. Please upload a valid image.",
        )
    except Invalid64EncodeException:
        logger.warning(
            f"PUT /vehicles/ , Invalid base64 encoding. {status.HTTP_400_BAD_REQUEST}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid base64 encoding. Please provide a valid base64 encoded string.",
        )


@vehicle_router.get("/", status_code=status.HTTP_200_OK)
def get_vehicles(
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
) -> List[VehicleDTO]:
    logger.info("GET /vehicles/")
    return [
        map_vehicle_model_to_vehicle_dto(vehicle)
        for vehicle in vehicle_service.get_all_vehicles()
    ]


@vehicle_router.get("/{vehicle_id}", status_code=status.HTTP_200_OK)
def get_vehicle(
    vehicle_id: int,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
) -> VehicleDTO:
    try:
        logger.info(f"GET /vehicles/{vehicle_id}")
        return map_vehicle_model_to_vehicle_dto(
            vehicle_service.get_vehicle_by_id(id=vehicle_id)
        )
    except ResourceNotFoundException:
        logger.warning(
            f"GET /vehicles/{vehicle_id} , Vehicle with id {vehicle_id} not found. {status.HTTP_404_NOT_FOUND}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
        )


@vehicle_router.delete("/{vehicle_id}", status_code=status.HTTP_200_OK)
def remove_vehicle(
    vehicle_id: int,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
):
    try:
        logger.info(f"DELETE /vehicles/{vehicle_id}")
        vehicle_service.remove_vehicle_by_id(id=vehicle_id)
    except ResourceNotFoundException:
        logger.warning(
            f"DELETE /vehicles/{vehicle_id} , Vehicle with id {vehicle_id} not found. {status.HTTP_404_NOT_FOUND}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
        )


@vehicle_router.get("/{vehicle_vin}/picture", status_code=status.HTTP_200_OK)
def download_vehicle_picture(
    vehicle_vin: str,
    authenticated_user: Annotated[
        AuthenticatedUserDTO, Depends(protect_route_middlware)
    ],
):
    try:
        logger.info(f"GET /vehicles/{vehicle_vin}/picture")
        return Response(vehicle_service.download_vehicle_picture(vehicle_vin))
    except FileNotFoundException:
        logger.warning(
            f"GET /vehicles/{vehicle_vin}/picture , Picture not found for vehicle with VIN {vehicle_vin}. {status.HTTP_404_NOT_FOUND}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Picture not found for the specified vehicle VIN.",
        )
    except InvalidFileException:
        logger.warning(
            f"GET /vehicles/{vehicle_vin}/picture , Invalid picture file for vehicle with VIN {vehicle_vin}. {status.HTTP_400_BAD_REQUEST}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid picture file. Please ensure the file format is supported.",
        )
