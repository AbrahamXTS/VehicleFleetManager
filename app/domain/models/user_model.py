class UserModel:
    def __init__(
        self, id: int | None, name: str, last_name: str, email: str, password: str
    ) -> None:
        self.id = id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
