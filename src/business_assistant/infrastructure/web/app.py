"""Web application configuration."""
import asyncio
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from business_assistant.interface.api.v1.routes import init_routes
from business_assistant.infrastructure.services.conversation_manager import ConversationManager

logger = logging.getLogger(__name__)

# Background task for cleaning up inactive workflows
async def cleanup_inactive_workflows():
    """Periodically clean up inactive conversation workflows."""
    manager = ConversationManager()
    while True:
        try:
            # Clean up workflows that have been inactive for more than 1 hour
            manager.cleanup_inactive_workflows(max_idle_time=3600)
            logger.debug("Cleaned up inactive workflows")
        except Exception as e:
            logger.error(f"Error cleaning up workflows: {str(e)}")
        # Run every 30 minutes
        await asyncio.sleep(1800)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Start the background task for cleaning up inactive workflows
    cleanup_task = asyncio.create_task(cleanup_inactive_workflows())
    logger.info("Started background task for cleaning up inactive workflows")
    
    yield
    
    # Cancel the background task when shutting down
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        logger.info("Background cleanup task cancelled")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="AI Micro-Businesses Assistant",
        description="AI assistant for micro-businesses that offers various products and services",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Initialize routes
    init_routes(app)
    
    return app
