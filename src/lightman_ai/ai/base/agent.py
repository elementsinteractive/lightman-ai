import logging
from abc import ABC, abstractmethod
from typing import Never

from lightman_ai.article.models import SelectedArticlesList
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.openai import OpenAIModel


class BaseAgent(ABC):
    _model: type[OpenAIModel] | type[GoogleModel]
    _model_name: str

    def __init__(self, system_prompt: str, logger: logging.Logger | None = None) -> None:
        model = self._model(self._model_name)
        self.agent: Agent[Never, SelectedArticlesList] = Agent(
            model=model, output_type=SelectedArticlesList, system_prompt=system_prompt
        )
        self.logger = logger or logging.getLogger("lightman")

    def get_prompt_result(self, prompt: str) -> SelectedArticlesList:
        return self._run_prompt(prompt)

    @abstractmethod
    def _run_prompt(self, prompt: str) -> SelectedArticlesList: ...
