import os
import json
import httpx
from typing import Any
from application.domain.ai.agents.ports.agent import AgentPort
from openai import AsyncOpenAI, OpenAI

class OpenRouterAgent(AgentPort):
    """Implementation of the AgentPort using OpenRouter."""
    
    def __init__(self, system_prompt: str):
        """Initialize the OpenRouter agent with the provided API key."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL")
        self.model = os.getenv("OPENROUTER_MODEL")
        self.ai_client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        self.async_ai_client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        self.system_prompt = system_prompt
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]
    
    async def clear_conversation(self) -> None:
        """Clear the current conversation history with the agent."""
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

    async def ask_to_agent(self, message: str) -> Any:
        """
        Send a message to the agent and get its response.
        
        Args:
            message (str): The message to send to the agent
            
        Returns:
            Any: The agent's response
        """
        # Add user message to conversation
        self.messages.append({"role": "user", "content": message})
        
        completion = await self.async_ai_client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})
        return response


    