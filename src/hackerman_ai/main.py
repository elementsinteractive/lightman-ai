import logging

from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.ai.prompts import merge_prompt_with_articles
from hackerman_ai.ai.utils import get_agent_instance_from_model_name
from hackerman_ai.article.models import ArticlesList, SelectedArticlesList
from hackerman_ai.core.settings import settings
from hackerman_ai.sources.the_hacker_news import TheHackerNewsSource

logger = logging.getLogger("hackerman")


def _get_articles() -> ArticlesList:
    return TheHackerNewsSource().get_articles()


def _classify_articles(articles: ArticlesList, prompt: str, agent: BaseAgent, iterations: int) -> SelectedArticlesList:
    full_prompt = merge_prompt_with_articles(prompt, articles)
    logger.info("Selected %s.", agent)
    return agent.get_prompt_result(full_prompt, iterations)


def hackerman(model: str, prompt: str, iterations: int | None = None) -> SelectedArticlesList:
    articles = _get_articles()

    agent = get_agent_instance_from_model_name(model)
    logger.info("Selected %s.", agent)

    classified_articles = _classify_articles(articles, prompt, agent, iterations or settings.PROMPT_ITERATIONS)
    logger.warning("Found these articles: %s", classified_articles.titles)
    return classified_articles
