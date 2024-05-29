from datetime import date


class DriverModel:
    def __init__(
        self,
        id: int | None,
        name: str,
        last_name: str,
        birth_date: date,
        curp: str,
        address: str,
        monthly_salary: float,
        driving_license: str,
        registration_date: date,
    ):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.curp = curp
        self.address = address
        self.monthly_salary = monthly_salary
        self.driving_license = driving_license
        self.registration_date = registration_date
