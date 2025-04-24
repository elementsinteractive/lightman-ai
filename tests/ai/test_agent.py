import pytest
from hackerman_ai.ai.models import New, News
from hackerman_ai.ai.openai_agent import OpenAIAgent
from hackerman_ai.ai.utils import get_prompt
from hackerman_ai.core.settings import settings


class TestAgent:
    @pytest.mark.vcr()
    async def test_run_prompt(self, thn_news: str) -> None:
        agent = OpenAIAgent()
        result = await agent._run_prompt(get_prompt(thn_news))
        assert isinstance(result, News)

    @pytest.mark.vcr()
    async def test_run_prompt_multiple_times(self, thn_news: str) -> None:
        agent = OpenAIAgent()
        result = await agent._run_prompt_multiple_times(
            get_prompt(thn_news), iterations=3, rate_limit_timeout=settings.OPENAI_RATE_LIMIT_TIMEOUT
        )
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(x, News) for x in result)

    @pytest.mark.vcr()
    async def test_get_prompt_result(self, thn_news: str) -> None:
        agent = OpenAIAgent()
        result = await agent.get_prompt_result(
            get_prompt(thn_news), iterations=3, rate_limit_timeout=settings.OPENAI_RATE_LIMIT_TIMEOUT
        )
        assert isinstance(result, News)

    def test__merge_results(self) -> None:
        new1 = New("", "", "link1")
        new1_repeated = New("", "", "link1")
        different_new = New("", "", "link2")
        news_list1 = News(news=[new1, different_new])
        news_list2 = News(news=[new1_repeated])

        agent = OpenAIAgent()
        result = agent._merge_results([news_list1, news_list2])
        assert isinstance(result, News)
        assert set(result.news) == {new1, different_new}
