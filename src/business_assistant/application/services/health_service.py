"""Health check application service."""
from business_assistant.domain.models.health import HealthStatus


class HealthService:
    """Health check service."""
    
    @staticmethod
    def get_health_status() -> HealthStatus:
        """Get the current health status of the application."""
        return HealthStatus.create_ok_status()
