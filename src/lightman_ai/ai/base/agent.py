from abc import ABC, abstractmethod

from lightman_ai.article.models import SelectedArticlesList


class BaseAgent(ABC):
    model: str

    def get_prompt_result(self, prompt: str) -> SelectedArticlesList:
        return self._run_prompt(prompt)

    @abstractmethod
    def _run_prompt(self, prompt: str) -> SelectedArticlesList: ...
