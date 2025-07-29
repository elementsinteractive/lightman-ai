from abc import ABC, abstractmethod
from datetime import datetime

from lightman_ai.article.models import ArticlesList


class BaseSource(ABC):
    @abstractmethod
    def get_articles(self, date: datetime | None = None) -> ArticlesList: ...
