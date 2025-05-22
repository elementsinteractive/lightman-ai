import logging
from typing import Never, override

from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.ai.gemini.exceptions import map_gemini_exceptions
from hackerman_ai.article.models import SelectedArticlesList
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel


class GeminiAgent(BaseAgent):
    """Class that provides an interface to operate with the Gemini model."""

    def __init__(self, model: str, logger: logging.Logger | None = None) -> None:
        ai_model = GeminiModel(model)
        self.agent: Agent[Never, SelectedArticlesList] = Agent(model=ai_model, output_type=SelectedArticlesList)
        self.logger = logger or logging.getLogger()

    @override
    async def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        async with map_gemini_exceptions():
            result = await self.agent.run(prompt)
        return result.output
