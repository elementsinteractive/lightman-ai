import logging

from hackerman_ai.ai.openai_agent import OpenAIAgent
from hackerman_ai.ai.utils import get_prompt
from hackerman_ai.core.settings import settings
from hackerman_ai.sources.news import get_thn_news

logger = logging.getLogger("hackerman")


async def hackerman() -> int:
    thn_news = await get_thn_news()
    agent = OpenAIAgent()
    prompt = get_prompt(thn_news)
    results = await agent.get_prompt_result(prompt, settings.PROMPT_ITERATIONS, settings.OPENAI_RATE_LIMIT_TIMEOUT)
    logger.warning("Found these news: %s", results.titles)
    return 0
