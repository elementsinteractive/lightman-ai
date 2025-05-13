from abc import ABC, abstractmethod

from hackerman_ai.article.models import SelectedArticlesList


class BaseAgent(ABC):
    @abstractmethod
    async def get_prompt_result(self, prompt: str, iterations: int = 1) -> SelectedArticlesList: ...
