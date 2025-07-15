import pytest
from lightman_ai.article.models import Article, ArticlesList, SelectedArticle, SelectedArticlesList


class TestBaseArticle:
    def test_compare_article_objects(self) -> None:
        new1 = Article(title="", description="", link="A")
        same_new = Article(title="", description="", link="A")
        different_new = Article(title="", description="", link="B")

        assert new1 == same_new
        assert new1 != different_new


class TestArticle:
    def test_number_of_tokens(self) -> None:
        article = Article(title="Elephant gives birth to a monkey", description="lorem ipsum", link="https://aaaa.com")
        assert article.number_of_tokens == 28


class TestSelectedArticle:
    def test_number_of_tokens(self) -> None:
        article = SelectedArticle(
            link="https://aaaa.com", title="Elephant gives birth to a monkey", relevance_score=1, why_is_relevant=""
        )
        assert article.number_of_tokens == 35


class TestArticlesList:
    def test_total_number_of_tokens(self) -> None:
        article1 = Article(title="Elephant gives birth to a monkey", description="lorem ipsum", link="https://aaaa.com")
        article2 = Article(title="Elephant gives birth to a monkey", description="lorem ipsum", link="https://aaaa.com")

        articles_list = ArticlesList(articles=[article1, article2])
        assert articles_list.total_number_of_tokens == 56


class TestSelectedArticlesList:
    def test_total_number_of_tokens(self) -> None:
        article1 = SelectedArticle(
            link="https://aaaa.com", title="Elephant gives birth to a monkey", relevance_score=1, why_is_relevant=""
        )
        article2 = SelectedArticle(
            link="https://aaaa.com", title="Elephant gives birth to a monkey", relevance_score=1, why_is_relevant=""
        )

        articles_list = SelectedArticlesList(articles=[article1, article2])
        assert articles_list.total_number_of_tokens == 70

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
