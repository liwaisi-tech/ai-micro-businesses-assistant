"""Repository interfaces for the application layer."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class BaseRepository(ABC):
    """Base repository interface."""

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get entity by ID.

        Args:
            entity_id: The ID of the entity to retrieve.

        Returns:
            The entity if found, None otherwise.
        """
        pass

    @abstractmethod
    def create(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new entity.

        Args:
            entity_data: The data for the new entity.

        Returns:
            The created entity.
        """
        pass

    @abstractmethod
    def update(self, entity_id: str, entity_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing entity.

        Args:
            entity_id: The ID of the entity to update.
            entity_data: The updated data for the entity.

        Returns:
            The updated entity if found, None otherwise.
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete an entity by ID.

        Args:
            entity_id: The ID of the entity to delete.

        Returns:
            True if the entity was deleted, False otherwise.
        """
        pass

    @abstractmethod
    def list_all(self) -> List[Dict[str, Any]]:
        """List all entities.

        Returns:
            A list of all entities.
        """
        pass


class ConversationRepository(BaseRepository):
    """Conversation repository interface."""

    @abstractmethod
    def get_by_phone_number(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """Get conversation by phone number.

        Args:
            phone_number: The WhatsApp phone number to search for.

        Returns:
            The conversation if found, None otherwise.
        """
        pass

    @abstractmethod
    def add_message(self, conversation_id: str, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a message to a conversation.

        Args:
            conversation_id: The ID of the conversation.
            message_data: The message data to add.

        Returns:
            The added message.
        """
        pass

    @abstractmethod
    def get_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a conversation.

        Args:
            conversation_id: The ID of the conversation.

        Returns:
            A list of messages.
        """
        pass
