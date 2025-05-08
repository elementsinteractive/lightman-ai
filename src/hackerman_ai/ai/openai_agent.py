import asyncio
from typing import Never

from hackerman_ai.ai.exceptions import LimitTokensExceededError, map_exceptions
from hackerman_ai.article.models import SelectedArticlesList
from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from pydantic_ai.models.openai import OpenAIModel


class OpenAIAgent:
    """Class that provides an interface to operate with the OpenAI model."""

    def __init__(self) -> None:
        ai_model = OpenAIModel("gpt-4o")
        self.agent: Agent[Never, SelectedArticlesList] = Agent(model=ai_model, output_type=SelectedArticlesList)

    async def get_prompt_result(self, prompt: str, iterations: int = 1) -> SelectedArticlesList:
        assert iterations > 0, "Number of iterations must be > 0."

        articles = await self._run_prompt_multiple_times(prompt, iterations)
        return self._merge_results(articles)

    async def _run_prompt_multiple_times(self, prompt: str, iterations: int) -> list[SelectedArticlesList]:
        results = []
        for _ in range(iterations):
            results.append(await self._run_prompt(prompt))
        return results

    async def _execute_agent(self, prompt: str) -> AgentRunResult[SelectedArticlesList]:
        async with map_exceptions():
            return await self.agent.run(prompt)

    async def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        try:
            result = await self._execute_agent(prompt)
        except LimitTokensExceededError as err:
            await asyncio.sleep(err.wait_time)
            result = await self._execute_agent(prompt)

        return result.data

    def _merge_results(self, articles_list_of_lists: list[SelectedArticlesList]) -> SelectedArticlesList:
        """Merge all the news, removing repeated ones."""
        all_articles = set()
        for articles_list in articles_list_of_lists:
            for article in articles_list.articles:
                all_articles.add(article)
        return SelectedArticlesList(articles=list(all_articles))
