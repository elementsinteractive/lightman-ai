import asyncio
import logging
from typing import Never, override

from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.ai.openai.exceptions import LimitTokensExceededError, map_openai_exceptions
from hackerman_ai.article.models import SelectedArticlesList
from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.models.openai import OpenAIModel


class OpenAIAgent(BaseAgent):
    """Class that provides an interface to operate with the OpenAI model."""

    def __init__(self, model: str, logger: logging.Logger | None = None) -> None:
        ai_model = OpenAIModel(model)
        self.agent: Agent[Never, SelectedArticlesList] = Agent(model=ai_model, output_type=SelectedArticlesList)
        self.logger = logger or logging.getLogger()

    async def _execute_agent(self, prompt: str) -> AgentRunResult[SelectedArticlesList]:
        async with map_openai_exceptions():
            return await self.agent.run(prompt)

    @override
    async def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        try:
            result = await self._execute_agent(prompt)
        except LimitTokensExceededError as err:
            self.logger.warning("waiting %s", err.wait_time)
            await asyncio.sleep(err.wait_time)
            result = await self._execute_agent(prompt)

        return result.output
