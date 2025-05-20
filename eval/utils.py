from dataclasses import dataclass
from decimal import Decimal

from hackerman_ai.article.models import Article, ArticlesList


@dataclass
class ClassifiedArticleResults:
    results: ArticlesList
    correctly_found_articles: set[Article]
    false_positives: set[Article]
    false_negatives: set[Article]
    total_relevant_articles: int

    @property
    def total_results(self) -> int:
        return len(self.results.articles)

    @property
    def total_correctly_found_articles(self) -> int:
        return len(self.correctly_found_articles)

    @property
    def total_false_positives(self) -> int:
        return len(self.false_positives)

    @property
    def total_false_negatives(self) -> int:
        return len(self.false_negatives)

    @property
    def recall(self) -> Decimal:
        if self.total_correctly_found_articles + self.total_false_negatives == 0:
            return Decimal(0)
        return round(
            Decimal(
                self.total_correctly_found_articles / (self.total_correctly_found_articles + self.total_false_negatives)
            ),
            2,
        )

    @property
    def precision(self) -> Decimal:
        if self.total_correctly_found_articles + self.total_false_positives == 0:
            return Decimal(0)
        return round(
            Decimal(
                self.total_correctly_found_articles / (self.total_correctly_found_articles + self.total_false_positives)
            ),
            2,
        )

    @property
    def false_positives_titles(self) -> list[str]:
        return [article.title for article in self.false_positives]

    @property
    def correctly_found_articles_titles(self) -> list[str]:
        return [article.title for article in self.correctly_found_articles]

    @property
    def false_negatives_titles(self) -> list[str]:
        return [article.title for article in self.false_negatives]

    @property
    def articles_found_titles(self) -> list[str]:
        return [article.title for article in self.results.articles]
