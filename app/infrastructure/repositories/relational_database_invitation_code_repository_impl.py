from sqlmodel import Session, select
from loguru import logger

from app.application.repositories.invitation_code_repository import (
    InvitationCodeRepository,
)
from app.domain.models.invitation_code_model import InvitationCodeModel
from app.infrastructure.configs.sql_database import db_engine
from app.infrastructure.entities.invitation_code_entity import InvitationCode
from app.infrastructure.mappers.invitation_code_mappers import (
    map_invitation_code_entity_to_invitation_code_model,
    map_invitation_code_model_to_invitation_code_entity,
)


class RelationalDatabaseInvitationCodeRepositoryImpl(InvitationCodeRepository):

    def get_invitation_code_by_code(self, code: str) -> InvitationCodeModel | None:
        with Session(db_engine) as session:
            invitation_code_entity = session.exec(
                select(InvitationCode).where(InvitationCode.code == code)
            ).first()

            if invitation_code_entity:
                logger.debug(f"Method get_invitation_code_by_code(), Retrieved invitation code with code: {code}")
                return map_invitation_code_entity_to_invitation_code_model(
                    invitation_code_entity
                )

    def get_invitation_code_by_email(self, email: str) -> InvitationCodeModel | None:
        with Session(db_engine) as session:
            invitation_code_entity = session.exec(
                select(InvitationCode).where(InvitationCode.email == email)
            ).first()

            if invitation_code_entity:
                logger.debug(f"Method get_invitation_code_by_email(), Retrieved invitation code with email: {email}")
                return map_invitation_code_entity_to_invitation_code_model(
                    invitation_code_entity
                )

    def get_invitation_code_by_code_and_email(
        self, code: str, email: str
    ) -> InvitationCodeModel | None:
        with Session(db_engine) as session:
            invitation_code_entity = session.exec(
                select(InvitationCode).where(
                    InvitationCode.code == code, InvitationCode.email == email
                )
            ).first()

            if invitation_code_entity:
                logger.debug(f"Method get_invitation_code_by_code_and_email(), Retrieved invitation code with code {code} and email {email}")
                return map_invitation_code_entity_to_invitation_code_model(
                    invitation_code_entity
                )

    def save_invitation_code(
        self, invitation_code: InvitationCodeModel
    ) -> InvitationCodeModel:
        with Session(db_engine) as session:
            invitation_code_entity = None

            if invitation_code.code:
                invitation_code_entity = session.exec(
                    select(InvitationCode).where(
                        InvitationCode.code == invitation_code.code
                    )
                ).one()

                invitation_code_entity.email = invitation_code.email
            else:
                invitation_code_entity = (
                    map_invitation_code_model_to_invitation_code_entity(invitation_code)
                )

            session.add(invitation_code_entity)
            session.commit()
            session.refresh(invitation_code_entity)
            logger.debug(f"Method save_invitation_code(), Invitation code: {invitation_code_entity.code} saved")
            return map_invitation_code_entity_to_invitation_code_model(
                invitation_code_entity
            )

    def delete_invitation_code_by_code(self, code: str) -> None:
        with Session(db_engine) as session:
            invitation_code_entity = session.exec(
                select(InvitationCode).where(InvitationCode.code == code)
            ).one()

            session.delete(invitation_code_entity)
            session.commit()
            logger.debug(f"Method delete_invitation_code_by_code(), Invitation code with code {code} deleted")
