from sqlmodel import Session, select
from loguru import logger

from app.application.repositories.driver_repository import DriverRepository
from app.domain.models.driver_model import DriverModel
from app.infrastructure.configs.sql_database import db_engine
from app.infrastructure.entities.driver_entity import Driver
from app.infrastructure.mappers.driver_mappers import (
    map_driver_entity_to_driver_model,
    map_driver_model_to_driver_entity,
)


class RelationalDatabaseDriverRepositoryImpl(DriverRepository):

    def get_driver_by_driver_id(self, driver_id: int) -> DriverModel | None:
        with Session(db_engine) as session:
            driver_entity = session.exec(
                select(Driver).where(Driver.id == driver_id)
            ).first()

            if driver_entity:
                logger.debug(f"Method get_driver_by_driver_id(), Retrieved driver with ID: {driver_id}")
                return map_driver_entity_to_driver_model(driver_entity)
            else:
                return None

    def get_driver_by_curp(self, curp: str) -> DriverModel | None:
        with Session(db_engine) as session:
            driver_entity = session.exec(
                select(Driver).where(Driver.curp == curp)
            ).first()

            if driver_entity:
                logger.debug(f"Method get_driver_by_curp(), Retrieved driver with CURP: {curp}")
                return map_driver_entity_to_driver_model(driver_entity)

    def get_all_drivers(self) -> list[DriverModel]:
        with Session(db_engine) as session:
            drivers_entity = session.exec(select(Driver)).all()
            logger.debug(f"Method get_all_drivers(), Retrieved {len(drivers_entity)} drivers")
            return [
                map_driver_entity_to_driver_model(driver) for driver in drivers_entity
            ]

    def save_driver(self, driver: DriverModel) -> DriverModel:
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
            logger.debug(f"Method save_driver(), Driver with ID: {driver_entity.id} saved")
            return map_driver_entity_to_driver_model(driver_entity)

    def delete_driver_by_driver_id(self, driver_id: int) -> None:
        with Session(db_engine) as session:
            driver_entity = session.exec(
                select(Driver).where(Driver.id == driver_id)
            ).one()

            session.delete(driver_entity)
            session.commit()
            logger.debug(f"Method delete_driver_by_driver_id(), Driver with ID: {driver_id} deleted")

    def get_number_of_drivers(self) -> int:
        with Session(db_engine) as session:
            number_of_drivers = len(session.exec(select(Driver)).all())
            logger.debug(f"Method get_number_of_drivers(), Retrieved {number_of_drivers} drivers")
        return number_of_drivers
