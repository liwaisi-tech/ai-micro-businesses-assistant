from typing import Literal

# Define available LLM types
LLMType = Literal["basic", "reasoning", "vision"]

# Define agent-LLM mapping
AGENT_LLM_MAP: dict[str, LLMType] = {
    "coordinator": "basic",  # basic llm
    "planner": "reasoning",  # reasoning llm
    "supervisor": "basic",  # basic llm
    "researcher": "basic",  # basic llm
    "coder": "basic",  # basic llm
    "browser": "vision",  # vision llm
    "reporter": "basic",  # basic llm
}
