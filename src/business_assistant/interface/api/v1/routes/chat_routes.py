"""Chat routes implementation."""

from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from business_assistant.application.services.chat_service import ChatService
from business_assistant.interface.api.v1.models.chat_models import (
    ChatRequest,
    ChatResponse,
)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request - Invalid WhatsApp number"},
    },
)


def get_chat_service():
    """Dependency injection for chat service.

    Returns:
        ChatService instance for the user.
    """
    return ChatService()


@router.post("/message", response_model=ChatResponse)
async def process_message(
    request: ChatRequest, chat_service: ChatService = Depends(get_chat_service, use_cache=False)
) -> ChatResponse:
    """Process a chat message.

    Args:
        request: The chat request containing the message.
        chat_service: The chat service instance for the user.

    Returns:
        ChatResponse containing the assistant's response.
    """
    print('initiating endpoint call')
    
    # Validate WhatsApp number format
    if not request.whatsapp_number.startswith("+") or not request.whatsapp_number[1:].isdigit():
        raise HTTPException(
            status_code=400,
            detail="Invalid WhatsApp number format. Must start with + followed by digits.",
        )
        
    response = chat_service.process_message(request.whatsapp_number, request.message)

    return ChatResponse(response=response)
