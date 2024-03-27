from app.domain.models.invitation_code_model import InvitationCodeModel


class InvitationCodeRepository:
    def get_invitation_code_by_code(self, code: str) -> InvitationCodeModel | None:
        raise NotImplementedError(
            "Method get_invitation_code_by_code hasn't been implemented yet."
        )

    def get_invitation_code_by_email(self, email: str) -> InvitationCodeModel | None:
        raise NotImplementedError(
            "Method get_invitation_code_by_email hasn't been implemented yet."
        )

    def get_invitation_code_by_code_and_email(
        self, code: str, email: str
    ) -> InvitationCodeModel | None:
        raise NotImplementedError(
            "Method get_invitation_code_by_code_and_email hasn't been implemented yet."
        )

    def save_invitation_code(
        self, invitation_code: InvitationCodeModel
    ) -> InvitationCodeModel:
        raise NotImplementedError(
            "Method save_invitation_code hasn't been implemented yet."
        )

    def delete_invitation_code_by_code(self, code: str) -> None:
        raise NotImplementedError(
            "Method delete_invitation_code hasn't been implemented yet."
        )
