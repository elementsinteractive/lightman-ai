import pytest
from lightman_ai.article.models import Article, SelectedArticle, SelectedArticlesList


class TestBaseArticle:
    def test_compare_article_objects(self) -> None:
        new1 = Article(title="", description="", link="A")
        same_new = Article(title="", description="", link="A")
        different_new = Article(title="", description="", link="B")

        assert new1 == same_new
        assert new1 != different_new


class TestSelectedArticlesList:
    def test__get_results_above_score(self) -> None:
        article_match = SelectedArticle(link="link1", relevance_score=5, title="", why_is_relevant="")
        article_no_match = SelectedArticle(link="link2", relevance_score=1, title="", why_is_relevant="")

        result = SelectedArticlesList(articles=[article_match, article_no_match]).get_articles_with_score_gte_threshold(
            5
        )

        assert result == [article_match]

    def test_score_threshold_must_be_positive(self) -> None:
        with pytest.raises(ValueError, match="score threshold must be > 0."):
            SelectedArticlesList(articles=[]).get_articles_with_score_gte_threshold(0)
