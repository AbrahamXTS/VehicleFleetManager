from app.application.repositories.vehicle_repository import VehicleRepository
from app.application.repositories.user_repository import UserRepository
from app.domain.exceptions.conflict_with_existing_resource_exception import ConflictWithExistingResourceException
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.domain.models.vehicle_model import VehicleModel
from app.infrastructure.services.storage_service import StorageService
from typing import List
from datetime import datetime, timezone

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

    def get_vehicle_by_id(self, id: int) -> VehicleModel | None:
        if vehicle := self.vehicle_repository.get_vehicle_by_id(id=id):
            return vehicle
        raise ResourceNotFoundException
    
    def get_all_vehicles(self) -> List[VehicleModel]:
        return self.vehicle_repository.get_vehicles()
    
    def remove_vehicle_by_id(self, id: int):
        if not self.vehicle_repository.get_vehicle_by_id(id=id):
            raise ResourceNotFoundException
        return self.vehicle_repository.remove_vehicle_by_id(id=id)
    
    def is_vehicle_duplicate(self, vehicle: VehicleModel, id: int | None = None):
        found = self.vehicle_repository.get_vehicle_by_vin(
            vin=vehicle.vin
        ) or self.vehicle_repository.get_vehicle_by_plate(
            plate=vehicle.plate
        )
        if found:
            return found.id != id
        return False
    
    def update_vehicle(self, id: int, vehicle_update: VehicleModel):
        if not self.get_vehicle_by_id(id=id):
            raise ResourceNotFoundException
        if self.is_vehicle_duplicate(
            vehicle=vehicle_update, id=id
        ):
            raise ConflictWithExistingResourceException
        self.vehicle_repository.update_vehicle(
            vehicle_update=vehicle_update, id=id
        )

        if vehicle_update.picture:
            vehicle_update.picture = self.storage_service.save_base64_image(
                vehicle_update.picture, 
                f'{vehicle_update.vin}.jpg'
            )

        return self.vehicle_repository.get_vehicle_by_id(id)

    def create_vehicle(self, vehicle: VehicleModel):
        vehicle.entry_date = datetime.now(timezone.utc)
        if self.is_vehicle_duplicate(vehicle=vehicle):
            raise ConflictWithExistingResourceException
        vehicle.picture = self.storage_service.save_base64_image(
            vehicle.picture, 
            f'{vehicle.vin}.jpg'
        )
        return self.vehicle_repository.create_vehicle(vehicle=vehicle)
    
    def download_vehicle_picture(self, vin: str):
        return self.storage_service.read_file_as_bytes(
            f'{vin}.jpg'
        )