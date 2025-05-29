import logging
from typing import Any

import pytest
from hackerman_ai.article.models import SelectedArticlesList
from hackerman_ai.main import hackerman


class TestHackerman:
    @pytest.mark.vcr
    def test_hackerman(self, caplog: Any, test_prompt: str) -> None:
        with caplog.at_level(logging.WARNING):
            result = hackerman("gpt-4.1", test_prompt)

        assert isinstance(result, SelectedArticlesList)
        assert "Found these articles: " in caplog.text
