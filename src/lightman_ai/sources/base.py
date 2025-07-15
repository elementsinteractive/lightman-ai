from abc import ABC, abstractmethod

from lightman_ai.article.models import ArticlesList


class BaseSource(ABC):
    @abstractmethod
    def get_articles(self) -> ArticlesList: ...
