"""
Environment configuration module using pydantic and python-dotenv.

This module provides a centralized configuration system for the application,
loading values from environment variables with sensible defaults.
"""
from pathlib import Path
from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file if it exists
env_path = Path(__file__).parents[3] / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """Application settings loaded from environment variables with defaults."""
    
    # Site settings
    SITE_URL: str = Field(default="http://localhost:8000", description="Base URL for the site")
    SITE_NAME: str = Field(default="AI Micro-Businesses Assistant", description="Name of the site")
    
    # Server settings
    SERVER_HOST: str = Field(default="0.0.0.0", description="Host to bind the server to")
    SERVER_PORT: int = Field(default=8080, description="Port to bind the server to")
    SERVER_RELOAD: bool = Field(default=True, description="Whether to enable auto-reload")
    
    # API settings
    API_PREFIX: str = Field(default="ai-business-assistant/api/v1", description="API route prefix")
    
    # Reasoning LLM configuration (for complex reasoning tasks)
    REASONING_MODEL: str = Field(default="", description="Model to use for complex reasoning tasks")
    REASONING_BASE_URL: str = Field(default="https://openrouter.ai/api/v1", description="Base URL for reasoning LLM API")
    REASONING_API_KEY: str = Field(default="", description="API key for reasoning LLM")
    REASONING_TEMPERATURE: float = Field(default=0.6, description="Temperature for reasoning LLM generation")
    
    # Basic LLM configuration (for straightforward tasks)
    BASIC_MODEL: str = Field(default="", description="Model to use for basic tasks")
    BASIC_BASE_URL: str = Field(default="https://openrouter.ai/api/v1", description="Base URL for basic LLM API")
    BASIC_API_KEY: str = Field(default="", description="API key for basic LLM")
    BASIC_TEMPERATURE: float = Field(default=0.6, description="Temperature for basic LLM generation")
    
    # Vision-language LLM configuration (for tasks requiring visual understanding)
    VL_MODEL: str = Field(default="", description="Model to use for vision-language tasks")
    VL_BASE_URL: str = Field(default="https://openrouter.ai/api/v1", description="Base URL for vision-language LLM API")
    VL_API_KEY: str = Field(default="", description="API key for vision-language LLM")
    VL_TEMPERATURE: float = Field(default=0.6, description="Temperature for vision-language LLM generation")
    
    # Legacy OpenRouter settings (for backward compatibility)
    OPENROUTER_API_KEY: str = Field(default="", description="API key for OpenRouter (legacy)")
    OPENROUTER_BASE_URL: str = Field(default="https://openrouter.ai/api/v1", description="Base URL for OpenRouter API (legacy)")
    OPENROUTER_MODEL: str = Field(default="", description="Model to use with OpenRouter (legacy)")
    
    # Database settings
    DB_HOST: str = Field(default="localhost", description="Database host")
    DB_PORT: int = Field(default=5432, description="Database port")
    POSTGRES_DB: str = Field(default="business_assistant_db", description="Database name")
    POSTGRES_USER: str = Field(default="postgres", description="Database user")
    POSTGRES_PASSWORD: str = Field(default="postgres", description="Database password")
    
    # Toolbox settings
    TOOLBOX_BASE_URL: str = Field(default="http://0.0.0.0:5000", description="Base URL for the toolbox service")
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    # Google Gen AI settings
    GOOGLE_GEN_AI_API_KEY: str = Field(default="", description="API key for Google Gen AI")
    
    @computed_field
    def DATABASE_URL(self) -> PostgresDsn:
        """Construct the database URL from individual components."""
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f"/{self.POSTGRES_DB}",
        )
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow",
        "case_sensitive": True,
    }


# Create a singleton instance of Settings
settings = Settings()