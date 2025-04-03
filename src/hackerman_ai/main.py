import logging

from hackerman_ai.ai.agent import AIAgent
from hackerman_ai.ai.utils import get_prompt
from hackerman_ai.sources.news import get_thn_news

logger = logging.getLogger("hackerman")


async def hackerman() -> int:
    thn_news = await get_thn_news()
    agent = AIAgent()

    prompt = get_prompt(thn_news)
    await agent.run_prompt(prompt)

    return 0
