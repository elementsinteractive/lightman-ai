from abc import ABC
from datetime import datetime
from typing import Self, override

from lightman_ai.article.exceptions import NoTimeZoneError
from pydantic import BaseModel, Field, field_validator


class BaseArticle(BaseModel, ABC):
    """Base abstract class for all Articles."""

    title: str = Field(..., min_length=1)
    link: str = Field(..., min_length=1)
    published_at: datetime = Field(..., description="Must be timezone aware")

    @field_validator("published_at", mode="after")
    @classmethod
    def validate_timezone_aware(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise NoTimeZoneError("published_at must be timezone aware")
        return v

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
    description: str = Field(..., min_length=1)


class BaseArticlesList[TArticle: BaseArticle](BaseModel):
    articles: list[TArticle]

    def __len__(self) -> int:
        return len(self.articles)

    @property
    def titles(self) -> list[str]:
        return [article.title for article in self.articles]

    @property
    def links(self) -> list[str]:
        return [article.link for article in self.articles]

    @classmethod
    def get_articles_from_date_onwards(cls, articles: list[TArticle], start_date: datetime) -> Self:
        if not start_date.tzinfo:
            raise NoTimeZoneError("A timezone is needed for filtering articles")
        articles = [article for article in articles if article.published_at >= start_date]
        return cls(articles=articles)


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
