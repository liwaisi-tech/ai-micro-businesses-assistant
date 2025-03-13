"""Conversation service implementation."""

from typing import List, Optional, Dict, Any

from business_assistant.domain.models.conversation import Message, Conversation
from business_assistant.application.interfaces.repository_interfaces import ConversationRepository
from business_assistant.infrastructure.persistence.repositories.conversation_repository import PostgresConversationRepository


class ConversationService:
    """Service for managing conversation persistence."""

    def __init__(self):
        """Initialize the conversation service."""
        self.repository: ConversationRepository = PostgresConversationRepository()
        self.conversation = Conversation()

    def get_or_create_conversation(self, whatsapp_number: str) -> Dict[str, Any]:
        """Get an existing conversation or create a new one.

        Args:
            whatsapp_number: The WhatsApp number of the user.

        Returns:
            The conversation data.
        """
        conversation = self.repository.get_by_phone_number(whatsapp_number)
        
        if not conversation:
            conversation = self.repository.create({
                "whatsapp_number": whatsapp_number,
                "summary": "Nueva conversación"
            })
            
        return conversation

    def add_message(self, whatsapp_number: str, message: Message) -> Dict[str, Any]:
        """Add a message to a conversation.

        Args:
            whatsapp_number: The WhatsApp number of the user.
            message: The message to add.

        Returns:
            The added message data.
        """
        # Add to in-memory conversation
        self.conversation.add_message(whatsapp_number, message)
        
        # Add to database
        conversation = self.get_or_create_conversation(whatsapp_number)
        
        message_data = {
            "role": message.role,
            "content": message.content
        }
        
        return self.repository.add_message(conversation["id"], message_data)

    def get_conversation_history(self, whatsapp_number: str) -> List[Dict[str, Any]]:
        """Get the conversation history for a user.

        Args:
            whatsapp_number: The WhatsApp number of the user.

        Returns:
            List of messages in the conversation.
        """
        conversation = self.repository.get_by_phone_number(whatsapp_number)
        
        if not conversation:
            return []
            
        return self.repository.get_messages(conversation["id"])
