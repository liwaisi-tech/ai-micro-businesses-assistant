from abc import ABC, abstractmethod
from typing import Any


class AgentPort(ABC):
    """Interface for AI agent interactions."""
    
    @abstractmethod
    async def ask_to_agent(self, message: str) -> Any:
        """
        Send a message to the agent and get its response.
        
        Args:
            message (str): The message to send to the agent
            
        Returns:
            Any: The agent's response
        """
        pass
    
    @abstractmethod
    async def clear_conversation(self) -> None:
        """
        Clear the current conversation history with the agent.
        """
        pass
