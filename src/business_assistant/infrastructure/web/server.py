"""Server configuration module."""
import uvicorn
from fastapi import FastAPI

from business_assistant.config.settings import ServerSettings
from business_assistant.infrastructure.web.app import create_app


def get_application() -> FastAPI:
    """Get the FastAPI application instance."""
    return create_app()


def run_server() -> None:
    """Run the Uvicorn server with the FastAPI application."""
    settings = ServerSettings()
    
    if settings.reload:
        # When reload is enabled, we need to use import string
        uvicorn.run(
            "src.main:app",
            host=settings.host,
            port=settings.port,
            reload=settings.reload
        )
    else:
        # When reload is disabled, we can pass the app instance directly
        app = get_application()
        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            reload=settings.reload
        )
