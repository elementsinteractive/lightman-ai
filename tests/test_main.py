from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock, call, patch

import pytest
from lightman_ai.article.models import (
    Article,
    ArticlesList,
    PrimarySelectedArticle,
    SelectedArticle,
    SelectedArticlesList,
)
from lightman_ai.core.sentry import configure_sentry
from lightman_ai.exceptions import NoSourcesError
from lightman_ai.main import _create_service_desk_issues, _get_articles_from_source, lightman
from lightman_ai.sources.exceptions import SourceError
from lightman_ai.sources.utils import SOURCE_CHOICES
from tests.conftest import patch_httpx_client_get, patch_multiple_responses
from tests.utils import patch_agent, patch_get_articles_from_xml


class TestLightman:
    async def test_lightman_retrieve_from_date_onwards(
        self,
    ) -> None:
        now = datetime.now(UTC)
        new_article = Article(title="article 2", link="https://article2.com", description="d", published_at=now)
        old_article = Article(
            title="article 1",
            link="https://article1.com",
            description="d",
            published_at=datetime.now(UTC) - timedelta(days=1),
        )

        feed_articles = [new_article, old_article]

        with (
            patch_httpx_client_get(),
            patch_get_articles_from_xml(feed_articles),
        ):
            result = await _get_articles_from_source(SOURCE_CHOICES[0], start_date=now)

        assert isinstance(result, ArticlesList)
        assert len(result) == 1
        assert new_article in result.articles
        assert old_article not in result.articles

    async def test_lightman_no_date_specified(self) -> None:
        now = datetime.now(UTC)
        new_article = Article(title="article 2", link="https://article2.com", description="d", published_at=now)
        old_article = Article(
            title="article 1",
            link="https://article1.com",
            description="d",
            published_at=datetime.now(UTC) - timedelta(days=1),
        )

        feed_articles = [new_article, old_article]
        with (
            patch_httpx_client_get(),
            patch_get_articles_from_xml(feed_articles),
        ):
            result = await _get_articles_from_source(SOURCE_CHOICES[0])

        assert isinstance(result, ArticlesList)
        assert result.articles == feed_articles

    async def test_lightman_and_service_desk_publish(self, test_prompt: str, thn_xml: str, bc_xml: str) -> None:
        now = datetime.now(UTC)
        related_article = SelectedArticle(
            title="article 2 from another source", link="https://article2-source2.com", published_at=now
        )
        relevant_article_1 = PrimarySelectedArticle(
            title="article 2",
            link="https://article2.com",
            why_is_relevant="a",
            relevance_score=8,
            published_at=now,
            related_articles=[related_article],
        )
        relevant_article_2 = PrimarySelectedArticle(
            title="article 3", link="https://article3.com", why_is_relevant="b", relevance_score=9, published_at=now
        )
        not_relevant_article = PrimarySelectedArticle(
            title="article 1", link="https://article1.com", why_is_relevant="a", relevance_score=5, published_at=now
        )
        agent_response = SelectedArticlesList(articles=[relevant_article_1, relevant_article_2, not_relevant_article])
        with (
            patch_multiple_responses([thn_xml, bc_xml]) as m_get_source_data,
            patch_agent(agent_response),
            patch("lightman_ai.main.ServiceDeskIntegration.from_env") as mock_service_desk_env,
        ):
            mock_service_desk = mock_service_desk_env.return_value
            mock_service_desk.create_request_of_type = AsyncMock(return_value="PROJ-123")
            result = await lightman(
                "openai",
                test_prompt,
                sources=SOURCE_CHOICES,
                score_threshold=8,
                service_desk_project_key="4",
                service_desk_request_id_type="2",
            )

        assert m_get_source_data.call_count == len(SOURCE_CHOICES)
        assert m_get_source_data.call_args_list == [
            call("https://feeds.feedburner.com/TheHackersNews"),
            call("https://news.google.com/rss/search?q=site:bleepingcomputer.com&hl=en-US&gl=US&ceid=US:en"),
        ]
        assert isinstance(result, list)
        assert len(result) == 2
        assert relevant_article_1 in result
        assert relevant_article_2 in result
        assert not_relevant_article not in result

        assert mock_service_desk_env.call_count == 1
        assert mock_service_desk.create_request_of_type.call_count == 2
        called_titles = [call.kwargs["summary"] for call in mock_service_desk.create_request_of_type.call_args_list]
        assert relevant_article_1.title in called_titles
        assert relevant_article_2.title in called_titles

    async def test_lightman_no_publish_if_dry_run(self, test_prompt: str, thn_xml: str, bc_xml: str) -> None:
        now = datetime.now(UTC)
        relevant_article_1 = PrimarySelectedArticle(
            title="article 2", link="https://article2.com", why_is_relevant="a", relevance_score=8, published_at=now
        )
        relevant_article_2 = PrimarySelectedArticle(
            title="article 3", link="https://article3.com", why_is_relevant="b", relevance_score=9, published_at=now
        )
        not_relevant_article = PrimarySelectedArticle(
            title="article 1", link="https://article1.com", why_is_relevant="a", relevance_score=5, published_at=now
        )
        agent_response = SelectedArticlesList(articles=[relevant_article_1, relevant_article_2, not_relevant_article])
        with (
            patch_multiple_responses([thn_xml, bc_xml]),
            patch_agent(agent_response),
            patch("lightman_ai.main.ServiceDeskIntegration.from_env") as mock_service_desk_env,
        ):
            mock_service_desk = mock_service_desk_env.return_value
            mock_service_desk.create_request_of_type = AsyncMock(return_value="PROJ-123")
            await lightman("openai", test_prompt, sources=SOURCE_CHOICES, score_threshold=8, dry_run=True)

        mock_service_desk_env.assert_not_called()
        assert mock_service_desk.create_request_of_type.call_count == 0

    async def test_lightman_raises_error_when_no_sources_provided(self) -> None:
        """Test that lightman raises NoSourcesError when no sources are provided."""
        with pytest.raises(NoSourcesError):
            await lightman(
                agent="openai",
                prompt="test prompt",
                score_threshold=5,
                sources=[],  # Empty sources list
                dry_run=True,
            )

    async def test_lightman_raises_error_when_sources_is_none(self) -> None:
        """Test that lightman raises NoSourcesError when sources is None."""
        with pytest.raises(NoSourcesError):
            await lightman(
                agent="openai",
                prompt="test prompt",
                score_threshold=5,
                sources=None,  # None sources
                dry_run=True,
            )

    async def test_lightman_fails_when_one_source_raises_exception(self, test_prompt: str, thn_xml: str) -> None:
        """Test that execution fails when one source raises an exception during download."""
        with (
            patch("httpx.AsyncClient.get") as mock_get,
            patch("pydantic_ai.Agent.run", new_callable=AsyncMock) as mock_agent_run,
        ):
            mock_get.side_effect = [
                Mock(text=thn_xml, **{"raise_for_status.return_value": None}),
                Exception("Network error: Connection timeout"),
            ]

            with pytest.raises(SourceError):
                await lightman(
                    agent="openai",
                    prompt=test_prompt,
                    sources=SOURCE_CHOICES,
                    score_threshold=8,
                    dry_run=True,
                )

        assert mock_get.call_count == len(SOURCE_CHOICES)
        mock_agent_run.assert_not_called()


