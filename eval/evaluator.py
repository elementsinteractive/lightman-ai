import logging

from lightman_ai.ai.utils import get_agent_class_from_agent_name
from lightman_ai.article.models import Article

from eval.classifier import Classifier
from eval.templates import ResultsFileBuilder
from eval.utils import ResultsMetrics

logger = logging.getLogger("eval")


def eval(
    *,
    prompt: str,
    score_threshold: int,
    relevant_articles: set[Article],
    non_relevant_articles: set[Article],
    samples: int,
    tag: str | None,
    agent: str,
    model: str | None,
    parallel_workers: int = 1,
    sources: list[str] | None = None,
) -> None:
    agent_class = get_agent_class_from_agent_name(agent)
    classified_articles = Classifier(
        agent=agent_class(prompt, model=model),
        score=score_threshold,
        relevant_articles=relevant_articles,
        non_relevant_articles=non_relevant_articles,
        samples=samples,
        workers=parallel_workers,
    ).run()

    results_metrics = ResultsMetrics(raw_results=classified_articles)
    results_template = ResultsFileBuilder(
        results_metrics=results_metrics,
        tag=tag,
        agent=agent,
        samples=samples,
        sources=sources or ["predefined_articles"],
        prompt=prompt,
        score=score_threshold,
        logger=logger,
        model=model or agent_class._DEFAULT_MODEL_NAME,
    )

    results_template.save()
