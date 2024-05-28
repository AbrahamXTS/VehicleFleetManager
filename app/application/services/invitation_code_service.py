from app.application.repositories.invitation_code_repository import (
    InvitationCodeRepository,
)
from app.application.repositories.user_repository import UserRepository
from app.domain.exceptions.conflict_with_existing_resource_exception import (
    ConflictWithExistingResourceException,
)
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.domain.models.invitation_code_model import InvitationCodeModel
import logging

class InvitationCodeService:
    def __init__(
        self,
        invitation_code_repository: InvitationCodeRepository,
        user_repository: UserRepository,
    ) -> None:
        self.invitation_code_repository = invitation_code_repository
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    def get_all_invitation_codes_by_user_id(
        self, user_id: int
    ) -> list[InvitationCodeModel]:
        self.logger.info("Method get_all_invitation_codes_by_user_id()")
        return self.user_repository.get_invitation_codes_created_by_user_id(user_id)

    def create_invitation_code(
        self, recipient_email: str, authenticated_user_id: int
    ) -> InvitationCodeModel:
        self.logger.info("Method create_invitation_code()")
        if self.user_repository.get_user_by_email(
            recipient_email
        ) or self.invitation_code_repository.get_invitation_code_by_email(
            recipient_email
        ):
            self.logger.warning(f"Conflict: User with email {recipient_email} already exists")
            raise ConflictWithExistingResourceException
        self.logger.debug(f"Creating invitation code for email: {recipient_email}")
        return self.invitation_code_repository.save_invitation_code(
            InvitationCodeModel(
                code=None, email=recipient_email, created_by_user=authenticated_user_id
            )
        )

    def update_recipient_email_from_invitation_code(
        self, code: str, recipient_email: str, authenticated_user_id: int
    ) -> InvitationCodeModel:
        self.logger.info("Method update_recipient_email_from_invitation_code()")
        if code not in [
            invitation_code.code
            for invitation_code in self.user_repository.get_invitation_codes_created_by_user_id(
                authenticated_user_id
            )
        ]:
            self.logger.warning(f"Invitation code with code {code} not found")
            raise ResourceNotFoundException

        if self.user_repository.get_user_by_email(
            recipient_email
        ) or self.invitation_code_repository.get_invitation_code_by_email(
            recipient_email
        ):
            self.logger.warning(f"Conflict: User with email {recipient_email} already exists")
            raise ConflictWithExistingResourceException

        self.logger.debug(f"Saving updated invitation code with code: {code}")
        return self.invitation_code_repository.save_invitation_code(
            InvitationCodeModel(
                code=code, email=recipient_email, created_by_user=authenticated_user_id
            )
        )

    def delete_invitation_code_by_code(
        self, code: str, authenticated_user_id: int
    ) -> None:
        self.logger.info("Method delete_invitation_code_by_code()")
        if code not in [
            invitation_code.code
            for invitation_code in self.user_repository.get_invitation_codes_created_by_user_id(
                authenticated_user_id
            )
        ]:
            self.logger.warning(f"Invitation code with code {code} not found")
            raise ResourceNotFoundException

        return self.invitation_code_repository.delete_invitation_code_by_code(code)
