import pytest
from hackerman_ai.ai.openai.agent import OpenAIAgent
from hackerman_ai.article.models import SelectedArticle, SelectedArticlesList
from tests.conftest import patch_run_prompt


class TestAgent:
    @pytest.mark.vcr
    async def test_run_prompt(self, short_prompt: str) -> None:
        agent = OpenAIAgent()
        result = await agent._run_prompt(short_prompt)
        assert isinstance(result, SelectedArticlesList)

    async def test_run_prompt_multiple_times(self, short_prompt: str) -> None:
        """Test that we run the prompt as many times as we specify, and we receive back a LIST of `SelectedArticlesList`."""
        agent = OpenAIAgent()
        async with patch_run_prompt() as mock:
            result = await agent._run_prompt_multiple_times(short_prompt, iterations=3)
        assert mock.call_count == 3
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(x, SelectedArticlesList) for x in result)

    async def test_get_prompt_result(self, short_prompt: str) -> None:
        """Test that we run the prompt as many times as we specify, and we receive back an INSTANCE of `SelectedArticlesList`."""
        agent = OpenAIAgent()
        async with patch_run_prompt() as mock:
            result = await agent.get_prompt_result(short_prompt, iterations=3)
        assert mock.call_count == 3
        assert isinstance(result, SelectedArticlesList)

    def test__merge_results(self) -> None:
        article1 = SelectedArticle(link="link1")
        article1_repeated = SelectedArticle(link="link1")
        different_article = SelectedArticle(link="link2")
        articles_list1 = SelectedArticlesList(articles=[article1, different_article])
        articles_list2 = SelectedArticlesList(articles=[article1_repeated])

        agent = OpenAIAgent()
        result = agent._merge_results([articles_list1, articles_list2])
        assert isinstance(result, SelectedArticlesList)
        assert set(result.articles) == {article1, different_article}
