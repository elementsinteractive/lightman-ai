import inspect
from dataclasses import dataclass
from decimal import Decimal

from hackerman_ai.article.models import Article, SelectedArticle, SelectedArticlesList


@dataclass
class ClassifiedArticleResults:
    results: SelectedArticlesList
    correctly_found_articles: set[SelectedArticle]
    false_positives: set[SelectedArticle]
    false_negatives: set[Article]
    total_relevant_articles: int
    time_delta: float

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


@dataclass
class ResultsMetrics:
    raw_results: list[ClassifiedArticleResults]

    def _calculate_average(self, field: str) -> Decimal:
        def is_field_on_classified_articles_results() -> bool:
            properties = [
                name for name, obj in inspect.getmembers(ClassifiedArticleResults) if isinstance(obj, property)
            ]

            return field in properties or field in ClassifiedArticleResults.__dataclass_fields__

        if not is_field_on_classified_articles_results():
            raise KeyError(f"`{field}` is not a field of ClassifiedArticleResults")

        if not self.raw_results:
            return Decimal(0)

        average = Decimal(sum([getattr(result, field) for result in self.raw_results]) / len(self.raw_results))
        return round(average, 2)

    @property
    def average_recall(self) -> Decimal:
        return self._calculate_average("recall")

    @property
    def average_precision(self) -> Decimal:
        return self._calculate_average("precision")

    @property
    def average_time_delta(self) -> Decimal:
        return self._calculate_average("time_delta")
