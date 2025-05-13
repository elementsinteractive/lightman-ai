from typing import Literal

from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.ai.openai.agent import OpenAIAgent

MODEL_TO_AGENT_MAPPING = {"openai": OpenAIAgent}


def get_agent_from_model_name(model: str) -> BaseAgent:
    if model not in MODEL_TO_AGENT_MAPPING:
        raise ValueError(f"Model '{model}' is not recognized. Available models: {list(MODEL_TO_AGENT_MAPPING.keys())}")
    return MODEL_TO_AGENT_MAPPING[model]()


MODEL_CHOICES = list(MODEL_TO_AGENT_MAPPING.keys())
MODEL_NAMES = Literal["openai"]
