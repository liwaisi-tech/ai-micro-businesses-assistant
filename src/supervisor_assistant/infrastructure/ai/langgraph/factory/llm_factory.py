"""
LLM Factory module for the AI Micro-Businesses Assistant.

This module provides a factory service for creating language model instances
with consistent configuration across the application.
"""

from typing import Optional

from langchain_openai import ChatOpenAI

# Import settings
from config.settings import settings


class LLMFactory:
    """Factory service for creating language model instances."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'LLMFactory':
        """
        Get or create the singleton instance of the factory.
        
        Returns:
            The singleton instance of LLMFactory
        """
        if cls._instance is None:
            cls._instance = LLMFactory()
        return cls._instance
    
    def create_openai_llm(
        self,
        temperature: float = 0.6,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> ChatOpenAI:
        """
        Create a ChatOpenAI instance with consistent configuration.
        
        Args:
            temperature: The temperature for the model (controls randomness)
            model_name: Optional override for the model name
            api_key: Optional override for the API key
            base_url: Optional override for the base URL
            
        Returns:
            A configured ChatOpenAI instance
        """
        return ChatOpenAI(
            model_name=model_name or settings.OPENROUTER_MODEL,
            base_url=base_url or settings.OPENROUTER_BASE_URL,
            api_key=api_key or settings.OPENROUTER_API_KEY,
            default_headers={
                "HTTP-Referer": settings.SITE_URL,
                "X-Title": settings.SITE_NAME,
            },
            temperature=temperature
        )


# Create a singleton instance of the factory
llm_factory = LLMFactory.get_instance()
