import logging

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
        self.logger = logging.getLogger(__name__)

    def get_driver_by_driver_id(self, driver_id: int) -> DriverModel:
        self.logger.info("Method get_driver_by_driver_id()")
        if driver := self.driver_repository.get_driver_by_driver_id(driver_id):
            return driver

        self.logger.warning(f"Driver with ID {driver_id} not found")
        raise ResourceNotFoundException

    def get_all_drivers(self) -> list[DriverModel]:
        self.logger.info("Method get_all_drivers()")
        return self.driver_repository.get_all_drivers()

    def create_driver(self, driver: DriverModel) -> DriverModel:
        self.logger.info("Method create_driver()")
        if self.driver_repository.get_driver_by_curp(driver.curp):
            self.logger.warning(f"Driver with CURP {driver.curp} already exists")
            raise ConflictWithExistingResourceException

        return self.driver_repository.save_driver(driver)

    def update_driver(self, driver: DriverModel) -> DriverModel:
        self.logger.info("Method update_driver()")
        if not driver.id or not self.driver_repository.get_driver_by_driver_id(
            driver.id
        ):
            self.logger.warning(f"Driver with ID {driver.id} not found")
            raise ResourceNotFoundException

        return self.driver_repository.save_driver(driver)

    def delete_driver_by_driver_id(self, driver_id: int):
        self.logger.info("Method delete_driver_by_driver_id()")
        if not self.get_driver_by_driver_id(driver_id):
            self.logger.warning(f"Driver with ID {driver_id} not found")
            raise ResourceNotFoundException

        return self.driver_repository.delete_driver_by_driver_id(driver_id)

