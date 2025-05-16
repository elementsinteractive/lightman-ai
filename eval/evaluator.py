import asyncio
import logging
from datetime import date
from pathlib import Path

import click
from dotenv import load_dotenv
from hackerman_ai.article.models import Article, ArticlesList
from hackerman_ai.main import _classify_articles

from eval.classified_articles import NON_RELEVANT_ARTICLES, RELEVANT_ARTICLES

RESULTS_DIR = "eval/results/"
logger = logging.getLogger("eval")


def get_results_fname(tag: str) -> str:
    return str(Path(RESULTS_DIR) / date.today().isoformat()) + f"-{tag}.md"


def get_results_template(
    results: ArticlesList,
    correctly_found_articles: set[Article],
    false_positives: set[Article],
    false_negatives: set[Article],
    relevant_articles: set[Article],
    non_relevant_articles: set[Article],
) -> str:
    def titles_to_bullet_list(titles: list[str]) -> str:
        return "- " + "\n- ".join(titles)

    total_results = len(results.articles)
    total_correctly_found_articles = len(correctly_found_articles)
    total_relevant_articles = len(relevant_articles)
    total_false_negatives = len(false_negatives)
    total_false_positives = len(false_positives)

    articles_found_titles_str = titles_to_bullet_list(results.titles)
    correctly_found_articles_titles_str = titles_to_bullet_list([article.title for article in correctly_found_articles])
    false_positives_titles_str = titles_to_bullet_list([article.title for article in false_positives])
    false_negatives_titles_str = titles_to_bullet_list([article.title for article in false_negatives])

    return f"""
# Results
Total relevant articles: {total_relevant_articles}
Total articles found by AI agent: {total_results}
Total relevant articles found: {total_correctly_found_articles}
Total false positives: {total_false_positives}
Total false negatives: {total_false_negatives}
Recall: {total_correctly_found_articles / (total_correctly_found_articles + total_false_negatives)}
Precision: {total_correctly_found_articles / (total_correctly_found_articles + total_false_positives)}

# Articles found by AI agent:
{articles_found_titles_str}

# Correctly classified articles:
{correctly_found_articles_titles_str}

# False positives:
{false_positives_titles_str}

# False negatives:
{false_negatives_titles_str}

"""


@click.command()
@click.option("--tag", type=str, help=("Tag that identifies the evaluation run"), required=True)
def eval(tag: str) -> None:
    articles = ArticlesList(articles=list(RELEVANT_ARTICLES) + list(NON_RELEVANT_ARTICLES))
    results = asyncio.run(_classify_articles(articles, "openai"))

    correctly_found_articles = set()
    false_positives = set()

    for article in results.articles:
        if article in RELEVANT_ARTICLES:
            correctly_found_articles.add(article)
        elif article in NON_RELEVANT_ARTICLES:
            false_positives.add(article)
        else:
            logger.error("%s", article)

    false_negatives = RELEVANT_ARTICLES - correctly_found_articles
    results_template = get_results_template(
        results, correctly_found_articles, false_positives, false_negatives, RELEVANT_ARTICLES, NON_RELEVANT_ARTICLES
    )
    logger.warning(results_template)
    with open(get_results_fname(tag), "w") as fp:
        fp.write(results_template)


if __name__ == "__main__":
    load_dotenv()
    eval()
