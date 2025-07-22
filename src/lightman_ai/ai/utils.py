from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.ai.gemini.agent import GeminiAgent
from lightman_ai.ai.openai.agent import OpenAIAgent

AGENT_MAPPING = {"openai": OpenAIAgent, "gemini": GeminiAgent}


def get_agent_class_from_agent_name(agent: str) -> type[BaseAgent]:
    if agent not in AGENT_MAPPING:
        raise ValueError(f"Agent '{agent}' is not recognized. Available agents: {list(AGENT_MAPPING.keys())}")
    return AGENT_MAPPING[agent]


AGENT_CHOICES = list(AGENT_MAPPING.keys())
