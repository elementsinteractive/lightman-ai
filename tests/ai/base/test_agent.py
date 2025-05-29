from typing import override

from hackerman_ai.ai.base.agent import BaseAgent
from hackerman_ai.article.models import SelectedArticle, SelectedArticlesList


class FakeAgent(BaseAgent):
    @override
    def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        return SelectedArticlesList(articles=[])


class TestBaseAgent:
    def test__run_prompt_multiple_times(self, test_prompt: str) -> None:
        """Test that we run the prompt as many times as we specify, and we receive back a LIST of `SelectedArticlesList`."""
        agent = FakeAgent()

        result = agent._run_prompt_multiple_times(test_prompt, iterations=3)
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(x, SelectedArticlesList) for x in result)

    def test__get_prompt_result(self, test_prompt: str) -> None:
        """Test that we run the prompt as many times as we specify, and we receive back an INSTANCE of `SelectedArticlesList`."""
        agent = FakeAgent()
        result = agent.get_prompt_result(test_prompt, iterations=3)
        assert isinstance(result, SelectedArticlesList)

    def test__merge_results(self) -> None:
        """Test that all the articles lists get merged into one."""
        article1 = SelectedArticle(link="link1", title="Elephant gives birth to a monkey")
        article1_repeated = SelectedArticle(link="link1", title="Elephant gives birth to a monkey")
        different_article = SelectedArticle(link="link2", title="Elephant gives birth to a monkey")
        articles_list1 = SelectedArticlesList(articles=[article1, different_article])
        articles_list2 = SelectedArticlesList(articles=[article1_repeated])

        agent = FakeAgent()
        result = agent._merge_results([articles_list1, articles_list2])
        assert isinstance(result, SelectedArticlesList)
        assert set(result.articles) == {article1, different_article}
