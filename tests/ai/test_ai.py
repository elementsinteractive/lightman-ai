import pytest
from hackerman_ai.ai.agent import AIAgent
from hackerman_ai.ai.utils import get_prompt


class TestAgent:
    @pytest.mark.vcr()
    async def test_run_prompt(self, thn_news: str) -> None:
        agent = AIAgent()
        result = await agent.run_prompt(get_prompt(thn_news))
        assert len(result.news) == 2
