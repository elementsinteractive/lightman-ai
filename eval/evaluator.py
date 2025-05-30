import logging
import time

import click
from dotenv import load_dotenv
from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.ai.prompts import PROMPTS_CHOICES, get_prompt
from hackerman_ai.ai.utils import MODEL_CHOICES, get_agent_instance_from_model_name
from hackerman_ai.article.models import Article, ArticlesList
from hackerman_ai.core.settings import settings
from hackerman_ai.main import _classify_articles

from eval.classified_articles import NON_RELEVANT_ARTICLES, RELEVANT_ARTICLES
from eval.constants import DEFAULT_MODEL
from eval.templates import ResultsFileBuilder
from eval.utils import ClassifiedArticleResults, ResultsMetrics

logger = logging.getLogger("eval")


def classify_articles(
    agent: BaseAgent,
    prompt: str,
    score: int,
    iterations: int,
    relevant_articles: set[Article],
    non_relevant_articles: set[Article],
) -> ClassifiedArticleResults:
    if overlapping_articles := relevant_articles & non_relevant_articles:
        logger.warning("These articles are in both relevant and non-relevant sets! %s", overlapping_articles)

    articles = ArticlesList(articles=list(relevant_articles) + list(non_relevant_articles))

    time_before = time.perf_counter()
    results = _classify_articles(
        articles=articles,
        prompt=prompt,
        agent=agent,
        iterations=iterations,
    )
    time_delta = round(time.perf_counter() - time_before, 2)

    if len(results.articles) != len(relevant_articles) + len(non_relevant_articles):
        # Sometimes, some LLM models fail to return all the articles
        # even if explicitly told so
        logger.error(
            "Not all articles were retrieved. Got %s, expected %s",
            len(results.articles),
            len(relevant_articles) + len(non_relevant_articles),
        )

    correctly_found_articles = set()
    false_positives = set()

    articles_above_threshold = results.get_articles_with_score_gte_threshold(score)
    for article in articles_above_threshold:
        if article in relevant_articles:
            correctly_found_articles.add(article)
        elif article in non_relevant_articles:
            false_positives.add(article)
        else:
            logger.error("%s is not present either in relevant_articles nor in non_relevant_articles", article)

    false_negatives_no_score = set(relevant_articles).difference(correctly_found_articles)

    # We cannot use here `set(results.articles).insterection(false_negatives_no_score)` to retrieve
    # the `SelectedArticle`s classified as false negatives.
    # The reason is that even if `Article` and `SelectedArticle` can be compared against each other
    # because of our implementation, it is not guaranteed that doing and intersection of
    # selected_article_object_set & article_object_set will return `SelectedArticle` object,
    # as per Python implementation it will pick up the one that's optimum to select
    # wich can be an instance of `Article` instead.
    # Because of this, we have to manually craft the set.
    false_negatives = {article for article in results.articles if article in false_negatives_no_score}

    return ClassifiedArticleResults(
        articles=articles_above_threshold,
        correctly_found_articles=correctly_found_articles,
        false_positives=false_positives,
        false_negatives=false_negatives,
        total_relevant_articles=len(relevant_articles),
        time_delta=time_delta,
    )


@click.command()
@click.option("--tag", type=str, help=("Tag that identifies the run"), default=None)
@click.option(
    "--model", type=click.Choice(MODEL_CHOICES), help=("The model to use to analyze articles"), default=DEFAULT_MODEL
)
@click.option("--iterations", type=int, help=("Number of times that the prompt will run"), default=1)
@click.option("--score", type=int, help=("Minimum score to consider an article to be relevant"), default=None)
@click.option(
    "--samples",
    type=int,
    help=(
        "Number of times the evaluation will run with all its iterations. It will calculate averages for the results. "
    ),
    default=1,
)
@click.option("--prompt", type=click.Choice(PROMPTS_CHOICES), help=("Which prompt to use."), default="eval")
def eval(model: str, iterations: int, score: int, samples: int, prompt: str, tag: str | None = None) -> None:
    if samples < 1:
        raise click.BadParameter("`samples` must be > 0.")

    agent = get_agent_instance_from_model_name(model)

    classified_articles = []
    for _ in range(samples):
        classified_articles.append(
            classify_articles(
                agent=agent,
                prompt=get_prompt(prompt),
                score=score or settings.RELEVANCE_SCORE_THRESHOLD,
                iterations=iterations,
                relevant_articles=RELEVANT_ARTICLES,
                non_relevant_articles=NON_RELEVANT_ARTICLES,
            )
        )
    results_metrics = ResultsMetrics(raw_results=classified_articles)
    results_template = ResultsFileBuilder(
        results_metrics=results_metrics,
        tag=tag,
        model=model,
        iterations=iterations,
        samples=samples,
        prompt=get_prompt(prompt),
        score=score,
    )

    logger.debug(results_template.content)
    with open(results_template.file_name, "w") as fp:
        fp.write(results_template.content)


if __name__ == "__main__":
    load_dotenv()
    eval()
