"""Conversation nodes for langgraph implementation using React agent."""
from typing import Annotated, Dict, List, Any
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from business_assistant.config.settings import settings
from toolbox_langchain import ToolboxClient
from business_assistant.infrastructure.tools.calculator_tool import get_calculator_tool
import logging

logger = logging.getLogger(__name__)


class State(TypedDict):
    """State type for conversation graph."""
    messages: Annotated[list, add_messages]
    context: Dict[str, Any] = {}


def create_chatbot_node() -> callable:
    """Create a React agent chatbot node with the specified model and tools.
    
    Args:
        model: The model to use for the chatbot.
        
    Returns:
        A function that can be used as a node in the graph.
    """
    # Initialize the LLM
    llm = ChatOpenAI(
        model_name = settings.openrouter_model,
        base_url = settings.openrouter_base_url,
        api_key = settings.openrouter_api_key,
        default_headers = {
            "HTTP-Referer": settings.site_url,
            "X-Title": settings.site_name,
        },
        temperature = 0.6
    )
    # Load tools from the Toolbox server
    client = ToolboxClient(settings.toolbox_base_url)
    toolbox_tools = client.load_toolset()
    
    # Add custom calculator tool
    calculator_tool = get_calculator_tool()
    
    # Combine all tools
    tools = toolbox_tools + [calculator_tool]
    
    # Create the React agent
    agent = create_react_agent(llm, tools, checkpointer=MemorySaver())
    
    def chatbot(state: State) -> Dict:
        """Process messages and generate a response using the React agent.
        
        Args:
            state: Current state containing messages.
            
        Returns:
            Dict containing the new messages to be added.
        """
        # Get the thread_id from the state or use a default
        thread_id = state.get("thread_id", "default-thread")
        
        # Initialize context if not present
        if "context" not in state:
            state["context"] = {}
            
        # Extract the last user message for analysis
        last_user_message = ""
        
        # Add detailed logging for message types
        if state["messages"]:
            logger.debug(f"Message types in state: {[type(msg).__name__ for msg in state['messages']]}")
            if hasattr(state["messages"][0], '__dict__'):
                logger.debug(f"First message attributes: {dir(state['messages'][0])}")
        
        for msg in reversed(state["messages"]):
            # Log message type for debugging
            logger.debug(f"Processing message of type: {type(msg).__name__}")
            
            # Handle different message types
            if isinstance(msg, dict):
                # Dict-like message
                if msg.get("role") == "user":
                    last_user_message = msg.get("content", "")
                    logger.debug(f"Found user message (dict): {last_user_message[:50]}...")
                    break
            elif hasattr(msg, 'type'):
                # Log message type
                logger.debug(f"Message has type attribute: {msg.type}")
                if msg.type == 'human':
                    # LangChain HumanMessage
                    last_user_message = msg.content
                    logger.debug(f"Found user message (LangChain): {last_user_message[:50]}...")
                    break
            elif hasattr(msg, 'role') and msg.role == 'user':
                # Generic object with role attribute
                if hasattr(msg, 'content'):
                    last_user_message = msg.content
                    logger.debug(f"Found user message (role object): {last_user_message[:50]}...")
                    break
            else:
                # Unknown message type
                logger.warning(f"Unknown message type: {type(msg).__name__}")
                
        # Log the conversation state for debugging
        logger.debug(f"Processing message with context: {state.get('context')}")
        logger.debug(f"Last user message: {last_user_message}")
        
        # Prepare inputs for the agent
        inputs = {"messages": state["messages"]}
        
        # Configure the agent with the thread_id and context
        config = {
            "configurable": {
                "thread_id": thread_id,
                "context": state.get("context", {})
            }
        }
        
        # Invoke the agent
        response = agent.invoke(inputs, stream_mode="values", config=config, debug=True)
        
        # Update context with any product information from the response
        # This helps maintain product context between interactions
        assistant_response = response["messages"][-1].content
         
        # Return the agent's response and updated context
        return {
            "messages": [response["messages"][-1]],
            "context": state.get("context", {})
        }

    return chatbot
