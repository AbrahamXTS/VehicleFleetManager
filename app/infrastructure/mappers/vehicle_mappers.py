from app.domain.models.vehicle_model import VehicleModel
from app.infrastructure.dto.vehicle_dto import VehicleDTO
from app.infrastructure.dto.vehicle_request_dto import VehicleRequestDTO
from app.infrastructure.entities.vehicle_entity import Vehicle


def map_vehicle_entity_to_vehicle_model(
    vehicle_entity: Vehicle,
) -> VehicleModel:
    return VehicleModel(
        id=vehicle_entity.id,
        brand=vehicle_entity.brand,
        model=vehicle_entity.model,
        vin=vehicle_entity.vin,
        plate=vehicle_entity.plate,
        purchase_date=vehicle_entity.purchase_date,
        cost=vehicle_entity.cost,
        picture=vehicle_entity.picture,
        entry_date=vehicle_entity.entry_date
    )


def map_vehicle_model_to_vehicle_entity(
    vehicle_model: VehicleModel,
) -> Vehicle:
    return Vehicle(
        id=vehicle_model.id,
        brand=vehicle_model.brand,
        model=vehicle_model.model,
        vin=vehicle_model.vin,
        plate=vehicle_model.plate,
        purchase_date=vehicle_model.purchase_date,
        cost=vehicle_model.cost,
        picture=vehicle_model.picture,
        entry_date=vehicle_model.entry_date
    )


def map_vehicle_model_to_vehicle_dto(
    vehicle_model: VehicleModel,
) -> VehicleDTO:
    return VehicleDTO(
        id=vehicle_model.id,
        brand=vehicle_model.brand,
        model=vehicle_model.model,
        vin=vehicle_model.vin,
        plate=vehicle_model.plate,
        purchase_date=vehicle_model.purchase_date,
        cost=vehicle_model.cost,
        picture=vehicle_model.picture,
        entry_date=vehicle_model.entry_date
    )


def map_vehicle_dto_to_vehicle_model(
    vehicle_request_dto: VehicleRequestDTO,
) -> VehicleModel:
    return VehicleModel(
        id=None,
        brand=vehicle_request_dto.brand,
        model=vehicle_request_dto.model,
        vin=vehicle_request_dto.vin,
        plate=vehicle_request_dto.plate,
        purchase_date=vehicle_request_dto.purchase_date,
        cost=vehicle_request_dto.cost,
        picture=vehicle_request_dto.picture,
        entry_date=None
    )
