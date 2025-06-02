import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Never, override

from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.ai.gemini.exceptions import map_gemini_exceptions
from hackerman_ai.article.models import SelectedArticlesList
from hackerman_ai.core.settings import settings
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel


class GeminiAgent(BaseAgent):
    """Class that provides an interface to operate with the Gemini model."""

    def __init__(self, model: str, logger: logging.Logger | None = None) -> None:
        ai_model = GeminiModel(model)
        self.agent: Agent[Never, SelectedArticlesList] = Agent(model=ai_model, output_type=SelectedArticlesList)
        self.logger = logger or logging.getLogger()

    @override
    def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        with map_gemini_exceptions():
            result = self.agent.run_sync(prompt)
        return result.output

    @override
    def _run_prompt_multiple_times(self, prompt: str, iterations: int) -> list[SelectedArticlesList]:
        """Run the prompt multiple times, so that we reduce the number of false negatives.

        Gemini does not raise any error while we are running multiple calls at the same time
        so we can run all of them at once.

        This should be done using async ideally, but pydantic-ai has a bug that in some cases it closes
        the event loop before we've finished running the tasks.
        """
        with ThreadPoolExecutor(max_workers=settings.PARALLEL_WORKERS) as executor:
            results = list(executor.map(self._run_prompt, [prompt for _ in range(iterations)]))
        return results
