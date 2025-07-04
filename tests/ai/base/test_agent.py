from typing import override

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.article.models import SelectedArticlesList


class FakeAgent(BaseAgent):
    @override
    def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        return SelectedArticlesList(articles=[])


class TestBaseAgent:
    def test__get_prompt_result(self, test_prompt: str) -> None:
        """Check that we receive an instance of `SelectedArticlesList` when running the method."""
        agent = FakeAgent()
        result = agent.get_prompt_result(test_prompt)
        assert isinstance(result, SelectedArticlesList)
