import logging

from hackerman_ai.ai.prompts import Prompts, add_articles_to_prompt
from hackerman_ai.ai.utils import get_agent_from_model_name
from hackerman_ai.article.processor import Processor
from hackerman_ai.core.settings import settings
from hackerman_ai.sources.the_hacker_news import TheHackerNewsSource

logger = logging.getLogger("hackerman")


async def hackerman(model: str) -> int:
    thn_news = await TheHackerNewsSource().get_articles()
    prompt = add_articles_to_prompt(Prompts.SHORT_PROMPT, thn_news)

    agent = get_agent_from_model_name(model)
    logger.info("Selected %s.", agent)
    results = await agent.get_prompt_result(prompt, settings.PROMPT_ITERATIONS)

    processed_articles = Processor(original_articles=thn_news, selected_articles=results).process()

    logger.warning("Found these articles: %s", processed_articles.titles)
    return 0
