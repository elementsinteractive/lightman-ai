import pytest
from hackerman_ai.main import hackerman


class TestHackerman:
    @pytest.mark.vcr()
    async def test_get_news(self) -> None:
        assert await hackerman("") == 0
