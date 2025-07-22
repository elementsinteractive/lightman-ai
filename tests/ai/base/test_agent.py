from typing import override
from unittest.mock import Mock, patch

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.article.models import ArticlesList, SelectedArticlesList


class FakeAgent(BaseAgent):
    _class = Mock()
    _default_model_name = "default model name"

    @override
    def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        return SelectedArticlesList(articles=[])


class TestBaseAgent:
    @patch("lightman_ai.ai.base.agent.Agent")
    def test__get_prompt_result(self, m_agent: Mock, test_prompt: str, thn_news: ArticlesList) -> None:
        """Check that we receive an instance of `SelectedArticlesList` when running the method."""
        agent = FakeAgent(test_prompt)

        with patch("tests.ai.base.test_agent.FakeAgent._run_prompt") as m_run_prompt:
            agent.get_prompt_result(str(thn_news))

        assert m_run_prompt.call_count == 1
        assert m_run_prompt.call_args[0][0] == str(thn_news)
        assert m_agent.call_count == 1
        assert m_agent.call_args[1]["system_prompt"] == test_prompt
        assert agent._class.call_count == 1
        assert agent._class.call_args[0][0] == FakeAgent._default_model_name

    @patch("lightman_ai.ai.base.agent.Agent")
    def test_agent_is_intantiated_with_model_when_set(self, m_agent: Mock, test_prompt: str) -> None:
        agent = FakeAgent(test_prompt, model="my model")
        agent.get_prompt_result("")

        assert m_agent.call_count == 1
        assert agent._class.call_count == 2
        assert agent._class.call_args[0][0] == "my model"
