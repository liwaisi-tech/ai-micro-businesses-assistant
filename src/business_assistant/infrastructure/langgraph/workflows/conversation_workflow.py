"""Conversation workflow implementation using langgraph."""
from langgraph.graph import StateGraph, START, END

from business_assistant.infrastructure.ai.prompts import get_system_prompt
from business_assistant.infrastructure.langgraph.nodes.conversation_nodes import State, create_chatbot_node


class ConversationWorkflow:
    """Manages the conversation workflow using langgraph."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        """Initialize the conversation workflow.
        
        Args:
            model: The model to use for the chatbot.
        """
        self.graph_builder = StateGraph(State)
        self._setup_graph(model)
        self.graph = self.graph_builder.compile()

    def _setup_graph(self, model: str) -> None:
        """Set up the graph with nodes and edges.
        
        Args:
            model: The model to use for the chatbot.
        """
        # Add chatbot node
        self.graph_builder.add_node("chatbot", create_chatbot_node(model))
        
        # Add edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def process_message(self, message: str) -> str:
        """Process a message through the conversation workflow.
        
        Args:
            message: The message to process.
            
        Returns:
            The assistant's response.
        """
        # Initialize state with system and user messages
        initial_state = {
            "messages": [
                {
                    "role": "system",
                    "content": get_system_prompt()
                },
                {"role": "user", "content": message}
            ]
        }
        
        # Process through graph
        for event in self.graph.stream(initial_state):
            for value in event.values():
                return value["messages"][-1].content

        return "Sorry, I couldn't process your message."
