"""Calculator tool for basic product price calculations."""
import re
from typing import Dict, Any, List, Optional, Union
from langchain.tools import BaseTool
import logging

logger = logging.getLogger(__name__)

class CalculatorTool(BaseTool):
    """Tool for performing basic calculations related to product pricing.
    
    This tool can:
    - Calculate total price for multiple products
    - Apply discounts
    - Calculate tax
    - Convert between currencies (using fixed rates)
    """
    
    name: str = "calculator"
    description: str = """
    Utiliza esta herramienta para realizar cálculos matemáticos básicos relacionados con productos y precios.
    
    Ejemplos de uso:
    - Cuando un cliente pregunta por el precio total de varios productos
    - Para calcular descuentos sobre productos
    - Para calcular impuestos sobre precios
    - Para convertir precios entre monedas
    
    La herramienta acepta expresiones matemáticas y devuelve el resultado del cálculo.
    """
    
    def _run(self, query: str) -> str:
        """Run the calculator tool.
        
        Args:
            query: The calculation expression to evaluate.
            
        Returns:
            The result of the calculation as a string.
        """
        try:
            # Clean the input to ensure it's safe to evaluate
            sanitized_query = self._sanitize_input(query)
            
            # Evaluate the expression
            result = eval(sanitized_query)
            
            # Format the result
            if isinstance(result, (int, float)):
                # Round to 2 decimal places for currency values
                formatted_result = f"{result:.2f}"
                return formatted_result
            else:
                return str(result)
                
        except Exception as e:
            logger.error(f"Error in calculator tool: {str(e)}")
            return f"Error al realizar el cálculo: {str(e)}"
    
    def _sanitize_input(self, query: str) -> str:
        """Sanitize the input to ensure it's safe to evaluate.
        
        Args:
            query: The raw calculation expression.
            
        Returns:
            A sanitized version of the expression safe to evaluate.
        """
        # Remove all characters except digits, basic operators, parentheses, and decimal points
        sanitized = re.sub(r'[^0-9+\-*/().%\s]', '', query)
        
        # Check if the sanitized string is empty or contains only invalid characters
        if not sanitized or all(c in ' ' for c in sanitized):
            raise ValueError("La expresión no contiene operaciones matemáticas válidas")
            
        return sanitized

def get_calculator_tool() -> CalculatorTool:
    """Create and return a calculator tool instance.
    
    Returns:
        An instance of the CalculatorTool.
    """
    return CalculatorTool()