class TestCreateServiceDeskIssues:
    """Tests for the _create_service_desk_issues function."""

    async def test_create_service_desk_issues_success(
        self,
        selected_articles: list[PrimarySelectedArticle],
        mock_service_desk: Mock,
    ) -> None:
        """Test successful creation of service desk issues for all articles."""
        await _create_service_desk_issues(
            selected_articles=selected_articles,
            service_desk_client=mock_service_desk,
            service_desk_project_key="TEST",
            service_desk_request_id_type="10001",
        )

        assert mock_service_desk.create_request_of_type.call_count == 2

        calls = mock_service_desk.create_request_of_type.call_args_list

        first_call = calls[0]
        assert first_call.kwargs["project_key"] == "TEST"
        assert first_call.kwargs["summary"] == "Critical Security Vulnerability in Popular Library"
        assert first_call.kwargs["request_id_type"] == "10001"
        expected_desc_1 = "*Why is relevant:*\nThis affects our production systems\n\n*Source:* https://example.com/article1\n\n*Related Articles:*\nThis is the same new: http://a.com\n\n*Score:* 9/10"
        assert first_call.kwargs["description"] == expected_desc_1

        second_call = calls[1]
        assert second_call.kwargs["project_key"] == "TEST"
        assert second_call.kwargs["summary"] == "New Attack Vector Discovered"
        assert second_call.kwargs["request_id_type"] == "10001"
        expected_desc_2 = "*Why is relevant:*\nCould impact our infrastructure\n\n*Source:* https://example.com/article2\n\n*Score:* 8/10"
        assert second_call.kwargs["description"] == expected_desc_2

    async def test_create_service_desk_issues_single_failure(
        self,
        selected_articles: list[PrimarySelectedArticle],
        mock_service_desk: Mock,
    ) -> None:
        """Test handling when one article fails to create service desk issue."""
        mock_service_desk.create_request_of_type.side_effect = [
            "PROJ-123",
            Exception("Service desk unavailable"),
        ]

        with pytest.raises(ExceptionGroup) as exc_info:
            await _create_service_desk_issues(
                selected_articles=selected_articles,
                service_desk_client=mock_service_desk,
                service_desk_project_key="TEST",
                service_desk_request_id_type="10001",
            )

        assert mock_service_desk.create_request_of_type.call_count == 2

        assert "Could not create all ServiceDesk issues" in str(exc_info.value)
        assert len(exc_info.value.exceptions) == 1
        assert "Service desk unavailable" in str(exc_info.value.exceptions[0])

    async def test_create_service_desk_issues_all_failures(
        self,
        selected_articles: list[PrimarySelectedArticle],
        mock_service_desk: Mock,
    ) -> None:
        """Test handling when all articles fail to create service desk issues."""
        mock_service_desk.create_request_of_type.side_effect = Exception("Service desk down")

        with pytest.raises(ExceptionGroup) as exc_info:
            await _create_service_desk_issues(
                selected_articles=selected_articles,
                service_desk_client=mock_service_desk,
                service_desk_project_key="TEST",
                service_desk_request_id_type="10001",
            )

        assert mock_service_desk.create_request_of_type.call_count == 2

        assert "Could not create all ServiceDesk issues" in str(exc_info.value)
        assert len(exc_info.value.exceptions) == 2


