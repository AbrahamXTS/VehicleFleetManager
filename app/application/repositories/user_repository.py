from app.domain.models.invitation_code_model import InvitationCodeModel
from app.domain.models.user_model import UserModel


class UserRepository:
    def get_user_by_email(self, email: str) -> UserModel | None:
        raise NotImplementedError(
            "Method get_user_by_email hasn't been implemented yet."
        )

    def get_all_users(self) -> list[UserModel]:
        raise NotImplementedError("Method get_all_users hasn't been implemented yet.")

    def get_invitation_codes_created_by_user_id(
        self, user_id: int
    ) -> list[InvitationCodeModel]:
        raise NotImplementedError(
            "Method get_invitation_codes_created_by_user_id hasn't been implemented yet."
        )

    def save_user(self, user: UserModel) -> UserModel:
        raise NotImplementedError("Method save_user hasn't been implemented yet.")

    def delete_user_by_user_id(self, user_id: int) -> None:
        raise NotImplementedError("Method delete_user hasn't been implemented yet.")

    def get_number_of_users(self):
        raise NotImplementedError(
            "Method get_number_of_users hasn't been implemented yet."
        )