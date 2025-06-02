from unittest.mock import patch

import pytest
from hackerman_ai.ai.gemini.agent import GeminiAgent
from hackerman_ai.article.models import SelectedArticlesList


class TestGeminiAgent:
    agent = GeminiAgent("gemini-2.5-flash-preview-04-17")

    @pytest.mark.vcr
    def test__run_prompt(self, test_prompt: str) -> None:
        result = self.agent._run_prompt(test_prompt)
        assert isinstance(result, SelectedArticlesList)

    def test__run_prompt_multiple_times(self, test_prompt: str) -> None:
        """Test that we run the prompt as many times as we specify, and we receive back a LIST of `SelectedArticlesList`."""
        with patch("hackerman_ai.ai.gemini.agent.GeminiAgent._run_prompt") as mock:
            mock.return_value = SelectedArticlesList(articles=[])
            result = self.agent._run_prompt_multiple_times(test_prompt, iterations=3)

        assert mock.call_count == 3
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(x, SelectedArticlesList) for x in result)
