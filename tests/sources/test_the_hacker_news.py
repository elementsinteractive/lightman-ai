import pytest
from hackerman_ai.sources.the_hacker_news import TheHackerNewsSource


class TestTheHackerNewsSource:
    @pytest.mark.vcr()
    async def test_get_news_xml(self) -> None:
        news = await TheHackerNewsSource.get_news()
        assert news.startswith('<?xml version="1.0" ')
