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
        logger.debug("Method called: relational_database_driver_repository_impl.get_driver_by_driver_id()")
        logger.debug(f"Params passed: {driver_id}")
        with Session(db_engine) as session:
            driver_entity = session.exec(
                select(Driver).where(Driver.id == driver_id)
            ).first()

            if driver_entity:
                return map_driver_entity_to_driver_model(driver_entity)
            else:
                return None

    def get_driver_by_curp(self, curp: str) -> DriverModel | None:
        logger.debug("Method called: relational_database_driver_repository_impl.get_driver_by_curp()")
        logger.debug(f"Params passed: {curp}")
        with Session(db_engine) as session:
            driver_entity = session.exec(
                select(Driver).where(Driver.curp == curp)
            ).first()

            if driver_entity:
                return map_driver_entity_to_driver_model(driver_entity)

    def get_all_drivers(self) -> list[DriverModel]:
        logger.debug("Method called: relational_database_driver_repository_impl.get_all_drivers()")
        with Session(db_engine) as session:
            drivers_entity = session.exec(select(Driver)).all()
            return [
                map_driver_entity_to_driver_model(driver) for driver in drivers_entity
            ]

    def save_driver(self, driver: DriverModel) -> DriverModel:
        logger.debug("Method called: relational_database_driver_repository_impl.save_driver()")
        logger.debug(f"Params passed: {driver.__dict__}")
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
            return map_driver_entity_to_driver_model(driver_entity)

    def delete_driver_by_driver_id(self, driver_id: int) -> None:
        logger.debug("Method called: relational_database_driver_repository_impl.delete_driver_by_driver_id()")
        logger.debug(f"Params passed: {driver_id}")
        with Session(db_engine) as session:
            driver_entity = session.exec(
                select(Driver).where(Driver.id == driver_id)
            ).one()

            session.delete(driver_entity)
            session.commit()

    def get_number_of_drivers(self) -> int:
        logger.debug("Method called: relational_database_driver_repository_impl.get_number_of_drivers()")
        with Session(db_engine) as session:
            number_of_drivers = len(session.exec(select(Driver)).all())
        return number_of_drivers
