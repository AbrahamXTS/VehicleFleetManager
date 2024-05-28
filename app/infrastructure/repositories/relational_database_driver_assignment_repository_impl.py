from datetime import date
from pymysql import IntegrityError
from sqlmodel import Session, select, or_
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from app.domain.models.driver_assignment import (
    DriverAssignmentModel,
    LocationModel,
    DriverAssignmentIdModel,
)
from app.infrastructure.configs.sql_database import db_engine
import logging

from app.application.repositories.driver_assingment_repository import (
    DriverAssignmentRepository,
)
from app.infrastructure.entities.driver_assignment_entity import DriverAssignment
from app.infrastructure.mappers.driver_assignment_mappers import (
    map_driver_assignment_entity_to_driver_assignment_model,
    map_driver_assignment_model_to_driver_assignment_entity,
)


class RelationalDatabaseDriverAssignmentRepositoryImpl(DriverAssignmentRepository):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def assign_driver_to_vehicle(self, driver_assignment: DriverAssignmentModel) -> DriverAssignmentModel:
        self.logger.info("Method assign_driver_to_vehicle()")
        with Session(db_engine) as session:
            driver_assignment_entity = (
                map_driver_assignment_model_to_driver_assignment_entity(
                    driver_assignment
                )
            )
            session.add(driver_assignment_entity)
            try:
                session.commit()
                self.logger.debug(f"Driver {driver_assignment.driver_id} assigned to vehicle {driver_assignment.vehicle_id} on {driver_assignment.travel_date}")
            except IntegrityError:
                session.rollback()
                self.logger.warning(f"Driver {driver_assignment.driver_id} already assigned to vehicle {driver_assignment.vehicle_id} on {driver_assignment.travel_date}")
                raise ResourceNotFoundException("Driver or vehicle to assign not found")
            else:
                session.refresh(driver_assignment_entity)
            return map_driver_assignment_entity_to_driver_assignment_model(
                driver_assignment_entity
            )

    def get_driver_assignments(self, only_actives: bool, travel_date: date | None) -> list[DriverAssignmentModel]:
        self.logger.info("Method get_driver_assignments()")
        with Session(db_engine) as session:
            statement = select(DriverAssignment)
            if travel_date:
                statement = statement.where(DriverAssignment.travel_date == travel_date)
            if only_actives:
                statement = statement.where(DriverAssignment.active)
            driver_assignment_entities = session.exec(
                statement.order_by(
                    DriverAssignment.travel_date.desc(),
                    DriverAssignment.creation_date.desc(),
                )
            ).all()
            self.logger.debug(f"Driver assignments: {driver_assignment_entities}")
            return [
                map_driver_assignment_entity_to_driver_assignment_model(
                    driver_assignment_entity
                )
                for driver_assignment_entity in driver_assignment_entities
            ]

    def get_driver_assignment(
        self, driver_id: int, vehicle_id: int, travel_date: date
    ) -> DriverAssignmentModel:
        self.logger.info(f"Method get_driver_assignment(), Getting driver assignment for driver {driver_id} and vehicle {vehicle_id} on {travel_date}")
        with Session(db_engine) as session:
            driver_assignment_entity = session.get(
                DriverAssignment, (driver_id, vehicle_id, travel_date)
            )
            if driver_assignment_entity:
                self.logger.debug(f"Driver assignment: {driver_assignment_entity}")
                return map_driver_assignment_entity_to_driver_assignment_model(
                    driver_assignment_entity
                )

    def get_active_driver_assignments_with_driver_id_or_vehicle_id_at_date(
        self, driver_id: int, vehicle_id: int, travel_date: date
    ) -> list[DriverAssignmentModel]:
        with Session(db_engine) as session:
            self.logger.info(f"Method get_active_driver_assignments_with_driver_id_or_vehicle_id_at_date(), Getting active driver assignments for driver {driver_id} or vehicle {vehicle_id} on {travel_date}")
            driver_assignment_entities = session.exec(
                select(DriverAssignment).where(
                    or_(
                        DriverAssignment.driver_id == driver_id,
                        DriverAssignment.vehicle_id == vehicle_id,
                    ),
                    DriverAssignment.travel_date == travel_date,
                    DriverAssignment.active,
                )
            ).all()
            self.logger.debug(f"Driver assignments: {driver_assignment_entities}")
        return [
            map_driver_assignment_entity_to_driver_assignment_model(driver_assignment_entity)
            for driver_assignment_entity in driver_assignment_entities
        ]

    def get_active_driver_assignment_by_destination_location_at_date(
        self,
        location: LocationModel,
        travel_date: date,
        exclude_assignment: DriverAssignmentIdModel,
    ) -> DriverAssignmentModel:
        self.logger.info(f"Method get_active_driver_assignment_by_destination_location_at_date(), Getting active driver assignment by destination location {location} on {travel_date}")
        with Session(db_engine) as session:
            statement = select(DriverAssignment).where(
                DriverAssignment.destination_location_latitude == location.latitude,
                DriverAssignment.destination_location_longitude == location.longitude,
                DriverAssignment.travel_date == travel_date,
                DriverAssignment.active,
            )
            if exclude_assignment:
                statement = statement.where(
                    DriverAssignment.driver_id != exclude_assignment.driver_id,
                    DriverAssignment.vehicle_id != exclude_assignment.vehicle_id,
                )
            driver_assignment_entity = session.exec(statement).first()
        if driver_assignment_entity:
            self.logger.debug(f"Driver assignment: {driver_assignment_entity}")
            return map_driver_assignment_entity_to_driver_assignment_model(driver_assignment_entity)

    def update_driver_assignment(self, driver_assignment: DriverAssignmentModel) -> DriverAssignmentModel:
        self.logger.info(f"Method update_driver_assignment(), Updating driver assignment for driver {driver_assignment.driver_id} and vehicle {driver_assignment.vehicle_id} on {driver_assignment.travel_date}")
        with Session(db_engine) as session:
            driver_assignment_entity = session.get(
                DriverAssignment,
                (
                    driver_assignment.driver_id,
                    driver_assignment.vehicle_id,
                    driver_assignment.travel_date,
                ),
            )
            if driver_assignment_entity:
                driver_assignment_entity.route_name = driver_assignment.route_name
                driver_assignment_entity.origin_location_latitude = (
                    driver_assignment.origin_location.latitude
                )
                driver_assignment_entity.origin_location_longitude = (
                    driver_assignment.origin_location.longitude
                )
                driver_assignment_entity.destination_location_latitude = (
                    driver_assignment.destination_location.latitude
                )
                driver_assignment_entity.destination_location_longitude = (
                    driver_assignment.destination_location.longitude
                )
                driver_assignment_entity.completed_successfully = (
                    driver_assignment.completed_successfully
                )
                driver_assignment_entity.problem_description = (
                    driver_assignment.problem_description
                )
                driver_assignment_entity.comments = driver_assignment.comments
                session.add(driver_assignment_entity)
                session.commit()
                session.refresh(driver_assignment_entity)
                self.logger.debug(f"Driver assignment updated: {driver_assignment_entity}")
        if driver_assignment_entity:
            return map_driver_assignment_entity_to_driver_assignment_model(driver_assignment_entity)
        
    def set_driver_assignment_as_inactive(self, driver_id: int, vehicle_id: int, travel_date: date) -> None:
        self.logger.info(f"Method set_driver_assignment_as_inactive(), Setting driver assignment as inactive for driver {driver_id} and vehicle {vehicle_id} on {travel_date}")
        with Session(db_engine) as session:
            driver_assignment_entity = session.get(
                DriverAssignment, (driver_id, vehicle_id, travel_date)
            )
            if driver_assignment_entity:
                driver_assignment_entity.active = False
                session.commit()
                self.logger.debug(f"Driver assignment set as inactive: {driver_assignment_entity}")

    def get_all_assignments_for_driver(self, driver_id: int) -> list[DriverAssignmentModel]:
        self.logger.info(f"Method get_all_assignments_for_driver(), Getting all assignments for driver {driver_id}")
        with Session(db_engine) as session:
            driver_assignment_entities = session.exec(
                select(DriverAssignment).where(DriverAssignment.driver_id == driver_id)
            ).all()
            self.logger.debug(f"Driver assignments: {driver_assignment_entities}")
        return [
            map_driver_assignment_entity_to_driver_assignment_model(driver_assignment_entity)
            for driver_assignment_entity in driver_assignment_entities
            ]

    def get_all_assignments_for_vehicle(self, vehicle_id: int) -> list[DriverAssignmentModel]:
        self.logger.info(f"Method get_all_assignments_for_vehicle(), Getting all assignments for vehicle {vehicle_id}")
        with Session(db_engine) as session:
            driver_assignment_entities = session.exec(
                select(DriverAssignment).where(
                    DriverAssignment.vehicle_id == vehicle_id
                )
            ).all()
            self.logger.debug(f"Driver assignments: {driver_assignment_entities}")
        return [
            map_driver_assignment_entity_to_driver_assignment_model(driver_assignment_entity)
            for driver_assignment_entity in driver_assignment_entities
        ]
    
    def get_number_of_today_assignments(self) -> int:
        self.logger.info("Method get_number_of_today_assignments(), Getting number of assignments for today")
        today = date.today()  
        formatted_date = today.strftime("%Y-%m-%d") 
        with Session(db_engine) as session:
            number_of_assignments = len(session.exec(
                select(DriverAssignment).where(DriverAssignment.travel_date == formatted_date)).all())
            self.logger.debug(f"Retrieved {number_of_assignments} assignments for today")
        return number_of_assignments
