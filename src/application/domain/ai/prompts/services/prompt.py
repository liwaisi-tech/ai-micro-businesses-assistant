from application.domain.ai.prompts.services.system_prompt import system_prompt
from application.domain.ai.prompts.ports.prompt import PromptPort
from typing import TypedDict
# Default variables for the prompts
default_variables = {
    "company_name": "Liwaisi",
    "assistant_name": "María Laya",
    "topics": """
    - Pregunta sobre los productos disponibles o no disponibles
    - Pregunta sobre los precios de los productos
    - Pregunta sobre los horarios de atención
    - Pregunta sobre domicilios y horas de entrega
    - Preguntas sobre cómo tener un asistente virtual para micro negocios. Siempre dirígelo a whatsapp.
    """,
    "products": """
    - Miel Melawi orgánica 330 gr aproximadamente Precio: veinticinco mil pesos colombianos. Cantidad en stock: 10 unidades.
    - Miel Melawi orgánica 500 gr aproximadamente Precio: cuarenta y cinco mil pesos colombianos. Cantidad en stock: 15 unidades.
    - Miel Melawi orgánica 1000 gr aproximadamente Precio: ochenta y cinco mil pesos colombianos. Cantidad en stock: 5 unidades.
    """,
    "hours": "Horarios de atención: Lunes a Viernes de 8:00 am a 5:00 pm, Sábados de 9:00 am a 1:00 pm. Domingos y festivos no directamente pero puedes apartar tu pedido para el siguiente día hábil.",
    "contact_info": """
    - Whatsapp: +57 3228655704. Entrégale al usuario el siguiente link para que pueda contactar al whatsapp de la empresa: https://wa.me/573228655704
    """
}

# Store prompts with their variables
prompts = {
    "system": system_prompt
}

def get_prompt(prompt_key: str) -> str:
    """Get a prompt by its key."""
    return prompts[prompt_key]

def set_prompt_variables(prompt_key: str, variables: TypedDict = None) -> str:
    """
    Set variables for the system prompt.
    
    Args:
        variables (dict, optional): Dictionary of variables to replace in the prompt.
                                  If None, uses default_variables.
    
    Returns:
        str: The processed system prompt with variables replaced
    """
    if variables is None:
        variables = default_variables
    
    processed_prompt = prompts[prompt_key]
    for key, value in variables.items():
        processed_prompt = processed_prompt.replace("{{" + key + "}}", value)
    
    return processed_prompt
