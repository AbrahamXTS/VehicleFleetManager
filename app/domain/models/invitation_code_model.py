class InvitationCodeModel:
    def __init__(self, code: str | None, email: str, created_by_user: int) -> None:
        self.code = code
        self.email = email
        self.created_by_user = created_by_user
