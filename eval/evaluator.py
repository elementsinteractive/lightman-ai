import logging

from lightman_ai.ai.utils import get_agent_instance_from_model_name
from lightman_ai.article.models import Article

from eval.classifier import Classifier
from eval.templates import ResultsFileBuilder
from eval.utils import ResultsMetrics

logger = logging.getLogger("eval")


def eval(
    prompt: str,
    score_threshold: int,
    iterations: int,
    relevant_articles: set[Article],
    non_relevant_articles: set[Article],
    samples: int,
    tag: str | None,
    model: str,
) -> None:
    classified_articles = Classifier(
        agent=get_agent_instance_from_model_name(model),
        prompt=prompt,
        score=score_threshold,
        iterations=iterations,
        relevant_articles=relevant_articles,
        non_relevant_articles=non_relevant_articles,
        samples=samples,
    ).run()

    results_metrics = ResultsMetrics(raw_results=classified_articles)
    results_template = ResultsFileBuilder(
        results_metrics=results_metrics,
        tag=tag,
        model=model,
        iterations=iterations,
        samples=samples,
        prompt=prompt,
        score=score_threshold,
        logger=logger,
    )

    results_template.save()
