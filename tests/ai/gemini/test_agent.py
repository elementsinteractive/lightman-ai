from unittest.mock import patch

import pytest
from lightman_ai.ai.gemini.agent import GeminiAgent
from lightman_ai.ai.gemini.exceptions import GeminiError
from lightman_ai.article.models import SelectedArticlesList
from tests.utils import patch_agent_raise_exception


class TestGeminiAgent:
    agent = GeminiAgent(system_prompt="Test system prompt")

    def test__run_prompt(self, test_prompt: str) -> None:
        """Test that we can run a prompt and receive a SelectedArticlesList."""
        with patch.object(self.agent.agent, "run_sync") as mock:
            mock.return_value.output = SelectedArticlesList(articles=[])
            result = self.agent._run_prompt(test_prompt)

        assert mock.call_count == 1
        assert isinstance(result, SelectedArticlesList)

    def test_gemini_exception(self) -> None:
        with pytest.raises(GeminiError), patch_agent_raise_exception():
            self.agent.get_prompt_result("")
