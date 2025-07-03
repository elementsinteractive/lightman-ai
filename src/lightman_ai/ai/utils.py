from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.ai.gemini.agent import GeminiAgent
from lightman_ai.ai.openai.agent import OpenAIAgent

MODEL_TO_AGENT_MAPPING = {"gpt-4.1": OpenAIAgent, "gemini-2.5-pro-preview-05-06": GeminiAgent}


def get_agent_instance_from_model_name(model: str) -> BaseAgent:
    if model not in MODEL_TO_AGENT_MAPPING:
        raise ValueError(f"Model '{model}' is not recognized. Available models: {list(MODEL_TO_AGENT_MAPPING.keys())}")
    return MODEL_TO_AGENT_MAPPING[model](model)


MODEL_CHOICES = list(MODEL_TO_AGENT_MAPPING.keys())
