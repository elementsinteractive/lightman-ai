import logging
from typing import Any
from unittest.mock import AsyncMock, patch

from lightman_ai.article.models import SelectedArticle, SelectedArticlesList
from lightman_ai.main import lightman
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
