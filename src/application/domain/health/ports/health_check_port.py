from abc import ABC, abstractmethod
from application.domain.health.dtos.health_check_dto import HealthCheckDTO


class HealthCheckPort(ABC):
    """
    Port (interface) for the health check service.
    This defines the contract for health check operations.
    """
    
    @abstractmethod
    async def health_check(self) -> HealthCheckDTO:
        """
        Simple health check method that returns a status response.
        
        Returns:
            HealthCheckDTO: A DTO containing the status
        """
        pass
