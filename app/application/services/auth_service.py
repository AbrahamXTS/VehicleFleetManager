from app.domain.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.domain.models.candidate_model import CandidateModel
from app.domain.models.user_model import UserModel

from ..repositories.user_repository import UserRepository
from ..security.password_encryptor import PasswordEncryptor


class AuthService:
    def __init__(
        self, user_repository: UserRepository, password_encryptor: PasswordEncryptor
    ) -> None:
        self.user_repository = user_repository
        self.password_encryptor = password_encryptor

    def login(self, email: str, password: str) -> UserModel:
        user = self.user_repository.get_user_by_email(email)

        if not user or not self.password_encryptor.verify_password_hash(
            password, user.password
        ):
            raise InvalidCredentialsException

        return user

    def signup(self, candidate: CandidateModel) -> UserModel:
        # Todo: Validate invitation code
        return self.user_repository.save_user(
            UserModel(
                id=None,
                email=candidate.email,
                last_name=candidate.last_name,
                name=candidate.name,
                password=self.password_encryptor.get_password_hash(candidate.password),
            )
        )
