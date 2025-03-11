"""Health check API models."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    version: str

    model_config = ConfigDict(from_attributes=True)
