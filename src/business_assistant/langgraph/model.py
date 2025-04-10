from langchain_openai import ChatOpenAI
from langchain_core.language_models import BaseLanguageModel
from business_assistant.config.env import settings


def get_basic_model()-> BaseLanguageModel:
    return ChatOpenAI(
        model_name=settings.BASIC_MODEL,
        base_url=settings.BASIC_BASE_URL,
        api_key=settings.BASIC_API_KEY,
        temperature=settings.BASIC_TEMPERATURE,
        default_headers = {
            "HTTP-Referer": settings.SITE_URL,
            "X-Title": settings.SITE_NAME,
        },
    )