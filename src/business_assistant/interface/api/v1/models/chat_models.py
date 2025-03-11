"""Chat API models."""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., description="Message from the user")


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str = Field(..., description="AI assistant's response")
