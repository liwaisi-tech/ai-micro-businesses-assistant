from application.ports.health_check_port import HealthCheckPort
from application.dtos.health_check_dto import HealthCheckDTO


class HealthCheckUseCase:
    """
    Use case for health check operations.
    This class implements the application logic for health checks.
    """
    
    def __init__(self, health_check_service: HealthCheckPort):
        """
        Initialize the health check use case with a health check service.
        
        Args:
            health_check_service (HealthCheckPort): The service that implements the health check port
        """
        self.health_check_service = health_check_service
    
    async def execute(self) -> HealthCheckDTO:
        """
        Execute the health check use case.
        
        Returns:
            HealthCheckDTO: A DTO containing the health check status and message
        """
        return await self.health_check_service.health_check()
