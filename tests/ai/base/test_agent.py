import logging
from typing import override
from unittest.mock import Mock

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.article.models import ArticlesList, SelectedArticlesList


class FakeAgent(BaseAgent):
    def __init__(self, system_prompt: str, logger: logging.Logger | None = None) -> None:
        self.agent = Mock()

    @override
    def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        return SelectedArticlesList(articles=[])


class TestBaseAgent:
    def test__get_prompt_result(self, test_prompt: str, thn_news: ArticlesList) -> None:
        """Check that we receive an instance of `SelectedArticlesList` when running the method."""
        agent = FakeAgent(test_prompt)
        result = agent.get_prompt_result(str(thn_news))
        assert isinstance(result, SelectedArticlesList)
