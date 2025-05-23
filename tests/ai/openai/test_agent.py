import pytest
from hackerman_ai.ai.openai.agent import OpenAIAgent
from hackerman_ai.article.models import SelectedArticlesList


class TestAgent:
    OPENAI_MODEL = "gpt-4.1"

    @pytest.mark.vcr
    def test_run_prompt(self, short_prompt: str) -> None:
        agent = OpenAIAgent(self.OPENAI_MODEL)
        result = agent._run_prompt(short_prompt)
        assert isinstance(result, SelectedArticlesList)
