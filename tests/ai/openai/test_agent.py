from unittest.mock import patch

from lightman_ai.ai.openai.agent import OpenAIAgent
from lightman_ai.article.models import SelectedArticlesList


class TestAgent:
    agent = OpenAIAgent("gpt-4.1")

    def test__run_prompt_multiple_times(self, test_prompt: str) -> None:
        """Test that we run the prompt as many times as we specify, and we receive back a LIST of `SelectedArticlesList`."""
        with patch("lightman_ai.ai.openai.agent.OpenAIAgent._run_prompt") as mock:
            mock.return_value = SelectedArticlesList(articles=[])
            result = self.agent._run_prompt_multiple_times(test_prompt, iterations=3)

        assert mock.call_count == 3
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(x, SelectedArticlesList) for x in result)
