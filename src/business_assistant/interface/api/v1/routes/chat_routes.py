"""Chat routes implementation."""
from typing import Dict
from fastapi import APIRouter, Depends, Header, HTTPException
from business_assistant.application.services.chat_service import ChatService
from business_assistant.interface.api.v1.models.chat_models import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request - Invalid WhatsApp number"}
    },
)

# Store chat services per user
_chat_services: Dict[str, ChatService] = {}

def get_chat_service(whatsapp_number: str = Header(..., description="User's WhatsApp number in international format (e.g., +573658425187)", alias="whatsapp-number")):
    """Dependency injection for chat service.
    
    Args:
        whatsapp_number: User's WhatsApp number as identifier.
        
    Returns:
        ChatService instance for the user.
        
    Raises:
        HTTPException: If WhatsApp number format is invalid.
    """
    # Validate WhatsApp number format
    if not whatsapp_number.startswith('+') or not whatsapp_number[1:].isdigit():
        raise HTTPException(
            status_code=400,
            detail="Invalid WhatsApp number format. Must start with + followed by digits."
        )
    
    # Get or create chat service for user
    if whatsapp_number not in _chat_services:
        _chat_services[whatsapp_number] = ChatService()
    
    return _chat_services[whatsapp_number]

@router.post("/message", response_model=ChatResponse)
async def process_message(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
) -> ChatResponse:
    """Process a chat message.
    
    Args:
        request: The chat request containing the message.
        chat_service: The chat service instance for the user.
        
    Returns:
        ChatResponse containing the assistant's response.
    """
    response = chat_service.process_message(request.message)
    
    return ChatResponse(response=response)
