import logging

from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.ai.utils import get_agent_instance_from_model_name
from hackerman_ai.article.models import ArticlesList, SelectedArticle, SelectedArticlesList
from hackerman_ai.sources.the_hacker_news import TheHackerNewsSource

logger = logging.getLogger("hackerman")


def _get_articles() -> ArticlesList:
    return TheHackerNewsSource().get_articles()


def _merge_prompt_with_articles(prompt: str, articles: ArticlesList) -> str:
    return f"""{prompt}
                This is the json:
                {articles}
            """


def _classify_articles(articles: ArticlesList, prompt: str, agent: BaseAgent, iterations: int) -> SelectedArticlesList:
    full_prompt = _merge_prompt_with_articles(prompt, articles)
    return agent.get_prompt_result(prompt=full_prompt, iterations=iterations)


def hackerman(model: str, prompt: str, score_threshold: int, iterations: int) -> list[SelectedArticle]:
    articles = _get_articles()

    agent = get_agent_instance_from_model_name(model)
    logger.info("Selected %s.", agent)

    classified_articles = _classify_articles(
        articles=articles,
        prompt=prompt,
        agent=agent,
        iterations=iterations,
    )

    logger.warning("Found these articles: %s", classified_articles.titles)

    return classified_articles.get_articles_with_score_gte_threshold(score_threshold)
