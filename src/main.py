"""Main application module."""
import logging
import sys

from business_assistant.infrastructure.web.server import run_server, get_application
from business_assistant.infrastructure.persistence.migration import run_migrations

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create app instance for Uvicorn to import when reload=True
app = get_application()

if __name__ == "__main__":
    # Run database migrations before starting the server
    logger.info("Running database migrations...")
    try:
        if run_migrations():
            logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Database migration error: {str(e)}")
        exit(1)
    # Start the server
    run_server()