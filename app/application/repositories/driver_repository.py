from app.domain.models.driver_model import DriverModel


class DriverRepository:
    def get_driver_by_driver_id(self, driver_id: int) -> DriverModel | None:
        raise NotImplementedError(
            "Method get_driver_by_driver_id hasn't been implemented yet."
        )

    def get_driver_by_curp(self, curp: str) -> DriverModel | None:
        raise NotImplementedError(
            "Method get_driver_by_curp hasn't been implemented yet."
        )

    def get_all_drivers(self) -> list[DriverModel]:
        raise NotImplementedError("Method get_all_drivers hasn't been implemented yet.")

    def save_driver(self, driver: DriverModel) -> DriverModel:
        raise NotImplementedError("Method save_driver hasn't been implemented yet.")

    def delete_driver_by_driver_id(self, driver_id: int) -> None:
        raise NotImplementedError(
            "Method delete_driver_by_driver_id hasn't been implemented yet."
        )

    def get_number_of_drivers(self):
        raise NotImplementedError(
            "Method get_number_of_drivers hasn't been implemented yet."
        )
