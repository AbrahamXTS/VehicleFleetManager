from fastapi import APIRouter, status
import logging

from app.application.services.metrics_service import MetricsService

from app.infrastructure.repositories.relational_database_driver_assignment_repository_impl import RelationalDatabaseDriverAssignmentRepositoryImpl
from app.infrastructure.repositories.relational_database_driver_repository_impl import RelationalDatabaseDriverRepositoryImpl
from app.infrastructure.repositories.relational_database_user_repository_impl import RelationalDatabaseUserRepositoryImpl
from app.infrastructure.repositories.relational_database_vehicle_repository_impl import RelationalDatabaseVehicleRepositoryImpl


logger = logging.getLogger(__name__)
management_router = APIRouter()

@management_router.get("/metrics",status_code=status.HTTP_200_OK)
def get_metrics_information() :
    metrics_service = MetricsService(
        vehicle_repository=RelationalDatabaseVehicleRepositoryImpl(),
        user_repository=RelationalDatabaseUserRepositoryImpl(),
        driver_assignment_repository=RelationalDatabaseDriverAssignmentRepositoryImpl(),
        driver_repository=RelationalDatabaseDriverRepositoryImpl(),
    )
    logger.info("GET /management/metrics")
    return metrics_service.get_metrics()
