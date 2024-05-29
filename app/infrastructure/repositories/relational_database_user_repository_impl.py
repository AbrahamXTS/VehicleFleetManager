from sqlmodel import Session, select
from loguru import logger

from app.application.repositories.user_repository import UserRepository
from app.domain.models.invitation_code_model import InvitationCodeModel
from app.domain.models.user_model import UserModel
from app.infrastructure.configs.sql_database import db_engine
from app.infrastructure.entities.user_entity import User
from app.infrastructure.mappers.invitation_code_mappers import (
    map_invitation_code_entity_to_invitation_code_model,
)
from app.infrastructure.mappers.user_mappers import (
    map_user_entity_to_user_model,
    map_user_model_to_user_entity,
)


class RelationalDatabaseUserRepositoryImpl(UserRepository):

    def get_user_by_email(self, email: str) -> UserModel | None:
        with Session(db_engine) as session:
            user_entity = session.exec(select(User).where(User.email == email)).first()

            if user_entity:
                logger.debug(
                    f"Method get_user_by_email(), User with email {email} found"
                )
                return map_user_entity_to_user_model(user_entity)

    def get_all_users(self) -> list[UserModel]:
        users = []

        with Session(db_engine) as session:
            for user_entity in session.exec(select(User)).all():
                users.append(map_user_entity_to_user_model(user_entity))
        logger.debug(f"Method get_all_users(), Retrieved {len(users)} users")
        return users

    def get_invitation_codes_created_by_user_id(
        self, user_id: int
    ) -> list[InvitationCodeModel]:
        invitation_codes = []

        with Session(db_engine) as session:
            for invitation_code_entity in (
                session.exec(select(User).where(User.id == user_id))
                .one()
                .invitation_codes
            ):
                invitation_codes.append(
                    map_invitation_code_entity_to_invitation_code_model(
                        invitation_code_entity
                    )
                )

        logger.debug(
            f"Method get_invitation_codes_created_by_user_id(), Retrieved invitation codes for {user_id}"
        )
        return invitation_codes

    def save_user(self, user: UserModel) -> UserModel:
        with Session(db_engine) as session:
            user_entity = None

            if user.id:
                user_entity = session.exec(select(User).where(User.id == user.id)).one()

                user_entity.email = user.email
                user_entity.last_name = user.last_name
                user_entity.name = user.name
                user_entity.password = user.password
            else:
                user_entity = map_user_model_to_user_entity(user)

            session.add(user_entity)
            session.commit()
            session.refresh(user_entity)
            logger.debug(
                f"Method save_user(), User saved: {user.name} {user.last_name}"
            )
            return map_user_entity_to_user_model(user_entity)

    def delete_user_by_user_id(self, user_id: int) -> None:
        with Session(db_engine) as session:
            user_entity = session.exec(select(User).where(User.id == user_id)).one()

            session.delete(user_entity)
            session.commit()
            logger.debug("Method delete_user_by_user_id()")

    def get_number_of_users(self) -> int:
        with Session(db_engine) as session:
            number_users = len(session.exec(select(User)).all())
        logger.debug(f"Method get_number_of_users(), Retrieved {number_users} users")
        return number_users
