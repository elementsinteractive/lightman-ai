import pytest
from freezegun import freeze_time
from hackerman_ai.main import hackerman


class TestHackerman:
    @pytest.mark.vcr()
    @freeze_time("2025-01-01")
    async def test_get_news(self, api_key: str) -> None:
        assert await hackerman(api_key) == 0
