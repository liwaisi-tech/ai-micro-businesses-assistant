"""API routes initialization."""
from fastapi import APIRouter

from business_assistant.interface.api.v1.routes.health_routes import router as health_router
from business_assistant.interface.api.v1.routes.chat_routes import router as chat_router
from business_assistant.config.settings import settings

def init_routes(app) -> None:
    """Initialize all API routes."""
    api_router = APIRouter(prefix=settings.api_prefix)
    
    # Include all route modules here
    api_router.include_router(health_router)
    api_router.include_router(chat_router)
    
    # Include the main API router in the app
    app.include_router(api_router)
