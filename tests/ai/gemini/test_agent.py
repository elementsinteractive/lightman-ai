from unittest.mock import patch

import pytest
from hackerman_ai.ai.gemini.agent import GeminiAgent
from hackerman_ai.ai.gemini.exceptions import GeminiError
from hackerman_ai.article.models import SelectedArticlesList
from tests.utils import patch_agent_raise_exception


class TestGeminiAgent:
    agent = GeminiAgent("gemini-2.5-flash-preview-04-17")

    def test__run_prompt_multiple_times(self, test_prompt: str) -> None:
        """Test that we run the prompt as many times as we specify, and we receive back a LIST of `SelectedArticlesList`."""
        with patch("hackerman_ai.ai.gemini.agent.GeminiAgent._run_prompt") as mock:
            mock.return_value = SelectedArticlesList(articles=[])
            result = self.agent._run_prompt_multiple_times(test_prompt, iterations=3)

        assert mock.call_count == 3
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(x, SelectedArticlesList) for x in result)

    def test_gemini_exception(self) -> None:
        with pytest.raises(GeminiError), patch_agent_raise_exception():
            self.agent.get_prompt_result("")
