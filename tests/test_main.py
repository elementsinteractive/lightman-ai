import logging
from typing import Any

import pytest
from hackerman_ai.main import hackerman


class TestHackerman:
    @pytest.mark.vcr
    async def test_hackerman(self, caplog: Any) -> None:
        with caplog.at_level(logging.WARNING):
            result = await hackerman()

        assert result == 0
        assert "Found these articles: " in caplog.text
