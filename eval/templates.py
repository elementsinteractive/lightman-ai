from datetime import date
from pathlib import Path

from eval.utils import ClassifiedArticleResults

RESULTS_DIR = "eval/results/"


class ResultsFileBuilder:
    def __init__(
        self, classified_article: ClassifiedArticleResults, tag: str | None, model: str, iterations: int
    ) -> None:
        self.classified_article = classified_article
        self.tag = tag
        self.model = model
        self.iterations = iterations

    @property
    def file_name(self) -> str:
        path = str(Path(RESULTS_DIR) / date.today().isoformat()) + f"-{self.model}-iterations-{self.iterations}"

        if self.tag:
            path += f"-{self.tag}"

        return path + ".md"

    @property
    def content(self) -> str:
        return self._get_summary() + "\n" + self._get_individual_run_results()

    def _get_summary(self) -> str:
        return f"""
# Summary
- Tag: {self.tag or "-"}
- Model: {self.model}
- Iterations: {self.iterations}
"""

    def _get_individual_run_results(self) -> str:
        return f"""
#Individual run results

## Results
Total relevant articles: {self.classified_article.total_relevant_articles}
Total articles found by AI agent: {self.classified_article.total_results}
Total relevant articles found: {self.classified_article.total_correctly_found_articles}
Total false positives: {self.classified_article.total_false_positives}
Total false negatives: {self.classified_article.total_false_negatives}
Recall: {self.classified_article.recall}
Precision: {self.classified_article.precision}

## Articles found by AI agent:
{self._titles_to_bullet_list(self.classified_article.articles_found_titles)}

## Correctly classified articles:
{self._titles_to_bullet_list(self.classified_article.correctly_found_articles_titles)}

## False positives:
{self._titles_to_bullet_list(self.classified_article.false_positives_titles)}

## False negatives:
{self._titles_to_bullet_list(self.classified_article.false_negatives_titles)}
"""

    @staticmethod
    def _titles_to_bullet_list(titles: list[str]) -> str:
        return "- " + "\n- ".join(titles)
