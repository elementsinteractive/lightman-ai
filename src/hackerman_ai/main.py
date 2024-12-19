import logging

from hackerman_ai.ai.agent import AIAgent
from hackerman_ai.sources.the_hacker_news import TheHackerNewsSource

logger = logging.getLogger("hackerman")


async def hackerman(api_key: str) -> int:
    news_xml = await TheHackerNewsSource.get_news()
    agent = AIAgent(api_key)
    result = await agent.run_prompt(news_xml)

    logger.debug(result)

    return 0
