from typing import override

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.ai.gemini.exceptions import map_gemini_exceptions
from lightman_ai.article.models import SelectedArticlesList
from pydantic_ai.models.google import GoogleModel


class GeminiAgent(BaseAgent):
    """Class that provides an interface to operate with the Gemini model."""

    _class = GoogleModel
    _default_model_name = "gemini-2.5-pro-preview-05-06"

    @override
    def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        with map_gemini_exceptions():
            result = self.agent.run_sync(prompt)
        return result.output
