import logging
from typing import Any

import pytest
from hackerman_ai.article.models import ArticlesList
from hackerman_ai.main import hackerman


class TestHackerman:
    @pytest.mark.vcr
    async def test_hackerman(self, caplog: Any) -> None:
        with caplog.at_level(logging.WARNING):
            result = await hackerman("gpt-4.1")

        assert isinstance(result, ArticlesList)
        assert "Found these articles: " in caplog.text
