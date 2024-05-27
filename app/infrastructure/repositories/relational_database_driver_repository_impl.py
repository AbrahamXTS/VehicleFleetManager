from sqlmodel import Session, select
import logging

from app.application.repositories.driver_repository import DriverRepository
from app.domain.models.driver_model import DriverModel
from app.infrastructure.configs.sql_database import db_engine
from app.infrastructure.entities.driver_entity import Driver
from app.infrastructure.mappers.driver_mappers import (
    map_driver_entity_to_driver_model,
    map_driver_model_to_driver_entity,
)


class RelationalDatabaseDriverRepositoryImpl(DriverRepository):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_driver_by_driver_id(self, driver_id: int) -> DriverModel | None:
        self.logger.info(f"Method get_driver_by_driver_id(), Getting driver with ID: {driver_id}")
        with Session(db_engine) as session:
            driver_entity = session.exec(
                select(Driver).where(Driver.id == driver_id)
            ).first()

            if driver_entity:
                self.logger.debug(f"Driver: {driver_entity}")
                return map_driver_entity_to_driver_model(driver_entity)
            else:
                self.logger.info("Driver not found")
                return None

    def get_driver_by_curp(self, curp: str) -> DriverModel | None:
        self.logger.info(f"Method get_driver_by_curp(), Getting driver with CURP: {curp}")
        with Session(db_engine) as session:
            driver_entity = session.exec(
                select(Driver).where(Driver.curp == curp)
            ).first()

            if driver_entity:
                self.logger.debug(f"Driver: {driver_entity}")
                return map_driver_entity_to_driver_model(driver_entity)

    def get_all_drivers(self) -> list[DriverModel]:
        with Session(db_engine) as session:
            drivers_entity = session.exec(select(Driver)).all()
            self.logger.info(f"Method get_all_drivers(), Retrieved {len(drivers_entity)} drivers")
            self.logger.debug(f"Drivers: {drivers_entity}")
            return [
                map_driver_entity_to_driver_model(driver) for driver in drivers_entity
            ]

    def save_driver(self, driver: DriverModel) -> DriverModel:
        self.logger.info(f"Method save_driver()")
        with Session(db_engine) as session:
            driver_entity = None

            if driver.id:
                driver_entity = session.exec(
                    select(Driver).where(Driver.id == driver.id)
                ).one()

                driver_entity.first_name = driver.name
                driver_entity.last_name = driver.last_name
                driver_entity.birth_date = driver.birth_date
                driver_entity.curp = driver.curp
                driver_entity.address = driver.address
                driver_entity.monthly_salary = driver.monthly_salary
                driver_entity.license_number = driver.driving_license
                driver_entity.entry_date = driver.registration_date
            else:
                driver_entity = map_driver_model_to_driver_entity(driver)

            session.add(driver_entity)
            session.commit()
            session.refresh(driver_entity)
            self.logger.debug(f"Driver saved: {driver_entity}")
            return map_driver_entity_to_driver_model(driver_entity)

    def delete_driver_by_driver_id(self, driver_id: int) -> None:
        self.logger.info(f"Method delete_driver_by_driver_id(), Deleting driver with ID: {driver_id}")
        with Session(db_engine) as session:
            driver_entity = session.exec(
                select(Driver).where(Driver.id == driver_id)
            ).one()

            session.delete(driver_entity)
            session.commit()
            self.logger.debug(f"Driver: {driver_entity}")

    def get_number_of_drivers(self) -> int:
        with Session(db_engine) as session:
            number_of_drivers = len(session.exec(select(Driver)).all())
            self.logger.debug(f"Retrieved {number_of_drivers} drivers")
        return number_of_drivers