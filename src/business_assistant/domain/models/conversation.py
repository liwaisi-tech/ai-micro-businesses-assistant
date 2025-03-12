"""Conversation domain model."""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Message:
    """Message model for conversations."""

    role: str
    content: str

    def to_dict(self) -> Dict:
        """Convert message to dictionary format."""
        return {"role": self.role, "content": self.content}


@dataclass
class Conversation:
    """Conversation model that maintains separate conversations by phone number."""

    conversations: Dict[str, List[Message]] = field(default_factory=dict)

    def add_message(self, phone_number: str, message: Message) -> None:
        """Add a message to the conversation for a specific phone number."""
        if phone_number not in self.conversations:
            self.conversations[phone_number] = []
        self.conversations[phone_number].append(message)

    def get_messages_as_dicts(self, phone_number: str) -> List[Dict]:
        """Get messages as list of dictionaries for a specific phone number."""
        if phone_number not in self.conversations:
            return []
        return [message.to_dict() for message in self.conversations[phone_number]]

    def get_all_conversations(self) -> Dict[str, List[Dict]]:
        """Get all conversations as a dictionary mapping phone numbers to message lists."""
        return {
            phone: [message.to_dict() for message in messages]
            for phone, messages in self.conversations.items()
        }


class ConversationManager:
    """Manager to handle multiple conversations by phone number."""

    def __init__(self):
        """Initialize an empty conversation manager."""
        self.conversations: Dict[str, Conversation] = {}

    def get_conversation(self, phone_number: str) -> Conversation:
        """Get or create a conversation by phone number."""
        if phone_number not in self.conversations:
            # Create a new conversation if it doesn't exist
            self.conversations[phone_number] = Conversation()
        return self.conversations[phone_number]

    def add_message(self, phone_number: str, message: Message) -> None:
        """Add a message to the conversation for a given phone number."""
        conversation = self.get_conversation(phone_number)
        conversation.add_message(phone_number, message)

    def get_messages(self, phone_number: str) -> List[Dict]:
        """Get all messages for a given phone number."""
        conversation = self.get_conversation(phone_number)
        return conversation.get_messages_as_dicts(phone_number)
