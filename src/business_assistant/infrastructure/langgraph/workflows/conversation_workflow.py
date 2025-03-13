"""Conversation workflow implementation using langgraph with React agent."""
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from business_assistant.infrastructure.ai.prompts import get_system_prompt
from business_assistant.infrastructure.langgraph.nodes.conversation_nodes import State, create_chatbot_node

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
        # Use MemorySaver to maintain conversation state between calls
        self.graph = self.graph_builder.compile(checkpointer=MemorySaver())
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

    def process_message(self, user_id: str, message: str) -> str:
        """Process a message through the conversation workflow using React agent.
        
        Args:
            user_id: The unique identifier for the user (e.g., WhatsApp number)
            message: The message to process.
            
        Returns:
            The assistant's response.
        """
        # Get or create a thread ID for this user
        if user_id not in self.user_threads:
            self.user_threads[user_id] = f"thread-{user_id}"
        
        thread_id = self.user_threads[user_id]
        
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
