from unittest.mock import patch

from lightman_ai.ai.openai.agent import OpenAIAgent
from lightman_ai.article.models import SelectedArticlesList


class TestAgent:
    agent = OpenAIAgent(False, system_prompt="Test system prompt")

    async def test__run_prompt(self, test_prompt: str) -> None:
        """Test that we can run a prompt and receive a SelectedArticlesList."""
        with patch("lightman_ai.ai.openai.agent.OpenAIAgent._execute_agent") as mock:
            mock.return_value.output = SelectedArticlesList(articles=[])
            result = await self.agent.run_prompt(test_prompt)

        assert mock.call_count == 1
        assert isinstance(result, SelectedArticlesList)
