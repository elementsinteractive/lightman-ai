import logging
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

import click
from dotenv import load_dotenv
from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.ai.gemini.agent import GeminiAgent
from hackerman_ai.ai.openai.agent import OpenAIAgent
from hackerman_ai.ai.prompts import PROMPTS_CHOICES, get_prompt
from hackerman_ai.ai.utils import MODEL_CHOICES, get_agent_instance_from_model_name
from hackerman_ai.article.models import Article, ArticlesList
from hackerman_ai.core.settings import settings
from hackerman_ai.main import _classify_articles

from eval.classified_articles import NON_RELEVANT_ARTICLES, RELEVANT_ARTICLES
from eval.constants import DEFAULT_MODEL, EVAL_WORKERS, MAX_WORKERS
from eval.templates import ResultsFileBuilder
from eval.utils import ClassifiedArticleResults, ResultsMetrics

logger = logging.getLogger("eval")


@dataclass
class ClassifyArticlesInput:
    agent: BaseAgent
    prompt: str
    score: int
    iterations: int
    relevant_articles: set[Article]
    non_relevant_articles: set[Article]


def classify_articles(input: ClassifyArticlesInput) -> ClassifiedArticleResults:
    if overlapping_articles := input.relevant_articles & input.non_relevant_articles:
        logger.warning("These articles are in both relevant and non-relevant sets! %s", overlapping_articles)

    articles = ArticlesList(articles=list(input.relevant_articles) + list(input.non_relevant_articles))

    time_before = time.perf_counter()
    results = _classify_articles(
        articles=articles,
        prompt=input.prompt,
        agent=input.agent,
        iterations=input.iterations,
    )
    time_delta = round(time.perf_counter() - time_before, 2)

    if len(results.articles) > len(input.relevant_articles) + len(input.non_relevant_articles):
        # Sometimes, some LLM models fail to return all the articles
        # even if explicitly told so
        logger.error(
            "Not all articles were retrieved. Got %s, expected %s",
            len(results.articles),
            len(input.relevant_articles) + len(input.non_relevant_articles),
        )

    correctly_found_articles = set()
    false_positives = set()

    articles_above_threshold = results.get_articles_with_score_gte_threshold(input.score)
    for article in articles_above_threshold:
        if article in input.relevant_articles:
            correctly_found_articles.add(article)
        elif article in input.non_relevant_articles:
            false_positives.add(article)
        else:
            logger.error("%s is not present either in relevant_articles nor in non_relevant_articles", article)

    false_negatives_no_score = set(input.relevant_articles).difference(correctly_found_articles)

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
        total_relevant_articles=len(input.relevant_articles),
        time_delta=time_delta,
    )


def can_run_in_parallel(agent: BaseAgent) -> bool:
    if isinstance(agent, OpenAIAgent):
        return False
    if isinstance(agent, GeminiAgent):
        return True
    raise RuntimeError(f"No information about if it is possible running `{agent}` in parallel.")


def parallel_run(classify_articles_input: ClassifyArticlesInput, samples: int) -> list[ClassifiedArticleResults]:
    if EVAL_WORKERS + settings.PARALLEL_WORKERS > MAX_WORKERS:
        raise RuntimeError("Too many workers specified while running `eval`.")

    with ThreadPoolExecutor(max_workers=EVAL_WORKERS) as executor:
        return list(executor.map(classify_articles, [classify_articles_input for _ in range(samples)]))


def sync_run(classify_articles_input: ClassifyArticlesInput, samples: int) -> list[ClassifiedArticleResults]:
    return [classify_articles(classify_articles_input) for _ in range(samples)]


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

    score_threshold = score or settings.RELEVANCE_SCORE_THRESHOLD
    classify_articles_input = ClassifyArticlesInput(
        agent=agent,
        prompt=get_prompt(prompt),
        score=score_threshold,
        iterations=iterations,
        relevant_articles=RELEVANT_ARTICLES,
        non_relevant_articles=NON_RELEVANT_ARTICLES,
    )

    if can_run_in_parallel(agent):
        classified_articles = parallel_run(classify_articles_input, samples)
    else:
        classified_articles = sync_run(classify_articles_input, samples)

    results_metrics = ResultsMetrics(raw_results=classified_articles)
    results_template = ResultsFileBuilder(
        results_metrics=results_metrics,
        tag=tag,
        model=model,
        iterations=iterations,
        samples=samples,
        prompt=get_prompt(prompt),
        score=score_threshold,
    )

    logger.debug(results_template.content)
    with open(results_template.file_name, "w") as fp:
        fp.write(results_template.content)


if __name__ == "__main__":
    load_dotenv()
    eval()