class TestSentryIntegration:
    """Tests for Sentry integration behavior."""

    @patch.dict("os.environ", {})
    @patch.dict("os.environ", {}, clear=True)
    @patch("sentry_sdk.init")
    def test_sentry_skipped_when_dsn_not_set(self, mock_sentry_init: Mock) -> None:
        """Test that Sentry initialization is skipped when SENTRY_DSN is not set."""
        configure_sentry(10)
        assert mock_sentry_init.call_count == 0

    @patch.dict("os.environ", {"SENTRY_DSN": "https://test@sentry.io/123"})
    @patch("sentry_sdk.init")
    def test_sentry_execution_does_not_error_when_it_cannot_instantiate(self, mock_sentry_init: Mock) -> None:
        """Test that execution continues when Sentry initialization fails."""
        mock_sentry_init.side_effect = Exception("Sentry connection failed")

        configure_sentry(10)

        mock_sentry_init.assert_called_once()

    @patch.dict("os.environ", {"SENTRY_DSN": "https://test@sentry.io/123"})
    @patch("sentry_sdk.init")
    @patch("lightman_ai.core.sentry.metadata.version")
    def test_sentry_initializes_successfully(self, mock_version: Mock, mock_sentry_init: Mock) -> None:
        """Test that Sentry initializes successfully when configured properly."""
        mock_version.return_value = "1.0.0"

        configure_sentry(10)

        mock_sentry_init.assert_called_once()
        call_kwargs = mock_sentry_init.call_args.kwargs
        assert "release" in call_kwargs
        assert "integrations" in call_kwargs

        mock_version.assert_called_once_with("lightman-ai")
