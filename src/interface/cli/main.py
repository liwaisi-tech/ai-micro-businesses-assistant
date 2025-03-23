import re
import signal
import sys
import asyncio
from typing import AsyncGenerator
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from supervisor_assistant.infrastructure.ai.langgraph.workflows.business_administrator import create_new_business_administrator_workflow

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format: +<country_code><number>"""
    pattern = r'^\+\d{1,3}\d{10}$'
    return bool(re.match(pattern, phone))

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n👋 ¡Gracias por usar nuestro servicio! ¡Hasta pronto!\n")
    sys.exit(0)

def display_welcome_message():
    """Display a welcoming message with emojis"""
    welcome_text = """
    ╔════════════════════════════════════════════════════╗
    ║  🌟 ¡Bienvenido al Asistente Virtual de Micro-Negocios! 🌟  ║
    ║                                                    ║
    ║  🤖 Soy Sara, tu asistente personal para:          ║
    ║     📊 Gestión de inventario                       ║
    ║     💰 Ventas y reservas                          ║
    ║     👥 Servicio al cliente                        ║
    ║                                                    ║
    ║  ⌨️  Para salir del chat, presiona Ctrl + C        ║
    ╚════════════════════════════════════════════════════╝
    """
    print("\033[94m" + welcome_text + "\033[0m")

async def chat_loop(phone_number: str):
    """Main chat loop with direct invocation"""
    checkpointer = InMemorySaver()
    store = InMemoryStore()
    app = create_new_business_administrator_workflow(
        checkpointer=checkpointer,
        store=store
    )
    
    config = {
        "configurable": {"thread_id": phone_number},
        "recursion_limit": 10
    }
    
    while True:
        try:
            print("\033[94m\nTú:\033[0m ", end='')
            user_input = input()
            if not user_input.strip():
                continue
                
            response = await app.ainvoke({
                "messages": [{
                    "role": "user",
                    "content": user_input
                }]
            }, config=config)
            
            print("\033[92mSara:\033[0m ", end='')
            if 'messages' in response and response['messages']:
                messages = response['messages']
                if messages and isinstance(messages, list):
                    latest_message = messages[-1]
                    if hasattr(latest_message, 'content'):
                        print("\033[92m" + latest_message.content + "\033[0m")
                    else:
                        print("\033[91mMensaje sin contenido\033[0m")
                else:
                    print("\033[91mNo hay mensajes disponibles\033[0m")
            else:
                print("\033[91mNo se recibió respuesta\033[0m")
            
        except EOFError:
            break

async def main():
    display_welcome_message()
    
    while True:
        phone = input("\n📱 Por favor, ingresa tu número de WhatsApp (formato: +573658425187): ")
        if validate_phone_number(phone):
            break
        print("\033[91m❌ Formato inválido. Usa el formato: +<código_país><número>\033[0m")
    
    print(f"\n\033[92m✅ Número validado: {phone}\033[0m")
    print("\n\033[94m💬 ¡Empecemos a chatear!\n\033[0m")
    
    signal.signal(signal.SIGINT, signal_handler)
    await chat_loop(phone)

if __name__ == "__main__":
    asyncio.run(main())
