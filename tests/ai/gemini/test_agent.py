import pytest
from hackerman_ai.ai.gemini.agent import GeminiAgent
from hackerman_ai.article.models import SelectedArticlesList


class TestGeminiAgent:
    MODEL = "gemini-2.5-flash-preview-04-17"

    @pytest.mark.vcr
    def test__run_prompt(self, short_prompt: str) -> None:
        agent = GeminiAgent(self.MODEL)
        result = agent._run_prompt(short_prompt)
        assert isinstance(result, SelectedArticlesList)
