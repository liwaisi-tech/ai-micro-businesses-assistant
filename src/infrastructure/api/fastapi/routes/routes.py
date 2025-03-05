from fastapi import APIRouter
from infrastructure.api.fastapi.controllers.health import HealthController

def register_routes(app):
    """
    Register all API routes with the FastAPI application.
    
    Args:
        app: The FastAPI application instance
    """
    # Initialize controllers
    health_controller = HealthController()
    
    # Create main API router
    api_router = APIRouter()
    
    # Include controller routers
    api_router.include_router(health_controller.router)
    
    # Include the main API router in the app
    app.include_router(api_router, prefix="")
