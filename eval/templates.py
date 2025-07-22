import logging
from datetime import date
from decimal import Decimal
from pathlib import Path

from eval.utils import ClassifiedArticleResults, ResultsMetrics

RESULTS_DIR = "eval/results/"


class ResultsFileBuilder:
    def __init__(
        self,
        results_metrics: ResultsMetrics,
        tag: str | None,
        agent: str,
        samples: int,
        prompt: str,
        score: int,
        model: str,
        logger: logging.Logger | None = None,
    ) -> None:
        self.results_metrics = results_metrics
        self.tag = tag
        self.agent = agent
        self.samples = samples
        self.prompt = prompt
        self.score = score
        self.results_dir = Path(RESULTS_DIR)
        self.model = model
        self.logger = logger or logging.getLogger("eval")

    @property
    def file_name(self) -> str:
        path = str(self.results_dir / date.today().isoformat()) + f"-{self.agent}-samples-{self.samples}"

        if self.tag:
            path += f"-{self.tag}"

        return path + ".md"

    @property
    def content(self) -> str:
        return self._get_summary() + "\n" + self._get_results_averages() + "\n" + self._get_run_results()

    def save(self) -> None:
        if not self.results_dir.exists():
            self.results_dir.mkdir()

        with open(self.file_name, "w") as fp:
            fp.write(self.content)

        self.logger.warning("\nSaved contents to file %s", self.file_name)

    def _get_summary(self) -> str:
        return f"""
# Summary
- Tag: {self.tag or "-"}
- Agent: {self.agent}
- Model: {self.model}
- Samples: {self.samples}
- Score threshold: {self.score}
- Prompt: \n {self.prompt}
"""

    def _get_results_averages(self) -> str:
        return f"""
- Average Recall: {self.results_metrics.average_recall}, 95% CI: {self._format_interval(self.results_metrics.confidence_interval_recall)}
- Average Precision: {self.results_metrics.average_precision}, 95% CI: {self._format_interval(self.results_metrics.confidence_interval_precision)}
- Average Time Delta: {self.results_metrics.average_time_delta}s
- Average F1 Score: {self.results_metrics.average_f1_score}
"""

    def _get_run_results(self) -> str:
        individual_run_header = "# Individual sample results"
        results = [
            self._get_individual_run_results(sample + 1, result)
            for sample, result in enumerate(self.results_metrics.raw_results)
        ]
        return individual_run_header + "\n".join(results)

    def _get_individual_run_results(self, sample: int, classified_article: ClassifiedArticleResults) -> str:
        return f"""

## Result {sample}
- Total relevant articles: {classified_article.total_relevant_articles}
- Total articles found by AI agent: {classified_article.total_results}
- Total relevant articles found: {classified_article.total_correctly_found_articles}
- Total false positives: {classified_article.total_false_positives}
- Total false negatives: {classified_article.total_false_negatives}
- Recall: {classified_article.recall}
- Precision: {classified_article.precision}
- Time delta: {classified_article.time_delta}s

## Articles found by AI agent:
{self.metadata_to_bullet_list(classified_article.articles_found_metadata)}

## Correctly classified articles:
{self.metadata_to_bullet_list(classified_article.correctly_found_articles_metadata)}

## False positives:
{self.metadata_to_bullet_list(classified_article.false_positives_metadata)}

## False negatives:
{self.metadata_to_bullet_list(classified_article.false_negatives_metadata)}
"""

    @staticmethod
    def metadata_to_bullet_list(metadata: list[str]) -> str:
        if not metadata:
            return "No results."

        return "- " + "\n- ".join(metadata)

    @staticmethod
    def _format_interval(interval: tuple[Decimal, Decimal]) -> str:
        return f"[{str(interval[0])}, {str(interval[1])}]"
