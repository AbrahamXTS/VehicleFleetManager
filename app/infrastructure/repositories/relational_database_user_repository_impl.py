from sqlmodel import Session, select

from app.domain.models.user_model import UserModel
from app.application.repositories.user_repository import UserRepository

from ..configs.sql_database import db_engine
from ..mappers.user_mappers import (
    map_user_entity_to_user_model,
    map_user_model_to_user_entity,
)
from ..entities.user_entity import User


class RelationalDatabaseUserRepositoryImpl(UserRepository):
    def get_user_by_email(self, email: str) -> UserModel | None:
        with Session(db_engine) as session:
            user_entity = session.exec(select(User).where(User.email == email)).first()

            if user_entity:
                return map_user_entity_to_user_model(user_entity)

    def get_all_users(self) -> list[UserModel]:
        users = []

        with Session(db_engine) as session:
            for user_entity in session.exec(select(User)).all():
                users.append(map_user_entity_to_user_model(user_entity))

        return users

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

            return map_user_entity_to_user_model(user_entity)

    def delete_user(self, id: int) -> None:
        with Session(db_engine) as session:
            user_entity = session.exec(select(User).where(User.id == id)).one()

            session.delete(user_entity)
            session.commit()
