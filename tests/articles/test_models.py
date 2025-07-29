from datetime import UTC, datetime, timedelta

import pytest
from lightman_ai.article.exceptions import NoTimeZoneError
from lightman_ai.article.models import Article, SelectedArticle, SelectedArticlesList
from pydantic import ValidationError


class TestBaseArticle:
    def test_compare_article_objects(self) -> None:
        now = datetime.now(UTC)
        new1 = Article(title="Test", description="Desc", link="A", published_at=now)
        same_new = Article(title="Test", description="Desc", link="A", published_at=now)
        different_new = Article(title="Test", description="Desc", link="B", published_at=now)

        assert new1 == same_new
        assert new1 != different_new

    def test_published_at_is_required(self) -> None:
        with pytest.raises(ValidationError, match="published_at"):
            Article(title="Test", description="Desc", link="https://example.com")  # type: ignore[call-arg]

    def test_published_at_accepts_timezone_aware_datetime(self) -> None:
        utc_time = datetime.now(UTC)
        article = Article(title="Test", description="Desc", link="https://example.com", published_at=utc_time)
        assert article.published_at == utc_time

    def test_published_at_does_not_accept_naive_datetime(self) -> None:
        naive_time = datetime.now()
        with pytest.raises(NoTimeZoneError, match="timezone aware"):
            Article(title="Test", description="Desc", link="https://example.com", published_at=naive_time)

    def test_title_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError, match="at least 1 character"):
            Article(title="", description="Desc", link="https://example.com", published_at=datetime.now(UTC))

    def test_link_cannot_be_empty(self) -> None:
        with pytest.raises(ValidationError, match="at least 1 character"):
            Article(title="Test", description="Desc", link="", published_at=datetime.now(UTC))

    def test_description_cannot_be_empty_for_article(self) -> None:
        with pytest.raises(ValidationError, match="at least 1 character"):
            Article(title="Test", description="", link="https://example.com", published_at=datetime.now(UTC))


class TestSelectedArticlesList:
    def test__get_results_above_score(self) -> None:
        now = datetime.now(UTC)
        article_match = SelectedArticle(
            link="link1", relevance_score=5, title="Test", why_is_relevant="Reason", published_at=now
        )
        article_no_match = SelectedArticle(
            link="link2", relevance_score=4, title="Test", why_is_relevant="Reason", published_at=now
        )

        result = SelectedArticlesList(articles=[article_match, article_no_match]).get_articles_with_score_gte_threshold(
            5
        )

        assert result == [article_match]

    def test_score_threshold_must_be_positive(self) -> None:
        with pytest.raises(ValueError, match="score threshold must be > 0."):
            SelectedArticlesList(articles=[]).get_articles_with_score_gte_threshold(0)

    def test_get_articles_from_date_onwards(self) -> None:
        start_date = datetime.now(UTC)
        article_match = SelectedArticle(
            link="link1", relevance_score=5, title="Test", why_is_relevant="Reason", published_at=datetime.now(UTC)
        )
        article_no_match = SelectedArticle(
            link="link2",
            relevance_score=4,
            title="Test",
            why_is_relevant="Reason",
            published_at=datetime.now(UTC) - timedelta(days=1),
        )

        result = SelectedArticlesList.get_articles_from_date_onwards([article_match, article_no_match], start_date)

        assert result.articles == [article_match]
