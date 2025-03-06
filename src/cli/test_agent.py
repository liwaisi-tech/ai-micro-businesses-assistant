#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from infrastructure.ai.agents.openrouter.agent import OpenRouterAgent
from application.domain.ai.prompts.services.prompt import get_prompt, set_prompt_variables
async def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize the agent with a system prompt
    system_prompt = get_prompt("system")
    processed_system_prompt = set_prompt_variables("system")
    
    agent = OpenRouterAgent(processed_system_prompt)
    print(processed_system_prompt)
    print("-" * 50)
    print("Welcome to the AI Micro Business Assistant CLI!")
    print("Type 'exit' to quit or 'clear' to clear the conversation history.")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle special commands
            if user_input.lower() == 'exit':
                print("\nGoodbye!")
                break
            elif user_input.lower() == 'clear':
                await agent.clear_conversation()
                print("\nConversation history cleared!")
                continue
            
            # Get agent's response
            response = await agent.ask_to_agent(user_input)
            
            # Print response
            print("\nAssistant:", response)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again or type 'exit' to quit.")

if __name__ == "__main__":
    asyncio.run(main()) 