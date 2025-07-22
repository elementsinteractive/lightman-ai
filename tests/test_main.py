import logging
from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pytest
from lightman_ai.article.models import SelectedArticle, SelectedArticlesList
from lightman_ai.main import _create_service_desk_issues, lightman
from tests.utils import patch_agent


class TestHackerman:
    def test_lightman_and_service_desk_publish(self, caplog: Any, test_prompt: str, thn_xml: str) -> None:
        relevant_article_1 = SelectedArticle(
            title="article 2", link="https://article2.com", why_is_relevant="a", relevance_score=8
        )
        relevant_article_2 = SelectedArticle(
            title="article 3", link="https://article3.com", why_is_relevant="b", relevance_score=9
        )
        not_relevant_article = SelectedArticle(
            title="article 1", link="https://article1.com", why_is_relevant="a", relevance_score=5
        )
        agent_response = SelectedArticlesList(articles=[relevant_article_1, relevant_article_2, not_relevant_article])
        with (
            caplog.at_level(logging.INFO),
            patch("httpx.get") as m_thn,
            patch_agent(agent_response),
            patch("lightman_ai.main.ServiceDeskIntegration.from_env") as mock_service_desk_env,
        ):
            m_thn.return_value = thn_xml
            mock_service_desk = mock_service_desk_env.return_value
            mock_service_desk.create_request_of_type = AsyncMock(return_value="PROJ-123")
            result = lightman("openai", test_prompt, score_threshold=8, project_key="4", request_id_type="2")

        # Check lightman result
        assert isinstance(result, list)
        assert len(result) == 2
        assert relevant_article_1 in result
        assert relevant_article_2 in result
        assert not_relevant_article not in result
        assert "Found these articles: " in caplog.text

        # Check ServiceDesk integration
        mock_service_desk_env.assert_called_once()
        assert mock_service_desk.create_request_of_type.call_count == 2
        called_titles = [call.kwargs["summary"] for call in mock_service_desk.create_request_of_type.call_args_list]
        assert relevant_article_1.title in called_titles
        assert relevant_article_2.title in called_titles

    def test_lightman_no_publish_if_dry_run(self, caplog: Any, test_prompt: str, thn_xml: str) -> None:
        relevant_article_1 = SelectedArticle(
            title="article 2", link="https://article2.com", why_is_relevant="a", relevance_score=8
        )
        relevant_article_2 = SelectedArticle(
            title="article 3", link="https://article3.com", why_is_relevant="b", relevance_score=9
        )
        not_relevant_article = SelectedArticle(
            title="article 1", link="https://article1.com", why_is_relevant="a", relevance_score=5
        )
        agent_response = SelectedArticlesList(articles=[relevant_article_1, relevant_article_2, not_relevant_article])
        with (
            caplog.at_level(logging.INFO),
            patch("httpx.get") as m_thn,
            patch_agent(agent_response),
            patch("lightman_ai.main.ServiceDeskIntegration.from_env") as mock_service_desk_env,
        ):
            m_thn.return_value = thn_xml
            mock_service_desk = mock_service_desk_env.return_value
            mock_service_desk.create_request_of_type = AsyncMock(return_value="PROJ-123")
            lightman("openai", test_prompt, score_threshold=8, dry_run=True)

        # Check ServiceDesk integration is NOT called in dry_run mode
        mock_service_desk_env.assert_not_called()
        assert mock_service_desk.create_request_of_type.call_count == 0


class TestCreateServiceDeskIssues:
    """Tests for the _create_service_desk_issues function."""

    def test_create_service_desk_issues_success(
        self, selected_articles: list[SelectedArticle], mock_service_desk: Mock, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test successful creation of service desk issues for all articles."""
        with caplog.at_level(logging.INFO):
            _create_service_desk_issues(
                selected_articles=selected_articles,
                service_desk_client=mock_service_desk,
                project_key="TEST",
                request_id_type="10001",
            )

        # Verify service desk client was called for each article
        assert mock_service_desk.create_request_of_type.call_count == 2

        # Check the calls were made with correct parameters
        calls = mock_service_desk.create_request_of_type.call_args_list

        # First article call
        first_call = calls[0]
        assert first_call.kwargs["project_key"] == "TEST"
        assert first_call.kwargs["summary"] == "Critical Security Vulnerability in Popular Library"
        assert first_call.kwargs["request_id_type"] == "10001"
        expected_desc_1 = "*Why is relevant:*\nThis affects our production systems\n\n*Source:* https://example.com/article1\n\n*Score:* 9/10"
        assert first_call.kwargs["description"] == expected_desc_1

        # Second article call
        second_call = calls[1]
        assert second_call.kwargs["project_key"] == "TEST"
        assert second_call.kwargs["summary"] == "New Attack Vector Discovered"
        assert second_call.kwargs["request_id_type"] == "10001"
        expected_desc_2 = "*Why is relevant:*\nCould impact our infrastructure\n\n*Source:* https://example.com/article2\n\n*Score:* 8/10"
        assert second_call.kwargs["description"] == expected_desc_2

        # Check success log messages
        assert "Created issue for article https://example.com/article1" in caplog.text
        assert "Created issue for article https://example.com/article2" in caplog.text

    def test_create_service_desk_issues_single_failure(
        self, selected_articles: list[SelectedArticle], mock_service_desk: Mock, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test handling when one article fails to create service desk issue."""
        # Make the first call succeed, second call fail
        mock_service_desk.create_request_of_type.side_effect = [
            "PROJ-123",  # Success for first article
            Exception("Service desk unavailable"),  # Failure for second article
        ]

        with caplog.at_level(logging.INFO), pytest.raises(ExceptionGroup) as exc_info:
            _create_service_desk_issues(
                selected_articles=selected_articles,
                service_desk_client=mock_service_desk,
                project_key="TEST",
                request_id_type="10001",
            )

        # Verify both calls were attempted
        assert mock_service_desk.create_request_of_type.call_count == 2

        # Check that ExceptionGroup contains the failure
        assert "Could not create all ServiceDesk issues" in str(exc_info.value)
        assert len(exc_info.value.exceptions) == 1
        assert "Service desk unavailable" in str(exc_info.value.exceptions[0])

        # Check that success was logged for the first article
        assert "Created issue for article https://example.com/article1" in caplog.text

    def test_create_service_desk_issues_all_failures(
        self, selected_articles: list[SelectedArticle], mock_service_desk: Mock, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test handling when all articles fail to create service desk issues."""
        # Make all calls fail
        mock_service_desk.create_request_of_type.side_effect = Exception("Service desk down")

        with caplog.at_level(logging.ERROR), pytest.raises(ExceptionGroup) as exc_info:
            _create_service_desk_issues(
                selected_articles=selected_articles,
                service_desk_client=mock_service_desk,
                project_key="TEST",
                request_id_type="10001",
            )

        # Verify both calls were attempted
        assert mock_service_desk.create_request_of_type.call_count == 2

        # Check that ExceptionGroup contains all failures
        assert "Could not create all ServiceDesk issues" in str(exc_info.value)
        assert len(exc_info.value.exceptions) == 2

        # Check error logging
        assert (
            "Could not create ServiceDesk issue: Critical Security Vulnerability in Popular Library, https://example.com/article1"
            in caplog.text
        )
        assert (
            "Could not create ServiceDesk issue: New Attack Vector Discovered, https://example.com/article2"
            in caplog.text
        )
