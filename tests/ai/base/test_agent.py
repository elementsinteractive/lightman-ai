from typing import override

import pytest
from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.article.models import SelectedArticle, SelectedArticlesList


class FakeAgent(BaseAgent):
    @override
    def _run_prompt(self, prompt: str) -> SelectedArticlesList:
        return SelectedArticlesList(articles=[])

    @override
    def _run_prompt_multiple_times(self, prompt: str, iterations: int) -> list[SelectedArticlesList]:
        return []


class TestBaseAgent:
    def test__get_prompt_result(self, test_prompt: str) -> None:
        """Check that we receive an instance of `SelectedArticlesList` when running the method."""
        agent = FakeAgent()
        result = agent.get_prompt_result(test_prompt, iterations=3)
        assert isinstance(result, SelectedArticlesList)

    def test__merge_results(self) -> None:
        """
        Test that all the articles lists get merged into one.

        Proves that what differentiates SelecterArticles from one another is the `link` field.
        """
        article1 = SelectedArticle(link="link1", relevance_score=1, title="", why_is_relevant="")
        article1_repeated = SelectedArticle(link="link1", relevance_score=1, title="", why_is_relevant="")
        different_article = SelectedArticle(link="link2", relevance_score=1, title="", why_is_relevant="")

        articles_list1 = SelectedArticlesList(articles=[article1, different_article])
        articles_list2 = SelectedArticlesList(articles=[article1_repeated])

        agent = FakeAgent()
        result = agent._merge_results([articles_list1, articles_list2])
        assert isinstance(result, SelectedArticlesList)
        assert set(result.articles) == {article1, different_article}

    def test_iterations_must_be_positive(self) -> None:
        agent = FakeAgent()
        with pytest.raises(ValueError, match="`iterations` must be > 0."):
            agent.get_prompt_result(prompt="", iterations=0)
