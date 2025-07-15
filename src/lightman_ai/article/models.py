from abc import ABC, abstractmethod
from typing import override

import tiktoken
from lightman_ai.core.settings import settings
from pydantic import BaseModel


class BaseArticle(BaseModel, ABC):
    """Base abstract class for all Articles."""

    title: str
    link: str
    _encoding: tiktoken.Encoding = tiktoken.get_encoding(settings.OPENAI_ENCODING)

    @override
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseArticle):
            return False

        return self.link == value.link

    @override
    def __hash__(self) -> int:
        return hash(self.link.encode())

    @property
    @abstractmethod
    def number_of_tokens(self) -> int: ...


class SelectedArticle(BaseArticle):
    why_is_relevant: str
    relevance_score: int

    @override
    @property
    def number_of_tokens(self) -> int:
        """
        Number of tokens that this Article has.

        Worth taking into account that this is not the final number of tokens to be sent,
        as pydantic-ai adds some extra characters.

        It is a rough estimation of the total tokens to be sent for this Article.
        """
        tokens = self._encoding.encode(
            f'"link": "{self.link}", "title": "{self.title}", "why_is_relevant": "{self.why_is_relevant}", "score_threshold": "{self.relevance_score}"'
        )
        return len(tokens)


class Article(BaseArticle):
    title: str
    description: str

    @override
    @property
    def number_of_tokens(self) -> int:
        """
        Number of tokens that this Article has.

        Worth taking into account that this is not the final number of tokens to be sent,
        as pydantic-ai adds some extra characters.

        It is a rough estimation of the total tokens to be sent for this Article.
        """
        tokens = self._encoding.encode(
            f'"title": "{self.title}", "description": "{self.description}", "link": "{self.link}"'
        )
        return len(tokens)


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

    @property
    def total_number_of_tokens(self) -> int:
        return sum(article.number_of_tokens for article in self.articles)


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
