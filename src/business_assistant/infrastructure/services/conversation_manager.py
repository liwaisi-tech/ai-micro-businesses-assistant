"""Conversation manager service to maintain conversation workflows by user."""

import logging
import time
from typing import Dict, Optional
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
            cls._instance._last_accessed = {}
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        """Initialize the ConversationManager if not already initialized."""
        if not getattr(self, '_initialized', False):
            logger.info("Initializing ConversationManager")
            self._workflows = {}
            self._last_accessed = {}
            self._initialized = True
    
    def get_workflow(self, user_id: str) -> ConversationWorkflow:
        """Get or create a conversation workflow for a specific user.
        
        Args:
            user_id: The unique identifier for the user (e.g., WhatsApp number)
            
        Returns:
            A ConversationWorkflow instance for the user
        """
        # Update last accessed time for this user
        self._last_accessed[user_id] = time.time()
        
        if user_id not in self._workflows:
            logger.info(f"Creating new ConversationWorkflow for user {user_id}")
            workflow = ConversationWorkflow()
            
            # The workflow will automatically attempt to restore state from PostgreSQL
            # during its first process_message call
            self._workflows[user_id] = workflow
            
        return self._workflows[user_id]
        
    def cleanup_inactive_workflows(self, max_idle_time: int = 3600) -> None:
        """Remove workflows that haven't been accessed for a specified time.
        
        This helps manage memory usage for long-running servers.
        
        Args:
            max_idle_time: Maximum idle time in seconds before a workflow is removed
        """
        current_time = time.time()
        users_to_remove = []
        
        for user_id, last_time in self._last_accessed.items():
            if current_time - last_time > max_idle_time:
                users_to_remove.append(user_id)
                
        for user_id in users_to_remove:
            if user_id in self._workflows:
                logger.info(f"Removing inactive workflow for user {user_id}")
                # The workflow's state should already be persisted in PostgreSQL
                # if that feature is enabled
                del self._workflows[user_id]
                del self._last_accessed[user_id]
    
    def get_all_user_ids(self) -> list:
        """Get a list of all user IDs with active workflows.
        
        Returns:
            List of user IDs
        """
        return list(self._workflows.keys())
