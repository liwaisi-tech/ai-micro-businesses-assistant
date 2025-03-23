"""
Settings module for the AI Micro-Businesses Assistant.

This module provides centralized configuration management using environment variables
with sensible defaults for development. Uses python-dotenv for loading .env files
and Pydantic for validation and type safety.
"""

from dotenv import load_dotenv
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings

# Load environment variables from .env file if it exists
load_dotenv()


class Settings(BaseSettings):
    """Application settings with validation using Pydantic."""
    
    # Server settings
    SERVER_HOST: str = Field(default="0.0.0.0", description="Host address for the server")
    SERVER_PORT: int = Field(default=8080, description="Port number for the server")
    SERVER_RELOAD: bool = Field(default=True, description="Enable/disable auto-reload")
    
    # Database settings
    DB_HOST: str = Field(
        default="0.0.0.0",
        description="Host address for the database"
    )
    DB_PORT: int = Field(
        default=5432,
        description="Port number for the database"
    )
    POSTGRES_DB: str = Field(
        default="business_assistant_db",
        description="Database name"
    )
    POSTGRES_USER: str = Field(
        default="postgres",
        description="Database username"
    )
    POSTGRES_PASSWORD: str = Field(
        default="postgres",
        description="Database password"
    )
    @property
    def DATABASE_URL(self) -> str:
        """Dynamically build the database URL from components."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
    
    
    # OpenRouter settings
    OPENROUTER_API_KEY: str = Field(
        default="", 
        description="API key for OpenRouter service"
    )
    OPENROUTER_BASE_URL: str = Field(
        default="https://openrouter.ai/api/v1",
        description="Base URL for OpenRouter API"
    )
    OPENROUTER_MODEL: str = Field(
        default="google/gemini-2.0-flash-001",
        description="Model to use with OpenRouter"
    )
    
    # Site information
    SITE_URL: str = Field(
        default="https://liwaisi.tech",
        description="URL for the site, used in API headers"
    )
    SITE_NAME: str = Field(
        default="LiwAIsi - AI Micro-Businesses Assistant",
        description="Name of the site, used in API headers"
    )
    
    # LLM settings
    LLM_TEMPERATURE: float = Field(
        default=0.6,
        description="Temperature for the language model"
    )
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "allow"  # Allow extra fields from environment variables
    }


# Create a singleton instance of the settings
settings = Settings()
