"""Health check routes."""
from fastapi import APIRouter

from business_assistant.application.services.health_service import HealthService
from business_assistant.interface.api.v1.models.health_models import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    health_status = HealthService.get_health_status()
    return health_status
