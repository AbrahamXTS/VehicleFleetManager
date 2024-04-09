# Run this file to migrate tables to the database on development

from sqlmodel import SQLModel

from app.infrastructure.configs.sql_database import db_engine

# Import here one by one of the entities that you want to create within the database
from app.infrastructure.entities.invitation_code_entity import InvitationCode
from app.infrastructure.entities.user_entity import User
from app.infrastructure.entities.vehicle_entity import Vehicle
from app.infrastructure.entities.driver_entity import Driver
from app.infrastructure.entities.driver_assignment_entity import DriverAssignment

if __name__ == "__main__":
    SQLModel.metadata.create_all(db_engine)
