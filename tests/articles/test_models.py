from datetime import UTC, datetime, timedelta

import pytest
from lightman_ai.article.exceptions import DifferentArticleClassesError, NoTimeZoneError
from lightman_ai.article.models import (
    Article,
    ArticlesList,
    PrimarySelectedArticle,
    SelectedArticlesList,
)
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
        article_match = PrimarySelectedArticle(
            link="link1", relevance_score=5, title="Test", why_is_relevant="Reason", published_at=now
        )
        article_no_match = PrimarySelectedArticle(
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
        article_match = PrimarySelectedArticle(
            link="link1", relevance_score=5, title="Test", why_is_relevant="Reason", published_at=datetime.now(UTC)
        )
        article_no_match = PrimarySelectedArticle(
            link="link2",
            relevance_score=4,
            title="Test",
            why_is_relevant="Reason",
            published_at=datetime.now(UTC) - timedelta(days=1),
        )

        result = SelectedArticlesList.get_articles_from_date_onwards([article_match, article_no_match], start_date)

        assert result.articles == [article_match]


class TestBaseArticlesList:
    def test_iadd_operator_combines_articles_lists(self) -> None:
        """Test that += operator combines two BaseArticlesList objects."""
        now = datetime.now(UTC)

        # Create articles for first list
        article1 = Article(
            title="Article 1", description="Description 1", link="https://example.com/1", published_at=now
        )

        # Create articles for second list
        article2 = Article(
            title="Article 3", description="Description 3", link="https://example.com/3", published_at=now
        )

        # Create two separate ArticlesList objects
        list1 = ArticlesList(articles=[article1])
        list2 = ArticlesList(articles=[article2])

        # Use += operator to combine lists
        list1 += list2

        # Verify the combination worked
        assert list1.articles == [article1, article2]

        # Verify list2 is unchanged
        assert list2.articles == [article2]

    def test_iadd_operator_with_selected_articles_list(self) -> None:
        """Test that += operator works with SelectedArticlesList objects."""
        now = datetime.now(UTC)

        # Create SelectedArticle objects
        selected1 = PrimarySelectedArticle(
            title="Selected 1",
            link="https://example.com/selected1",
            published_at=now,
            why_is_relevant="Reason 1",
            relevance_score=8,
        )
        selected2 = PrimarySelectedArticle(
            title="Selected 2",
            link="https://example.com/selected2",
            published_at=now,
            why_is_relevant="Reason 2",
            relevance_score=9,
        )

        # Create two SelectedArticlesList objects
        list1 = SelectedArticlesList(articles=[selected1])
        list2 = SelectedArticlesList(articles=[selected2])

        # Use += operator
        list1 += list2

        # Verify the combination
        assert len(list1) == 2
        assert list1.articles == [selected1, selected2]

    def test_iadd_operator_cannot_merge_different_classes(self) -> None:
        """Test that += operator fails if attempting to merge different BaseArticleList subclasses."""
        now = datetime.now(UTC)

        # Create SelectedArticle objects
        selected_article = PrimarySelectedArticle(
            title="Selected 1",
            link="https://example.com/selected1",
            published_at=now,
            why_is_relevant="Reason 1",
            relevance_score=8,
        )

        selected_article_list = SelectedArticlesList(articles=[selected_article])

        article = Article(
            title="Article 3", description="Description 3", link="https://example.com/3", published_at=now
        )

        article_list = ArticlesList(articles=[article])
        with pytest.raises(DifferentArticleClassesError):
            selected_article_list += article_list  # type: ignore[arg-type]

    def test_iadd_operator_raises_error_for_incompatible_type(self) -> None:
        """Test that += operator raises TypeError for incompatible types."""
        now = datetime.now(UTC)
        article = Article(
            title="Article", description="Description", link="https://example.com/article", published_at=now
        )

        articles_list = ArticlesList(articles=[article])

        # Try to add incompatible types
        with pytest.raises(DifferentArticleClassesError):
            articles_list += "invalid_type"  # type: ignore[arg-type]

        with pytest.raises(DifferentArticleClassesError):
            articles_list += [article]  # type: ignore[arg-type]

        with pytest.raises(DifferentArticleClassesError):
            articles_list += 123  # type: ignore[arg-type]
