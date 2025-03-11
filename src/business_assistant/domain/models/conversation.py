"""Conversation domain model."""
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Message:
    """Message model for conversations."""
    role: str
    content: str

    def to_dict(self) -> Dict:
        """Convert message to dictionary format."""
        return {
            "role": self.role,
            "content": self.content
        }


@dataclass
class Conversation:
    """Conversation model."""
    messages: List[Message]

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)

    def get_messages_as_dicts(self) -> List[Dict]:
        """Get messages as list of dictionaries."""
        return [message.to_dict() for message in self.messages]
