from loguru import logger

from app.application.repositories.driver_repository import (
    DriverRepository,
)
from app.domain.exceptions.conflict_with_existing_resource_exception import (
    ConflictWithExistingResourceException,
)
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.domain.models.driver_model import DriverModel


class DriverService:
    def __init__(
        self,
        driver_repository: DriverRepository,
    ) -> None:
        self.driver_repository = driver_repository

    def get_driver_by_driver_id(self, driver_id: int) -> DriverModel:
        logger.debug("Method called: driver_service.get_driver_by_driver_id()")
        logger.debug(f"Params passed: {driver_id}")
        if driver := self.driver_repository.get_driver_by_driver_id(driver_id):
            return driver
        raise ResourceNotFoundException

    def get_all_drivers(self) -> list[DriverModel]:
        logger.debug("Method called: driver_service.get_all_drivers()")
        return self.driver_repository.get_all_drivers()

    def create_driver(self, driver: DriverModel) -> DriverModel:
        logger.debug("Method called: driver_service.create_driver()")
        logger.debug(f"Params passed: {driver.__dict__}")
        if self.driver_repository.get_driver_by_curp(driver.curp):
            raise ConflictWithExistingResourceException

        return self.driver_repository.save_driver(driver)

    def update_driver(self, driver: DriverModel) -> DriverModel:
        logger.debug("Method called: driver_service.update_driver()")
        logger.debug(f"Params passed: {driver.__dict__}")
        if not driver.id or not self.driver_repository.get_driver_by_driver_id(
            driver.id
        ):
            raise ResourceNotFoundException

        return self.driver_repository.save_driver(driver)

    def delete_driver_by_driver_id(self, driver_id: int):
        logger.debug("Method called: driver_service.delete_driver_by_driver_id()")
        logger.debug(f"Params passed: {driver_id}")
        if not self.get_driver_by_driver_id(driver_id):
            raise ResourceNotFoundException

        return self.driver_repository.delete_driver_by_driver_id(driver_id)
