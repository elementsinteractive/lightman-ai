import logging
from typing import Any
from unittest.mock import patch

from hackerman_ai.article.models import SelectedArticle, SelectedArticlesList
from hackerman_ai.main import hackerman
from tests.utils import patch_agent


class TestHackerman:
    def test_hackerman(self, caplog: Any, test_prompt: str, thn_xml: str) -> None:
        relevant_article = SelectedArticle(
            title="article 2", link="https://article2.com", why_is_relevant="a", relevance_score=8
        )
        not_relevant_article = SelectedArticle(
            title="article 1", link="https://article1.com", why_is_relevant="a", relevance_score=5
        )
        agent_response = SelectedArticlesList(articles=[relevant_article, not_relevant_article])
        with caplog.at_level(logging.WARNING), patch("httpx.get") as m_thn, patch_agent(agent_response):
            m_thn.return_value = thn_xml
            result = hackerman("gpt-4.1", test_prompt, score_threshold=8, iterations=1)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] == relevant_article
        assert "Found these articles: " in caplog.text
