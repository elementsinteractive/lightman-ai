import inspect
from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from lightman_ai.core.config import FileConfig, FinalConfig
from lightman_ai.core.settings import Settings
from pydantic import PositiveInt  # noqa: TC002

if TYPE_CHECKING:
    from collections.abc import Iterable

    from lightman_ai.article.models import SelectedArticle


class EvalSettings(Settings):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    PARALLEL_WORKERS: int = 5


def init_eval_settings(env_file: str | None = None) -> EvalSettings:
    return EvalSettings(_env_file=env_file)


class EvalConfig(FinalConfig):
    samples: PositiveInt


class EvalFileConfig(FileConfig):
    samples: int | None = None


@dataclass
class ClassifiedArticleResults:
    articles: list[SelectedArticle]
    correctly_found_articles: set[SelectedArticle]
    false_positives: set[SelectedArticle]
    false_negatives: set[SelectedArticle]
    total_relevant_articles: int
    time_delta: float

    @property
    def total_results(self) -> int:
        return len(self.articles)

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
    def f1_score(self) -> Decimal:
        return _compute_f1_score(self.precision, self.recall)

    @property
    def false_positives_metadata(self) -> list[str]:
        return self._get_articles_metadata(self.false_positives)

    @property
    def correctly_found_articles_metadata(self) -> list[str]:
        return self._get_articles_metadata(self.correctly_found_articles)

    @property
    def false_negatives_metadata(self) -> list[str]:
        return self._get_articles_metadata(self.false_negatives)

    @property
    def articles_found_metadata(self) -> list[str]:
        return self._get_articles_titles(self.articles)

    @staticmethod
    def _get_articles_titles(articles: Iterable[SelectedArticle]) -> list[str]:
        return [article.title for article in articles]

    @staticmethod
    def _get_articles_metadata(articles: set[SelectedArticle]) -> list[str]:
        return [
            f"Title: {article.title}\n\t- Reason: {article.why_is_relevant}\n\t- Score: {article.relevance_score}"
            for article in articles
        ]


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
    def confidence_interval_recall(self) -> tuple[Decimal, Decimal]:
        return _compute_confidence_interval([result.recall for result in self.raw_results])

    @property
    def confidence_interval_precision(self) -> tuple[Decimal, Decimal]:
        return _compute_confidence_interval([result.precision for result in self.raw_results])

    @property
    def average_time_delta(self) -> Decimal:
        return self._calculate_average("time_delta")

    @property
    def average_f1_score(self) -> Decimal:
        return _compute_f1_score(self.average_precision, self.average_recall)


def _compute_f1_score(precision: Decimal, recall: Decimal) -> Decimal:
    if precision + recall == 0:
        return Decimal(0)
    return round(Decimal(2 * (precision * recall) / (precision + recall)), 2)


def _compute_confidence_interval(values: list[Decimal]) -> tuple[Decimal, Decimal]:
    """Compute the 95% confidence interval for a list of values.

    Assumes a t-distribution for small sample sizes.
    """
    n = len(values)
    if n < 3:
        # We just cannot compute a confidence interval with less than 3 samples
        return Decimal("NaN"), Decimal("NaN")

    # Compute mean
    mean = sum(values) / Decimal(n)

    # Compute sample standard deviation (ddof=1)
    squared_diffs = [(x - mean) ** 2 for x in values]
    variance = sum(squared_diffs) / Decimal(n - 1)
    stdev = variance.sqrt()

    # t-critical value for 95% CI (two-tailed) with df=n-1

    # For small n, we hardcode values (source: t-distribution table)
    t_critical_values = {
        1: 12.706,
        2: 4.303,
        3: 3.182,
        4: 2.776,
        5: 2.571,
        6: 2.447,
        7: 2.365,
        8: 2.306,
        9: 2.262,
        10: 2.228,
    }

    df = n - 1
    t_critical = Decimal(str(t_critical_values.get(df, 2.0)))  # fallback to 2.0 if df > 10

    # Margin of error
    margin_error = t_critical * (stdev / Decimal(n).sqrt())

    # Confidence interval
    ci_lower = max(Decimal(0), mean - margin_error)
    ci_upper = min(Decimal(1), mean + margin_error)

    return round(ci_lower, 2), round(ci_upper, 2)
