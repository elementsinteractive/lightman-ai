import logging

from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.ai.prompts import Prompts, add_articles_to_prompt
from hackerman_ai.ai.utils import get_agent_instance_from_model_name
from hackerman_ai.article.models import ArticlesList
from hackerman_ai.article.processor import Processor
from hackerman_ai.core.settings import settings
from hackerman_ai.sources.the_hacker_news import TheHackerNewsSource

logger = logging.getLogger("hackerman")


async def _get_articles() -> ArticlesList:
    return await TheHackerNewsSource().get_articles()


async def _classify_articles(articles: ArticlesList, agent: BaseAgent, iterations: int) -> ArticlesList:
    prompt = add_articles_to_prompt(Prompts.SHORT_PROMPT, articles)

    logger.info("Selected %s.", agent)
    results = await agent.get_prompt_result(prompt, iterations)

    return Processor(original_articles=articles, selected_articles=results).process()


async def hackerman(model: str, iterations: int | None = None) -> ArticlesList:
    articles = await _get_articles()

    agent = get_agent_instance_from_model_name(model)
    logger.info("Selected %s.", agent)

    classified_articles = await _classify_articles(articles, agent, iterations or settings.PROMPT_ITERATIONS)
    logger.warning("Found these articles: %s", classified_articles.titles)
    return classified_articles
