from typing import List
from app.domain.models.vehicle_model import VehicleModel


class VehicleRepository:
    def get_vehicle_by_id(self, id: int) -> VehicleModel | None:
        raise NotImplementedError(
            "Method get_vehicle_by_id hasn't been implemented yet."
        )
    
    def get_vehicle_by_vin(self, vin: str) -> VehicleModel | None:
        raise NotImplementedError(
            "Method get_vehicle_by_id hasn't been implemented yet."
        )
    
    def get_vehicle_by_plate(self, plate: str) -> VehicleModel | None:
        raise NotImplementedError(
            "Method get_vehicle_by_id hasn't been implemented yet."
        )

    def get_vehicles(self) -> List[VehicleModel] | None:
        raise NotImplementedError(
            "Method get_vehicles hasn't been implemented yet."
        )

    def remove_vehicle_by_id(self, id: int) -> str | None:
        raise NotImplementedError(
            "Method remove_vehicle_by_id hasn't been implemented yet."
        )
    
    def update_vehicle(self, vehicle_update: VehicleModel, id: int) -> VehicleModel | None:
        raise NotImplementedError(
            "Method update_vehicle hasn't been implemented yet."
        )

    def create_vehicle(self, vehicle: VehicleModel) -> VehicleModel | None:
        raise NotImplementedError(
            "Method create_vehicle hasn't been implemented yet."
        )