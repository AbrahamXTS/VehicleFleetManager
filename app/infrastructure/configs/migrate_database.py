# Run this file to migrate tables to the database on development

from sqlmodel import SQLModel

from app.infrastructure.configs.sql_database import db_engine

# Import here one by one of the entities that you want to create within the database
from app.infrastructure.entities.driver_entity import Driver # noqa: F401
from app.infrastructure.entities.driver_assignment_entity import DriverAssignment # noqa: F401
from app.infrastructure.entities.invitation_code_entity import InvitationCode # noqa: F401
from app.infrastructure.entities.user_entity import User # noqa: F401
from app.infrastructure.entities.vehicle_entity import Vehicle # noqa: F401

if __name__ == "__main__":
    SQLModel.metadata.create_all(db_engine)
