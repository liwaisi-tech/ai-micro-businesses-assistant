"""Conversation manager service to maintain conversation workflows by user."""

import logging
from typing import Dict
from business_assistant.infrastructure.langgraph.workflows.conversation_workflow import ConversationWorkflow

logger = logging.getLogger(__name__)

class ConversationManager:
    """Singleton service that manages conversation workflows by user ID.
    
    This ensures that conversation context is maintained across multiple API requests
    for the same user (identified by WhatsApp number).
    """
    
    _instance = None
    
    def __new__(cls):
        """Ensure only one instance of ConversationManager exists."""
        if cls._instance is None:
            logger.info("Creating new ConversationManager instance")
            cls._instance = super(ConversationManager, cls).__new__(cls)
            cls._instance._workflows = {}
        return cls._instance
    
    def get_workflow(self, user_id: str) -> ConversationWorkflow:
        """Get or create a conversation workflow for a specific user.
        
        Args:
            user_id: The unique identifier for the user (e.g., WhatsApp number)
            
        Returns:
            A ConversationWorkflow instance for the user
        """
        if user_id not in self._workflows:
            logger.info(f"Creating new ConversationWorkflow for user {user_id}")
            self._workflows[user_id] = ConversationWorkflow()
        return self._workflows[user_id]
    
    def get_all_user_ids(self) -> list:
        """Get a list of all user IDs with active workflows.
        
        Returns:
            List of user IDs
        """
        return list(self._workflows.keys())
