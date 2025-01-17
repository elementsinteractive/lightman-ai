import pytest
from hackerman_ai.sources.news import get_thn_news


class TestTheHackerNewsSource:
    @pytest.mark.vcr()
    async def test_get_news_xml(self) -> None:
        news = await get_thn_news()
        assert news.startswith('<?xml version="1.0" ')
