import logging
from typing import Any

import pytest
from hackerman_ai.article.models import SelectedArticle
from hackerman_ai.main import hackerman


class TestHackerman:
    @pytest.mark.vcr
    def test_hackerman(self, caplog: Any, test_prompt: str) -> None:
        with caplog.at_level(logging.WARNING):
            result = hackerman("gpt-4.1", test_prompt, 1, 1)

        assert isinstance(result, list)
        assert all(isinstance(article, SelectedArticle) for article in result)
        assert "Found these articles: " in caplog.text
