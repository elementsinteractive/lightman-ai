import logging
from typing import Never, override

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.ai.gemini.exceptions import map_gemini_exceptions
from lightman_ai.article.models import SelectedArticlesList
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel


class GeminiAgent(BaseAgent):
    """Class that provides an interface to operate with the Gemini model."""

    def __init__(self, model: str, logger: logging.Logger | None = None) -> None:
        ai_model = GoogleModel(model)
        self.agent: Agent[Never, SelectedArticlesList] = Agent(model=ai_model, output_type=SelectedArticlesList)
        self.logger = logger or logging.getLogger()

    @override
    def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        with map_gemini_exceptions():
            result = self.agent.run_sync(prompt)
        return result.output
