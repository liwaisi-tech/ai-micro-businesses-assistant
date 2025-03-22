"""Conversation workflow implementation using langgraph with React agent."""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg_pool
import psycopg

from business_assistant.infrastructure.ai.prompts import get_system_prompt
from business_assistant.infrastructure.langgraph.nodes.conversation_nodes import State, create_chatbot_node
from business_assistant.config.settings import settings

import logging

logger = logging.getLogger(__name__)

class ConversationWorkflow:
    """Manages the conversation workflow using langgraph with React agent."""

    def __init__(self):
        """Initialize the conversation workflow with React agent.
        
        Args:
            model: The model to use for the chatbot.
        """
        self.graph_builder = StateGraph(State)
        self._setup_graph()
        
        # Use PostgreSQL checkpointer if possible, fallback to MemorySaver
        try:
            self.checkpointer = self._init_postgres_checkpointer()
            logger.info("Using PostgreSQL checkpointer for conversation state persistence")
            self.using_postgres = True
        except Exception as e:
            logger.warning(f"Failed to initialize PostgreSQL checkpointer, falling back to MemorySaver: {str(e)}")
            self.checkpointer = MemorySaver()
            self.using_postgres = False
            
        self.graph = self.graph_builder.compile(checkpointer=self.checkpointer)
        # Store thread IDs for different users
        self.user_threads = {}
        # Store context for different users
        self.user_contexts = {}

    def _setup_graph(self) -> None:
        """Set up the graph with nodes and edges."""
        # Add chatbot node with React agent
        self.graph_builder.add_node("chatbot", create_chatbot_node())
        
        # Add edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        
    def _init_postgres_checkpointer(self):
        """Initialize the PostgreSQL checkpointer saver.
        
        Returns:
            PostgresSaver: The PostgreSQL checkpointer instance.
            
        Raises:
            Exception: If the PostgreSQL connection fails.
        """
        try:
            # Create connection string from settings
            connection_string = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
            

            
            # Connect with autocommit=True to avoid transaction blocks for CREATE INDEX CONCURRENTLY
            conn = psycopg.connect(connection_string, autocommit=True)
            
            # Create PostgresSaver with the direct connection
            checkpointer = PostgresSaver(conn=conn)
            
            # Setup the tables (this will work now because autocommit=True)
            checkpointer.setup()
            
            logger.info("PostgreSQL checkpointer initialized successfully")
            return checkpointer
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL checkpointer: {str(e)}")
            raise

    def _restore_thread_from_checkpointer(self, user_id: str):
        """Attempt to restore a thread and its context from the checkpointer.
        
        Args:
            user_id: The unique identifier for the user
            
        Returns:
            tuple: (thread_id, context) - The thread ID and context if found, or (None, {}) if not
        """
        thread_id = f"thread-{user_id}"
        
        # Only attempt to restore from PostgreSQL checkpointer
        if not self.using_postgres:
            return thread_id, {}
            
        try:
            # Check if this thread exists in the checkpointer
            if hasattr(self.checkpointer, 'list_checkpoints'):
                checkpoints = self.checkpointer.list_checkpoints()
                logger.debug(f"Available checkpoints: {checkpoints}")
                
                # Look for the thread ID in available checkpoints
                if thread_id in checkpoints:
                    logger.info(f"Found existing checkpoint for thread {thread_id}")
                    
                    # Get the latest state for this thread
                    config = {"configurable": {"thread_id": thread_id}}
                    state = self.checkpointer.get(thread_id)
                    
                    if state and "context" in state:
                        logger.info(f"Restored context for user {user_id} from checkpoint")
                        return thread_id, state["context"]
        except Exception as e:
            logger.warning(f"Error restoring thread from checkpointer: {str(e)}")
            
        return thread_id, {}
    
    def process_message(self, user_id: str, message: str) -> str:
        """Process a message through the conversation workflow using React agent.
        
        Args:
            user_id: The unique identifier for the user (e.g., WhatsApp number)
            message: The message to process.
            
        Returns:
            The assistant's response.
        """
        # Try to restore thread and context from checkpointer
        thread_id, restored_context = self._restore_thread_from_checkpointer(user_id)
        
        # Update user_threads with the thread ID
        self.user_threads[user_id] = thread_id
        
        # Use restored context if available, otherwise use existing in-memory context or empty dict
        if restored_context:
            self.user_contexts[user_id] = restored_context
            logger.info(f"Using restored context for user {user_id} from checkpoint")
        
        # Get existing context for this user if available
        user_context = self.user_contexts.get(user_id, {})
        logger.debug(f"Retrieved existing context for user {user_id}: {user_context}")
        
        # Initialize state with system and user messages
        initial_state = {
            "messages": [
                {
                    "role": "system",
                    "content": get_system_prompt()
                },
                {"role": "user", "content": message}
            ],
            "thread_id": thread_id,
            "context": user_context
        }
        
        # Configure the graph with the thread_id
        config = {"configurable": {"thread_id": thread_id}}
        
        # Process through graph
        try:
            last_context = {}
            for event in self.graph.stream(initial_state, config=config):
                logger.debug(f"Event: {event}")
                for key, value in event.items():
                    # Store context for future use
                    if "context" in value and value["context"]:
                        last_context = value["context"]
                        logger.debug(f"Updated context: {last_context}")
                    
                    # Return the assistant's response
                    if "messages" in value and value["messages"]:
                        # Store the context in the user's thread data for future messages
                        if last_context:
                            # Create a simple dictionary to store user contexts if it doesn't exist
                            if not hasattr(self, 'user_contexts'):
                                self.user_contexts = {}
                            
                            # Store the context for this user
                            self.user_contexts[user_id] = last_context
                            logger.debug(f"Saved context for user {user_id}: {last_context}")
                            
                            # Explicitly save the state to the checkpointer if using PostgreSQL
                            if self.using_postgres:
                                try:
                                    # Ensure the thread ID is in the checkpointer
                                    thread_id = self.user_threads.get(user_id, f"thread-{user_id}")
                                    
                                    # Create a state object with the context
                                    state_to_save = {
                                        "messages": value["messages"],
                                        "context": last_context,
                                        "thread_id": thread_id
                                    }
                                    
                                    # Save to the checkpointer
                                    self.checkpointer.put(thread_id, state_to_save)
                                    logger.info(f"Explicitly saved state to PostgreSQL checkpointer for thread {thread_id}")
                                except Exception as e:
                                    logger.error(f"Failed to explicitly save state to checkpointer: {str(e)}")
                        
                        # Handle both dict-like messages and LangChain message objects
                        last_message = value["messages"][-1]
                        if hasattr(last_message, 'content'):
                            # LangChain message object
                            return last_message.content
                        elif isinstance(last_message, dict) and "content" in last_message:
                            # Dictionary-style message
                            return last_message["content"]
                        else:
                            # Fallback
                            logger.warning(f"Unexpected message format: {type(last_message)}")
                            return str(last_message)
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return "Lo siento, se me presentó un error y no puedo responderte ahora."

        return "Lo siento, no pude procesar tu mensaje."
