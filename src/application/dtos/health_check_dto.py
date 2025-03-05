from pydantic import BaseModel
    
    
class HealthCheckDTO(BaseModel):
    """
    Data Transfer Object specifically for ping responses.
    Contains information about the service availability.
    """
    status: str
    message: str
