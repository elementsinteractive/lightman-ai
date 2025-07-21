from abc import ABC
from typing import override

from pydantic import BaseModel


class BaseArticle(BaseModel, ABC):
    """Base abstract class for all Articles."""

    title: str
    link: str

    @override
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseArticle):
            return False

        return self.link == value.link

    @override
    def __hash__(self) -> int:
        return hash(self.link.encode())


class SelectedArticle(BaseArticle):
    why_is_relevant: str
    relevance_score: int


class Article(BaseArticle):
    title: str
    description: str


class BaseArticlesList[TArticle: BaseArticle](BaseModel):
    articles: list[TArticle]

    def __len__(self) -> int:
        return len(self.articles)

    @property
    def titles(self) -> list[str]:
        return [new.title for new in self.articles]

    @property
    def links(self) -> list[str]:
        return [new.link for new in self.articles]


class SelectedArticlesList(BaseArticlesList[SelectedArticle]):
    """
    Model that holds all the articles that were selected by the AI model.

    It saves the minimum information so that they are identifiable.
    """

    def get_articles_with_score_gte_threshold(self, score_threshold: int) -> list[SelectedArticle]:
        if not score_threshold > 0:
            raise ValueError("score threshold must be > 0.")
        return [article for article in self.articles if article.relevance_score >= score_threshold]


class ArticlesList(BaseArticlesList[Article]):
    """Model that saves articles with all their information."""
