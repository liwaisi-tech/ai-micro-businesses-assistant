from application.ports.health_check_port import HealthCheckPort
from application.dtos.health_check_dto import HealthCheckDTO


class HealthCheckServiceImpl(HealthCheckPort):
    """
    Implementation of the HealthCheckService port.
    Provides a simple health check functionality for the application.
    """
    
    async def health_check(self) -> HealthCheckDTO:
        """
        Simple health check method that returns a status response.
        
        Returns:
            HealthCheckResponse: A dictionary containing the status and a message
                                indicating the health of the service.
        """
        return HealthCheckDTO(status="ok", message="Service is up and running")
