"""Web application configuration."""
from fastapi import FastAPI

from business_assistant.interface.api.v1.routes import init_routes

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="AI Micro-Businesses Assistant",
        description="AI assistant for micro-businesses that offers various products and services",
        version="1.0.0"
    )
    
    # Initialize routes
    init_routes(app)
    
    return app
