"""Application settings module."""
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in root directory
root_dir = Path(__file__).resolve().parent.parent.parent.parent
env_path = root_dir / '.env'
load_dotenv(dotenv_path=env_path)


@dataclass
class ServerSettings:
    """Server configuration settings."""
    # Server settings
    host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    port: int = int(os.getenv("SERVER_PORT", "8000"))
    reload: bool = os.getenv("SERVER_RELOAD", "True").lower() in ("true", "t", "yes", "y", "1")
    api_prefix: str = os.getenv("API_PREFIX", "/ai-business-assistant/api/v1")
    
    # OpenRouter settings
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "")
    
    # Site settings
    site_url: str = os.getenv("SITE_URL", "http://localhost:8080")
    site_name: str = os.getenv("SITE_NAME", "AI Micro-Businesses Assistant")
    
    # Database settings
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("POSTGRES_DB", "business_assistant")
    db_user: str = os.getenv("POSTGRES_USER", "postgres")
    db_password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    
    # Toolbox settings
    toolbox_base_url: str = os.getenv("TOOLBOX_BASE_URL", "http://0.0.0.0:5000")

settings = ServerSettings()