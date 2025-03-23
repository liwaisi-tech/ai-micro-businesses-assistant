import datetime
from typing import Annotated, TypedDict
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

from supervisor_assistant.infrastructure.ai.langgraph.factory.llm_factory import llm_factory


class MicroBusinessExpertAgent:
    def __init__(self, llm):
        self.llm = llm
        if not self.llm:
            self.llm = llm_factory.create_openai_llm()
            
    @tool()
    def opening_hours(self) -> str:
        """
        Use this tool to answer any question or request that is not a greeting.
        
        Args:
            question: The client's question that needs to be answered.
        """
        return {
            "opening_hours": {
                "monday": "7 am - 6 pm",
                "tuesday": "7 am - 6 pm",
                "wednesday": "7 am - 6 pm",
                "thursday": "7 am - 6 pm",
                "friday": "7 am - 6 pm",
                "saturday": "7 am - 3 pm",
                "sunday": "Closed"
            }
        }
    
    @tool()
    def company_information(self, ) -> str:
        """
        Use this tool to answer any question or request that is not a greeting.
        
        Args:
            question: The client's question that needs to be answered.
        """
        return {
            "company": {
                "name": "Liwaisi Tech",
                "description": "Liwaisi Tech es una compañía de triple impacto enfocada en Educación, Desarrollo Sostenible e Innovación con Tecnologías de la información en zonas rurales de Colombia.",
                "address": "Vereda El Guineo, Aguazul, Casanare, Colombia",
                "phone": "+573228655704",
                "email": "liwaisitech@gmail.com"
            }
        }

    def create_micro_business_expert_agent(self) -> CompiledGraph:
        return create_react_agent(
            model=self.llm,
            name = "micro_business_expert",
            prompt="""
            You are the expert of any micro business information. Your function is to know every detail of Liwaisi Tech micro business.
            Use the availables tools to respond any question or request.
            
            The tools available are:
            
            - Company_information: Use this tool to answer about any company question like legal information, opening hours, contact information, etc.
            - Opening_hours: Use this tool to answer about any opening hours question.
            
            """,
            tools=[self.company_information, self.opening_hours]
        )