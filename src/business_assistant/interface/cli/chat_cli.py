"""CLI interface for the business assistant chat."""
import os
import sys
import re
import requests
from typing import Optional
import readline  # Enable arrow key navigation and command history

class ChatCLI:
    """CLI chat interface for the business assistant."""
    
    def __init__(self):
        """Initialize the chat CLI."""
        self.api_url = "http://localhost:8080/ai-business-assistant/api/v1/chat/message"
        self.whatsapp_number: Optional[str] = None
        
    def validate_whatsapp_number(self, number: str) -> bool:
        """Validate WhatsApp number format.
        
        Args:
            number: WhatsApp number to validate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        pattern = r'^\+\d{1,3}\d{10}$'  # Format: +CountryCodeNumber
        return bool(re.match(pattern, number))
    
    def get_whatsapp_number(self) -> None:
        """Get and validate WhatsApp number from user input."""
        while True:
            number = input("\nIngrese su número de WhatsApp (formato: +573658425187): ")
            if self.validate_whatsapp_number(number):
                self.whatsapp_number = number
                break
            print("\n❌ Formato inválido. Use el formato +CountryCodeNumber (ejemplo: +573658425187)")
    
    def send_message(self, message: str) -> Optional[str]:
        """Send message to the API and get response.
        
        Args:
            message: Message to send.
            
        Returns:
            Optional[str]: Response from the API or None if error.
        """
        try:
            headers = {
                "Content-Type": "application/json",
            }
            response = requests.post(
                self.api_url,
                headers=headers,
                json={"message": message, "whatsapp_number": self.whatsapp_number}
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Error al enviar mensaje: {str(e)}")
            return None
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_welcome(self):
        """Print welcome message."""
        self.clear_screen()
        print("=" * 50)
        print("       Liwaisi Tech - Asistente de Negocios")
        print("=" * 50)
        print("\nBienvenido al chat de asistencia de Liwaisi Tech.")
        print("Para salir, escriba 'exit' o presione Ctrl+C")
        print("-" * 50)
        
    def run(self):
        """Run the chat CLI interface."""
        self.print_welcome()
        self.get_whatsapp_number()
        
        print("\n✅ Número validado. ¡Comencemos!")
        print("-" * 50)
        
        while True:
            try:
                message = input("\nUsted: ")
                if message.lower() in ['exit', 'quit', 'salir']:
                    print("\n👋 ¡Gracias por usar nuestro servicio!")
                    break
                    
                if message.strip():
                    response = self.send_message(message)
                    if response:
                        print(f"\nSara: {response}")
                        
            except KeyboardInterrupt:
                print("\n\n👋 ¡Gracias por usar nuestro servicio!")
                break
                
def main():
    """Main entry point for the CLI application."""
    try:
        cli = ChatCLI()
        cli.run()
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
