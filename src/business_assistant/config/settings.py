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
    host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    port: int = int(os.getenv("SERVER_PORT", "8000"))
    reload: bool = bool(os.getenv("SERVER_RELOAD", "True"))
    api_prefix: str = os.getenv("API_PREFIX", "/ai-business-assistant/api/v1")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_base_url: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "")
    site_url: str = os.getenv("SITE_URL", "http://localhost:8000")
    site_name: str = os.getenv("SITE_NAME", "AI Micro-Businesses Assistant")

settings = ServerSettings()