import asyncio
from typing import Never

from hackerman_ai.article.models import SelectedArticlesList
from hackerman_ai.core.settings import settings
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel


class OpenAIAgent:
    """Class that provides an interface to operate with the OpenAI model."""

    def __init__(self) -> None:
        ai_model = OpenAIModel("gpt-4o", api_key=settings.OPENAI_API_KEY)
        self.agent: Agent[Never, SelectedArticlesList] = Agent(model=ai_model, result_type=SelectedArticlesList)

    async def get_prompt_result(self, prompt: str, iterations: int, rate_limit_timeout: int) -> SelectedArticlesList:
        assert iterations >= 0, "Number of iterations cannot be a negative number."
        assert rate_limit_timeout >= 0, "Rate limit timeout cannot be a negative number."

        articles = await self._run_prompt_multiple_times(prompt, iterations, rate_limit_timeout)
        return self._merge_results(articles)

    async def _run_prompt_multiple_times(
        self, prompt: str, iterations: int, rate_limit_timeout: int
    ) -> list[SelectedArticlesList]:
        tasks = [self._run_prompt_with_delay(prompt, n * rate_limit_timeout) for n in range(iterations)]
        return await asyncio.gather(*tasks)

    async def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        result = await self.agent.run(prompt)
        return result.data

    async def _run_prompt_with_delay(self, prompt: str, delay: int) -> SelectedArticlesList:
        await asyncio.sleep(delay)
        return await self._run_prompt(prompt)

    def _merge_results(self, articles_list_of_lists: list[SelectedArticlesList]) -> SelectedArticlesList:
        """Merge all the news, removing repeated ones."""
        all_articles = set()
        for articles_list in articles_list_of_lists:
            for article in articles_list.articles:
                all_articles.add(article)
        return SelectedArticlesList(articles=list(all_articles))
