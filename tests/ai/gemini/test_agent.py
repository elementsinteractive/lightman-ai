from unittest.mock import patch

import pytest
from lightman_ai.ai.gemini.agent import GeminiAgent
from lightman_ai.ai.gemini.exceptions import GeminiError
from lightman_ai.article.models import SelectedArticlesList
from tests.utils import patch_agent_raise_exception


class TestGeminiAgent:
    agent = GeminiAgent(False, system_prompt="Test system prompt")

    async def test__run_prompt(self, test_prompt: str) -> None:
        """Test that we can run a prompt and receive a SelectedArticlesList."""
        with patch.object(self.agent.agent, "run") as mock:
            mock.return_value.output = SelectedArticlesList(articles=[])
            result = await self.agent.run_prompt(test_prompt)

        assert mock.call_count == 1
        assert isinstance(result, SelectedArticlesList)

    async def test_gemini_exception(self) -> None:
        with pytest.raises(GeminiError), patch_agent_raise_exception():
            await self.agent.run_prompt("")
