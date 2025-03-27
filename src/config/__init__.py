from .env import (
    # Reasoning LLM
    REASONING_MODEL,
    REASONING_BASE_URL,
    REASONING_API_KEY,
    # Basic LLM
    BASIC_MODEL,
    BASIC_BASE_URL,
    BASIC_API_KEY,
    # Vision-language LLM
    VL_MODEL,
    VL_BASE_URL,
    VL_API_KEY,
)

# Team configuration
TEAM_MEMBER_CONFIGURATIONS = {
    "coder": {
        "name": "coder",
        "desc": (
            "Responsible for code implementation, debugging and optimization, handling technical programming tasks"
        ),
        "desc_for_llm": (
            "Executes Python or Bash commands, performs mathematical calculations, and outputs a Markdown report. "
            "Must be used for all mathematical computations."
        ),
        "is_optional": True,
    },
    "customer_service": {
        "name": "customer_service",
        "desc": (
            "Responsible for addressing all customer inquiries regarding essential business information, locations, business hours, frequently asked questions, product inquiries, and product sales. You are in charge of providing customers with all the necessary information to facilitate the sale. However, you do not have the ability to create sales orders. In this case, you must pass this task to the sales agent."
        ),
        "desc_for_llm": "Provide customer service in a kind and harmonious manner, addressing all their inquiries.",
        "is_optional": False,
    },
    "sales_agent": {
        "name": "sales_agent",
        "desc": (
            "Responsible for creating sales orders based on customer inquiries and providing necessary information to customers. You must pass this task to the sales agent."
        ),
        "desc_for_llm": "Create sales orders based on customer inquiries and provide necessary information to customers.",
        "is_optional": False,
    },
}

TEAM_MEMBERS = list(TEAM_MEMBER_CONFIGURATIONS.keys())

__all__ = [
    # Reasoning LLM
    "REASONING_MODEL",
    "REASONING_BASE_URL",
    "REASONING_API_KEY",
    # Basic LLM
    "BASIC_MODEL",
    "BASIC_BASE_URL",
    "BASIC_API_KEY",
    # Vision-language LLM
    "VL_MODEL",
    "VL_BASE_URL",
    "VL_API_KEY",
    # Other configurations
    "TEAM_MEMBERS",
    "TEAM_MEMBER_CONFIGURATIONS",
]
