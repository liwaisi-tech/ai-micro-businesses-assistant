"""Chat service implementation with React agent integration."""

import logging
from business_assistant.domain.models.conversation import Message, Conversation
from business_assistant.infrastructure.services.conversation_manager import ConversationManager
from business_assistant.config.settings import settings

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing chat interactions using React agent."""

    def __init__(self):
        """Initialize the chat service with conversation manager.
        """
        # Use the singleton conversation manager to get workflows by user ID
        self.conversation_manager = ConversationManager()
        # Keep the conversation model for message history
        self.conversation = Conversation()
        
        logger.debug("ChatService initialized with ConversationManager")

    def process_message(self, phone_number: str, user_message: str) -> str:
        """Process a user message and get the assistant's response using React agent.

        Args:
            phone_number: The WhatsApp number of the user (used as user_id)
            user_message: The message from the user.

        Returns:
            The assistant's response.
        """
        # Create and add user message to conversation
        message = Message(role="user", content=user_message)
        self.conversation.add_message(phone_number, message)

        # Get the appropriate workflow for this user from the manager
        workflow = self.conversation_manager.get_workflow(phone_number)
        logger.debug(f"Retrieved workflow for user {phone_number}")
        
        # Process through workflow with user_id (phone_number)
        response = workflow.process_message(phone_number, user_message)

        # Add assistant response to conversation
        assistant_message = Message(role="assistant", content=response)
        self.conversation.add_message(phone_number, assistant_message)

        return response

    def get_conversation_history(self) -> list:
        """Get the full conversation history.

        Returns:
            List of messages in the conversation.
        """
        return self.conversation.get_messages_as_dicts()
