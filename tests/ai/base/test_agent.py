from typing import override
from unittest.mock import Mock, patch

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.article.models import ArticlesList, SelectedArticlesList


class FakeAgent(BaseAgent):
    _AGENT_CLASS = Mock()
    _DEFAULT_MODEL_NAME = "default model name"
    _AGENT_NAME = "Fake"

    @override
    async def run_prompt(self, prompt: str) -> SelectedArticlesList:
        return SelectedArticlesList(articles=[])


class TestBaseAgent:
    @patch("lightman_ai.ai.base.agent.Agent")
    async def test__get_prompt_result(self, m_agent: Mock, test_prompt: str, thn_news: ArticlesList) -> None:
        """Check that we receive an instance of `SelectedArticlesList` when running the method."""
        agent = FakeAgent(test_prompt)

        with patch("tests.ai.base.test_agent.FakeAgent.run_prompt") as m_run_prompt:
            await agent.run_prompt(str(thn_news))

        assert m_run_prompt.call_count == 1
        assert m_run_prompt.call_args[0][0] == str(thn_news)
        assert m_agent.call_count == 1
        assert m_agent.call_args[1]["system_prompt"] == test_prompt
        assert agent._AGENT_CLASS.call_args[0][0] == FakeAgent._DEFAULT_MODEL_NAME

    @patch("lightman_ai.ai.base.agent.Agent")
    async def test_agent_is_intantiated_with_model_when_set(self, m_agent: Mock, test_prompt: str) -> None:
        agent = FakeAgent(test_prompt, model="my model")
        await agent.run_prompt("")

        assert m_agent.call_count == 1
        assert agent._AGENT_CLASS.call_args[0][0] == "my model"
