import logging

from hackerman_ai.ai.openai_agent import OpenAIAgent
from hackerman_ai.ai.prompts import Prompts, add_articles_to_prompt
from hackerman_ai.article.processor import Processor
from hackerman_ai.core.settings import settings
from hackerman_ai.sources.the_hacker_news import TheHackerNewsSource

logger = logging.getLogger("hackerman")


async def hackerman() -> int:
    thn_news = await TheHackerNewsSource().get_articles()
    agent = OpenAIAgent()
    prompt = add_articles_to_prompt(Prompts.SHORT_PROMPT, thn_news)
    results = await agent.get_prompt_result(prompt, settings.PROMPT_ITERATIONS, settings.OPENAI_RATE_LIMIT_TIMEOUT)
    processed_articles = Processor(original_articles=thn_news, selected_articles=results).process()

    logger.warning("Found these articles: %s", processed_articles.titles)
    return 0
