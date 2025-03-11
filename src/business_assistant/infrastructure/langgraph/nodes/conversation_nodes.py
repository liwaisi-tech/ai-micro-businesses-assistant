"""Conversation nodes for langgraph implementation."""
from typing import Annotated, Dict
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from business_assistant.config.settings import settings


class State(TypedDict):
    """State type for conversation graph."""
    messages: Annotated[list, add_messages]


def create_chatbot_node(model: str = "") -> callable:
    """Create a chatbot node with the specified model.
    
    Args:
        model: The model to use for the chatbot.
        
    Returns:
        A function that can be used as a node in the graph.
    """
    llm = ChatOpenAI(
        model_name = model,
        base_url = settings.openrouter_base_url,
        api_key = settings.openrouter_api_key,
        default_headers = {
            "HTTP-Referer": settings.site_url,
            "X-Title": settings.site_name,
        }
    )

    def chatbot(state: State) -> Dict:
        """Process messages and generate a response.
        
        Args:
            state: Current state containing messages.
            
        Returns:
            Dict containing the new messages to be added.
        """
        return {"messages": [llm.invoke(state["messages"])]}

    return chatbot
