import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Site settings
SITE_URL = os.getenv("SITE_URL", "http://localhost:8000")
SITE_NAME = os.getenv("SITE_NAME", "AI Micro-Businesses Assistant")

# API settings
API_PREFIX = os.getenv("API_PREFIX", "ai-business-assistant/api/v1")

# Database settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "business_assistant_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

# Toolbox settings
TOOLBOX_BASE_URL = os.getenv("TOOLBOX_BASE_URL", "http://0.0.0.0:5000")

# Server settings
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))
SERVER_RELOAD = os.getenv("SERVER_RELOAD", "true").lower() == "true"

# Reasoning LLM configuration (for complex reasoning tasks)
REASONING_MODEL = os.getenv("REASONING_MODEL", "google/gemini-2.0-flash-001")
REASONING_BASE_URL = os.getenv("REASONING_BASE_URL", "https://openrouter.ai/api/v1")
REASONING_API_KEY = os.getenv("REASONING_API_KEY", "your_openrouter_api_key")
REASONING_TEMPERATURE = float(os.getenv("REASONING_TEMPERATURE", "0.6"))

# Non-reasoning LLM configuration (for straightforward tasks)
BASIC_MODEL = os.getenv("BASIC_MODEL", "google/gemini-2.0-flash-001")
BASIC_BASE_URL = os.getenv("BASIC_BASE_URL", "https://openrouter.ai/api/v1")
BASIC_API_KEY = os.getenv("BASIC_API_KEY", "your_openrouter_api_key")
BASIC_TEMPERATURE = float(os.getenv("BASIC_TEMPERATURE", "0.6"))

# Vision-language LLM configuration (for tasks requiring visual understanding)
VL_MODEL = os.getenv("VL_MODEL", "google/gemini-2.0-flash-001")
VL_BASE_URL = os.getenv("VL_BASE_URL", "https://openrouter.ai/api/v1")
VL_API_KEY = os.getenv("VL_API_KEY", "your_openrouter_api_key")
VL_TEMPERATURE = float(os.getenv("VL_TEMPERATURE", "0.6"))

# Logging settings
LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO")