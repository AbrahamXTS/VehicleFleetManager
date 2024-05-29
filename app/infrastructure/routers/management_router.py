from fastapi import APIRouter, status
from loguru import logger

from app.application.services.metrics_service import MetricsService

from app.infrastructure.repositories.relational_database_driver_assignment_repository_impl import RelationalDatabaseDriverAssignmentRepositoryImpl
from app.infrastructure.repositories.relational_database_driver_repository_impl import RelationalDatabaseDriverRepositoryImpl
from app.infrastructure.repositories.relational_database_user_repository_impl import RelationalDatabaseUserRepositoryImpl
from app.infrastructure.repositories.relational_database_vehicle_repository_impl import RelationalDatabaseVehicleRepositoryImpl


management_router = APIRouter()

@management_router.get("/metrics",status_code=status.HTTP_200_OK)
def get_metrics_information() :
    metrics_service = MetricsService(
        vehicle_repository=RelationalDatabaseVehicleRepositoryImpl(),
        user_repository=RelationalDatabaseUserRepositoryImpl(),
        driver_assignment_repository=RelationalDatabaseDriverAssignmentRepositoryImpl(),
        driver_repository=RelationalDatabaseDriverRepositoryImpl(),
    )
    logger.info("API REQUEST - GET /management/metrics")
    dashboard_metrics = metrics_service.get_metrics()
    logger.success(f"API RESPONSE {status.HTTP_200_OK} - GET /management/metrics")
    return dashboard_metrics
