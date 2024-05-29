class CandidateModel:
    def __init__(
        self, name: str, last_name: str, email: str, password: str, invitation_code: str
    ) -> None:
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.invitation_code = invitation_code
