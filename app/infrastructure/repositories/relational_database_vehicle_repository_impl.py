from sqlmodel import Session, select
from typing import List
import logging

from app.application.repositories.vehicle_repository import (
    VehicleRepository,
)
from app.infrastructure.configs.sql_database import db_engine
from app.infrastructure.entities.vehicle_entity import Vehicle
from app.domain.models.vehicle_model import VehicleModel
from app.infrastructure.entities.vehicle_entity import Vehicle
from app.infrastructure.mappers.vehicle_mappers import (
    map_vehicle_entity_to_vehicle_model,
    map_vehicle_model_to_vehicle_entity,
)

class RelationalDatabaseVehicleRepositoryImpl(VehicleRepository):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_vehicle_by_id(self, id: int) -> VehicleModel | None:
        self.logger.info(f"Method get_vehicle_by_id() , Getting vehicle with ID: {id}")
        with Session(db_engine) as session:
            vehicle_entity = session.exec(
                select(Vehicle).where(Vehicle.id == id)
            ).first()

            if vehicle_entity:
                self.logger.debug(f"Method get_vehicle_by_id(), Vehicle: {vehicle_entity}")
                return map_vehicle_entity_to_vehicle_model(
                    vehicle_entity
                )
            
    def get_vehicle_by_vin(self, vin: str) -> VehicleModel | None:
        self.logger.info(f"Method get_vehicle_by_vin(), Getting vehicle with VIN: {vin}")
        with Session(db_engine) as session:
            vehicle_entity = session.exec(
                select(Vehicle).where(Vehicle.vin == vin)
            ).first()
            if vehicle_entity:
                self.logger.debug(f"Vehicle: {vehicle_entity}")
                return map_vehicle_entity_to_vehicle_model(
                    vehicle_entity
                )
            
            
    def get_vehicle_by_plate(self, plate: str) -> VehicleModel | None:
        self.logger.info(f"Method get_vehicles_by_plate(), Getting vehicle with plate: {plate}")
        with Session(db_engine) as session:
            vehicle_entity = session.exec(
                select(Vehicle).where(Vehicle.plate == plate)
            ).first()            
            if vehicle_entity:
                self.logger.debug(f"Vehicle: {vehicle_entity}")
                return map_vehicle_entity_to_vehicle_model(
                    vehicle_entity
                )

    def get_vehicles(self) -> List[VehicleModel] | None:
        self.logger.info("Method get_vehicles(), Getting all vehicles")
        with Session(db_engine) as session:
            vehicles = session.exec(
                select(Vehicle)
            )

            if vehicles:
                self.logger.debug(f"Vehicles: {vehicles.all()}")
                return [
                    map_vehicle_entity_to_vehicle_model(vehicle)
                    for vehicle in vehicles
                ]

    def remove_vehicle_by_id(self, id: int) -> int | None:
        self.logger.info(f"Method remove_vehicle_by_id(), Removing vehicle with ID: {id}")
        with Session(db_engine) as session:
            vehicle_entity = session.exec(
                select(Vehicle).where(Vehicle.id == id)
            ).one()

            session.delete(vehicle_entity)
            session.commit()
            self.logger.debug(f"Vehicle removed: {vehicle_entity}")

    def update_vehicle(self, vehicle_update: VehicleModel, id: int):
        self.logger.info(f"Method update_vehicle(), Updating vehicle with ID: {id}")
        with Session(db_engine) as session:
            vehicle_entity = session.exec(
                select(Vehicle).where(Vehicle.id == id)
            ).one()
            
            vehicle_entity.brand = vehicle_update.brand
            vehicle_entity.model = vehicle_update.model
            vehicle_entity.vin = vehicle_update.vin
            vehicle_entity.plate = vehicle_update.plate
            vehicle_entity.purchase_date = vehicle_update.purchase_date
            vehicle_entity.cost = vehicle_update.cost
            vehicle_entity.picture = vehicle_update.picture
            
            session.add(vehicle_entity)
            session.commit()
            session.refresh(vehicle_entity)
            self.logger.debug(f"Vehicle updated: {vehicle_entity}")
        return map_vehicle_entity_to_vehicle_model(
            vehicle_entity=vehicle_entity
        )

    def create_vehicle(
        self, vehicle: VehicleModel
    ) -> VehicleModel:
        self.logger.info(f"Method create_vehicle(), Creating vehicle")
        with Session(db_engine) as session:
            vehicle_entity = (
                map_vehicle_model_to_vehicle_entity(vehicle)
            )

            session.add(vehicle_entity)
            session.commit()
            session.refresh(vehicle_entity)
            self.logger.debug(f"Vehicle created: {vehicle_entity}")
            return map_vehicle_entity_to_vehicle_model(
                vehicle_entity
            )
        
    def get_number_of_vehicles(self) -> int:
        with Session(db_engine) as session:
            number_of_vehicles = len(session.exec(select(Vehicle)).all())
            self.logger.debug(f"Retrieved {number_of_vehicles} vehicles")
        return number_of_vehicles