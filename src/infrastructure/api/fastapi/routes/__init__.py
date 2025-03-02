from fastapi import APIRouter
from infrastructure.api.fastapi.controllers.health import HealthController


def register_routes() -> APIRouter:
    """
    Register all API routes.
    
    Returns:
        APIRouter: A FastAPI router with all registered routes
    """
    router = APIRouter()
    
    # Initialize controllers
    health_controller = HealthController()
    
    # Include routers from controllers
    router.include_router(health_controller.router)
    
    return router
