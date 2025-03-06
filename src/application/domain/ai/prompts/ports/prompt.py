from abc import ABC, abstractmethod
from typing import TypedDict
class PromptPort(ABC):
    @abstractmethod
    def get_prompt(self, prompt_key: str) -> str:
        pass
    
    @abstractmethod
    def set_prompt_variables(self, prompt_key: str, variables: TypedDict) -> str:
        pass