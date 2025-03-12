"""Chat service implementation."""

from business_assistant.domain.models.conversation import Message, Conversation
from business_assistant.infrastructure.langgraph.workflows.conversation_workflow import (
    ConversationWorkflow,
)
from business_assistant.config.settings import settings


class ChatService:
    """Service for managing chat interactions."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        """Initialize the chat service.

        Args:
            model: The model to use for the chatbot.
        """
        self.workflow = ConversationWorkflow(settings.openrouter_model)
        self.conversation = Conversation()

    def process_message(self, phone_number: str, user_message: str) -> str:
        """Process a user message and get the assistant's response.

        Args:
            user_message: The message from the user.

        Returns:
            The assistant's response.
        """
        # Create and add user message to conversation
        message = Message(role="user", content=user_message)
        self.conversation.add_message(phone_number, message)

        # Process through workflow
        response = self.workflow.process_message(user_message)

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
