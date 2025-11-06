import logging
from abc import ABC, abstractmethod
from typing import ClassVar, Never, override

from lightman_ai.article.models import SelectedArticlesList
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.openai import OpenAIChatModel


class BaseAgent(ABC):
    _AGENT_CLASS: type[OpenAIChatModel] | type[GoogleModel]
    _DEFAULT_MODEL_NAME: str
    _AGENT_NAME: ClassVar[str]

    def __init__(self, system_prompt: str, model: str | None = None, logger: logging.Logger | None = None) -> None:
        selected_model = model or self._DEFAULT_MODEL_NAME
        agent_model = self._AGENT_CLASS(selected_model)
        self.agent: Agent[Never, SelectedArticlesList] = Agent(
            model=agent_model, output_type=SelectedArticlesList, system_prompt=system_prompt
        )
        self.logger = logger or logging.getLogger("lightman")
        self.logger.info("Selected %s's %s model", self, selected_model)

    @override
    def __str__(self) -> str:
        return self._AGENT_NAME

    @abstractmethod
    def run_prompt(self, prompt: str) -> SelectedArticlesList: ...
