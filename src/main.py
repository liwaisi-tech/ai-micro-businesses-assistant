"""Main application module."""
from business_assistant.infrastructure.web.server import run_server, get_application

# Create app instance for Uvicorn to import when reload=True
app = get_application()

if __name__ == "__main__":
    run_server()