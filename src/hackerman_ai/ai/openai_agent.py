import asyncio
from typing import Never

from hackerman_ai.ai.models import News
from hackerman_ai.core.settings import settings
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel


class OpenAIAgent:
    """Class that provides an interface to operate with the OpenAI model."""

    def __init__(self) -> None:
        ai_model = OpenAIModel("gpt-4o", api_key=settings.OPENAI_API_KEY)
        self.agent: Agent[Never, News] = Agent(model=ai_model, result_type=News)

    async def get_prompt_result(self, prompt: str, iterations: int, rate_limit_timeout: int) -> News:
        news_list = await self._run_prompt_multiple_times(prompt, iterations, rate_limit_timeout)
        return self._merge_results(news_list)

    async def _run_prompt_multiple_times(self, prompt: str, iterations: int, rate_limit_timeout: int) -> list[News]:
        tasks = [self._run_prompt_with_delay(prompt, n * rate_limit_timeout) for n in range(iterations)]
        return await asyncio.gather(*tasks)

    async def _run_prompt(self, prompt: str) -> News:
        result = await self.agent.run(prompt)
        return result.data

    async def _run_prompt_with_delay(self, prompt: str, delay: int) -> News:
        await asyncio.sleep(delay)
        return await self._run_prompt(prompt)

    def _merge_results(self, news_list: list[News]) -> News:
        """Merge all the news, removing repeated ones."""
        all_news = set()
        for news in news_list:
            for new in news.news:
                all_news.add(new)
        return News(news=list(all_news))
