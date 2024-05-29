from app.domain.models.driver_model import DriverModel
from app.infrastructure.dto.driver_dto import DriverDTO
from app.infrastructure.dto.driver_request_dto import DriverRequestDTO
from app.infrastructure.entities.driver_entity import Driver


def map_driver_entity_to_driver_model(
    driver_entity: Driver,
) -> DriverModel:
    return DriverModel(
        address=driver_entity.address,
        birth_date=driver_entity.birth_date,
        curp=driver_entity.curp,
        driving_license=driver_entity.license_number,
        id=driver_entity.id,
        last_name=driver_entity.last_name,
        monthly_salary=driver_entity.monthly_salary,
        name=driver_entity.first_name,
        registration_date=driver_entity.entry_date,
    )


def map_driver_model_to_driver_entity(
    driver_model: DriverModel,
) -> Driver:
    return Driver(
        address=driver_model.address,
        birth_date=driver_model.birth_date,
        curp=driver_model.curp,
        entry_date=driver_model.registration_date,
        first_name=driver_model.name,
        id=driver_model.id,
        last_name=driver_model.last_name,
        license_number=driver_model.driving_license,
        monthly_salary=driver_model.monthly_salary,
    )


def map_driver_dto_to_driver_model(driver_dto: DriverDTO):
    return DriverModel(
        address=driver_dto.address,
        birth_date=driver_dto.birth_date,
        curp=driver_dto.curp,
        driving_license=driver_dto.driving_license,
        id=driver_dto.id,
        last_name=driver_dto.last_name,
        monthly_salary=driver_dto.monthly_salary,
        name=driver_dto.name,
        registration_date=driver_dto.registration_date,
    )


def map_driver_request_dto_to_driver_model(
    driver_request_dto: DriverRequestDTO,
) -> DriverModel:
    return DriverModel(
        address=driver_request_dto.address,
        birth_date=driver_request_dto.birth_date,
        curp=driver_request_dto.curp,
        driving_license=driver_request_dto.driving_license,
        id=None,
        last_name=driver_request_dto.last_name,
        monthly_salary=driver_request_dto.monthly_salary,
        name=driver_request_dto.name,
        registration_date=driver_request_dto.registration_date,
    )


def map_driver_model_to_driver_dto(
    driver_model: DriverModel,
) -> DriverDTO:
    return DriverDTO(
        address=driver_model.address,
        birth_date=driver_model.birth_date,
        curp=driver_model.curp,
        driving_license=driver_model.driving_license,
        id=driver_model.id or 0,
        last_name=driver_model.last_name,
        monthly_salary=driver_model.monthly_salary,
        name=driver_model.name,
        registration_date=driver_model.registration_date,
    )
