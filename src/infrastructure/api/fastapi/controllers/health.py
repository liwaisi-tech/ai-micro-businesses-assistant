from fastapi import APIRouter, Depends
from application.services.health_check_service import HealthCheckServiceImpl
from application.usecases.health_check_usecase import HealthCheckUseCase
from application.dtos.health_check_dto import HealthCheckDTO


class HealthController:
    """
    Controller for health check endpoints.
    Provides a simple health check endpoint to verify the service is running.
    """
    
    def __init__(self):
        """
        Initialize the health controller with the necessary dependencies.
        Creates a health check service and injects it into the health check use case.
        """
        self.health_check_service = HealthCheckServiceImpl()
        self.health_check_usecase = HealthCheckUseCase(self.health_check_service)
        self.router = APIRouter(tags=["Health"])
        self._register_routes()
    
    def _register_routes(self):
        """Register all routes related to health checks."""
        self.router.add_api_route(
            path="/health",
            endpoint=self.health_check,
            methods=["GET"],
            response_model=HealthCheckDTO,
            summary="Health Check",
            description="Check if the service is up and running"
        )
    
    async def health_check(self):
        """
        Health check endpoint.
        
        Returns:
            HealthCheckDTO: A DTO containing the health check status and message
        """
        return await self.health_check_usecase.execute()
