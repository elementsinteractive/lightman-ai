from typing import override

from pydantic import BaseModel


class BaseArticle(BaseModel):
    link: str

    @override
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseArticle):
            return False

        return self.link == value.link

    @override
    def __hash__(self) -> int:
        return hash(self.link.encode())


class SelectedArticle(BaseArticle): ...


class Article(BaseArticle):
    title: str
    description: str


class BaseArticlesList[TArticle: BaseArticle](BaseModel):
    articles: list[TArticle]

    @property
    def links(self) -> list[str]:
        return [new.link for new in self.articles]


class SelectedArticlesList(BaseArticlesList[SelectedArticle]):
    """
    Model that holds all the articles that were selected by the AI model.

    It saves the minimum information so that they are identifiable.
    """


class ArticlesList(BaseArticlesList[Article]):
    """Model that saves articles with all their information."""

    @property
    def titles(self) -> list[str]:
        return [new.title for new in self.articles]
