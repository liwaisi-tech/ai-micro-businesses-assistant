"""PostgreSQL implementation of the Conversation repository."""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from business_assistant.application.interfaces.repository_interfaces import ConversationRepository
from business_assistant.infrastructure.persistence.connection import execute_query
from business_assistant.infrastructure.persistence.queries.conversation_queries import (
    GET_CONVERSATION_BY_ID,
    GET_CONVERSATION_BY_PHONE,
    CREATE_CONVERSATION,
    UPDATE_CONVERSATION,
    LIST_ALL_CONVERSATIONS,
    DELETE_CONVERSATION,
    GET_MESSAGE_BY_ID,
    CREATE_MESSAGE,
    GET_MESSAGES_BY_CONVERSATION,
    DELETE_MESSAGE,
)

logger = logging.getLogger(__name__)


class PostgresConversationRepository(ConversationRepository):
    """PostgreSQL implementation of the Conversation repository."""

    def get_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation by ID.

        Args:
            entity_id: The ID of the conversation to retrieve.

        Returns:
            The conversation if found, None otherwise.
        """
        try:
            results = execute_query(GET_CONVERSATION_BY_ID, {"id": entity_id})
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error retrieving conversation {entity_id}: {str(e)}")
            return None

    def get_by_phone_number(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """Get conversation by phone number.

        Args:
            phone_number: The WhatsApp phone number to search for.

        Returns:
            The conversation if found, None otherwise.
        """
        try:
            results = execute_query(
                GET_CONVERSATION_BY_PHONE, {"whatsapp_number": phone_number}
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error retrieving conversation for {phone_number}: {str(e)}")
            return None

    def create(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new conversation.

        Args:
            entity_data: The data for the new conversation.

        Returns:
            The created conversation.
        """
        try:
            results = execute_query(
                CREATE_CONVERSATION,
                {
                    "whatsapp_number": entity_data.get("whatsapp_number"),
                    "summary": entity_data.get("summary", ""),
                },
                commit=True,
            )
            return results[0] if results else {}
        except Exception as e:
            logger.error(f"Error creating conversation: {str(e)}")
            raise

    def update(self, entity_id: str, entity_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing conversation.

        Args:
            entity_id: The ID of the conversation to update.
            entity_data: The updated data for the conversation.

        Returns:
            The updated conversation if found, None otherwise.
        """
        try:
            results = execute_query(
                UPDATE_CONVERSATION,
                {
                    "id": entity_id,
                    "end_time": entity_data.get("end_time"),
                    "summary": entity_data.get("summary"),
                },
                commit=True,
            )
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Error updating conversation {entity_id}: {str(e)}")
            return None

    def delete(self, entity_id: str) -> bool:
        """Delete a conversation by ID.

        Args:
            entity_id: The ID of the conversation to delete.

        Returns:
            True if the conversation was deleted, False otherwise.
        """
        try:
            execute_query(DELETE_CONVERSATION, {"id": entity_id}, commit=True)
            return True
        except Exception as e:
            logger.error(f"Error deleting conversation {entity_id}: {str(e)}")
            return False

    def list_all(self) -> List[Dict[str, Any]]:
        """List all conversations.

        Returns:
            A list of all conversations.
        """
        try:
            results = execute_query(LIST_ALL_CONVERSATIONS)
            return results if results else []
        except Exception as e:
            logger.error(f"Error listing conversations: {str(e)}")
            return []

    def add_message(self, conversation_id: str, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a message to a conversation.

        Args:
            conversation_id: The ID of the conversation.
            message_data: The message data to add.

        Returns:
            The added message.
        """
        try:
            results = execute_query(
                CREATE_MESSAGE,
                {
                    "conversation_id": conversation_id,
                    "role": message_data.get("role"),
                    "content": message_data.get("content"),
                },
                commit=True,
            )
            return results[0] if results else {}
        except Exception as e:
            logger.error(f"Error adding message to conversation {conversation_id}: {str(e)}")
            raise

    def get_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a conversation.

        Args:
            conversation_id: The ID of the conversation.

        Returns:
            A list of messages.
        """
        try:
            results = execute_query(
                GET_MESSAGES_BY_CONVERSATION, {"conversation_id": conversation_id}
            )
            return results if results else []
        except Exception as e:
            logger.error(f"Error retrieving messages for conversation {conversation_id}: {str(e)}")
            return []
