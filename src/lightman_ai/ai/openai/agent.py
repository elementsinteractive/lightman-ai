import logging
import time
from typing import Never, override

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.ai.openai.exceptions import LimitTokensExceededError, map_openai_exceptions
from lightman_ai.article.models import SelectedArticlesList
from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.models.openai import OpenAIModel


class OpenAIAgent(BaseAgent):
    """Class that provides an interface to operate with the OpenAI model."""

    model: str = "gpt-4.1"

    def __init__(self, logger: logging.Logger | None = None) -> None:
        ai_model = OpenAIModel(self.model)
        self.agent: Agent[Never, SelectedArticlesList] = Agent(model=ai_model, output_type=SelectedArticlesList)
        self.logger = logger or logging.getLogger()

    def _execute_agent(self, prompt: str) -> AgentRunResult[SelectedArticlesList]:
        with map_openai_exceptions():
            return self.agent.run_sync(prompt)

    @override
    def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        try:
            result = self._execute_agent(prompt)
        except LimitTokensExceededError as err:
            self.logger.warning("waiting %s", err.wait_time)
            time.sleep(err.wait_time)
            result = self._execute_agent(prompt)
        return result.output
