import logging
import time

import click
from dotenv import load_dotenv
from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.ai.prompts import PROMPTS_CHOICES, get_prompt
from hackerman_ai.ai.utils import MODEL_CHOICES, get_agent_instance_from_model_name
from hackerman_ai.article.models import ArticlesList
from hackerman_ai.main import _classify_articles

from eval.classified_articles import NON_RELEVANT_ARTICLES, RELEVANT_ARTICLES
from eval.constants import DEFAULT_MODEL
from eval.templates import ResultsFileBuilder
from eval.utils import ClassifiedArticleResults, ResultsMetrics

logger = logging.getLogger("eval")


def classify_articles(
    articles: ArticlesList, agent: BaseAgent, prompt: str, iterations: int
) -> ClassifiedArticleResults:
    time_before = time.perf_counter()
    results = _classify_articles(articles, prompt, agent, iterations)
    time_delta = round(time.perf_counter() - time_before, 2)

    correctly_found_articles = set()
    false_positives = set()

    for article in results.articles:
        if article in RELEVANT_ARTICLES:
            correctly_found_articles.add(article)
        elif article in NON_RELEVANT_ARTICLES:
            false_positives.add(article)
        else:
            logger.error("%s", article)

    false_negatives = set(RELEVANT_ARTICLES).difference(correctly_found_articles)

    return ClassifiedArticleResults(
        results=results,
        correctly_found_articles=correctly_found_articles,
        false_positives=false_positives,
        false_negatives=false_negatives,
        total_relevant_articles=len(RELEVANT_ARTICLES),
        time_delta=time_delta,
    )


@click.command()
@click.option("--tag", type=str, help=("Tag that identifies the run"), default=None)
@click.option(
    "--model", type=click.Choice(MODEL_CHOICES), help=("The model to use to analyze articles"), default=DEFAULT_MODEL
)
@click.option("--iterations", type=int, help=("Number of times that the prompt will run"), default=1)
@click.option(
    "--samples",
    type=int,
    help=(
        "Number of times the evaluation will run with all its iterations. It will calculate averages for the results. "
    ),
    default=1,
)
@click.option("--prompt", type=click.Choice(PROMPTS_CHOICES), help=("Which prompt to use."), default="eval")
def eval(model: str, iterations: int, samples: int, prompt: str, tag: str | None = None) -> None:
    if samples < 1:
        raise ValueError("`samples` must be > 0.")

    articles = ArticlesList(articles=list(RELEVANT_ARTICLES) + list(NON_RELEVANT_ARTICLES))
    agent = get_agent_instance_from_model_name(model)

    classified_articles = []
    for _ in range(samples):
        classified_articles.append(classify_articles(articles, agent, get_prompt(prompt), iterations))
    results_metrics = ResultsMetrics(raw_results=classified_articles)
    results_template = ResultsFileBuilder(
        results_metrics=results_metrics,
        tag=tag,
        model=model,
        iterations=iterations,
        samples=samples,
        prompt=get_prompt(prompt),
    )

    logger.debug(results_template.content)
    with open(results_template.file_name, "w") as fp:
        fp.write(results_template.content)


if __name__ == "__main__":
    load_dotenv()
    eval()
