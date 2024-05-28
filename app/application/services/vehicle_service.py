from app.application.repositories.vehicle_repository import VehicleRepository
from app.application.repositories.user_repository import UserRepository
from app.domain.exceptions.conflict_with_existing_resource_exception import ConflictWithExistingResourceException
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.domain.models.vehicle_model import VehicleModel
from app.infrastructure.services.storage_service import StorageService
from typing import List
from datetime import datetime, timezone
import logging

class VehicleService:
    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        user_repository: UserRepository,
        storage_service: StorageService
    ) -> None:
        self.vehicle_repository = vehicle_repository
        self.user_repository = user_repository
        self.storage_service = storage_service
        self.logger = logging.getLogger(__name__)

    def get_vehicle_by_id(self, id: int) -> VehicleModel | None:
        self.logger.info("Method get_vehicle_by_id()")
        if vehicle := self.vehicle_repository.get_vehicle_by_id(id=id):
            return vehicle
        self.logger.warning(f"Vehicle with id {id} not found")
        raise ResourceNotFoundException
    
    def get_all_vehicles(self) -> List[VehicleModel]:
        self.logger.info("Method get_all_vehicles()")
        return self.vehicle_repository.get_vehicles()
    
    def remove_vehicle_by_id(self, id: int):
        self.logger.info("Method remove_vehicle_by_id()")
        if not self.vehicle_repository.get_vehicle_by_id(id=id):
            self.logger.warning(f"Vehicle with id {id} not found")
            raise ResourceNotFoundException
        return self.vehicle_repository.remove_vehicle_by_id(id=id)
    
    def is_vehicle_duplicate(self, vehicle: VehicleModel, id: int | None = None):
        self.logger.info("Method is_vehicle_duplicate()")
        found = self.vehicle_repository.get_vehicle_by_vin(
            vin=vehicle.vin
        ) or self.vehicle_repository.get_vehicle_by_plate(
            plate=vehicle.plate
        )
        if found:
            return found.id != id
        return False
    
    def update_vehicle(self, id: int, vehicle_update: VehicleModel):
        self.logger.info("Method update_vehicle()")
        if not self.get_vehicle_by_id(id=id):
            self.logger.warning(f"Vehicle with id {id} not found")
            raise ResourceNotFoundException
        if self.is_vehicle_duplicate(
            vehicle=vehicle_update, id=id
        ):
            self.logger.warning(f"Duplicate vehicle found with id {id}")
            raise ConflictWithExistingResourceException
        if vehicle_update.picture:
            vehicle_update.picture = self.storage_service.save_base64_image(
                vehicle_update.picture, 
                f'{vehicle_update.vin}.jpg'
            )
        self.vehicle_repository.update_vehicle(
            vehicle_update=vehicle_update, id=id
        )
        return self.vehicle_repository.get_vehicle_by_id(id)

    def create_vehicle(self, vehicle: VehicleModel):
        self.logger.info("Method create_vehicle()")
        vehicle.entry_date = datetime.now(timezone.utc)
        if self.is_vehicle_duplicate(vehicle=vehicle):
            self.logger.warning("Duplicate vehicle found")
            raise ConflictWithExistingResourceException
        vehicle.picture = self.storage_service.save_base64_image(
            vehicle.picture, 
            f'{vehicle.vin}.jpg'
        )
        return self.vehicle_repository.create_vehicle(vehicle=vehicle)
    
    def download_vehicle_picture(self, vin: str):
        self.logger.info("Method download_vehicle_picture()")
        self.logger.debug(f"Downloading picture for vehicle with VIN {vin}")
        return self.storage_service.read_file_as_bytes(
            f'{vin}.jpg'
        )
    