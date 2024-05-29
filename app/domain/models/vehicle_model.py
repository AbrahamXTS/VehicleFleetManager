from datetime import datetime


class VehicleModel:
    def __init__(
        self,
        id: int | None,
        brand: str,
        model: str,
        vin: str,
        plate: str,
        purchase_date: str | datetime,
        cost: float | int,
        picture: str,
        entry_date: str | datetime,
    ) -> None:
        self.id = id
        self.brand = brand
        self.model = model
        self.vin = vin
        self.plate = plate
        self.purchase_date = purchase_date
        self.cost = cost
        self.picture = picture
        self.entry_date = entry_date
