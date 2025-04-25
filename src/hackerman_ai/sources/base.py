from abc import ABC, abstractmethod

from hackerman_ai.article.models import ArticlesList


class BaseSource(ABC):
    @abstractmethod
    async def get_articles(self) -> ArticlesList: ...
