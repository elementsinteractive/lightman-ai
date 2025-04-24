import pytest
from hackerman_ai.sources.the_hacker_news import TheHackerNewsSource


class TestTheHackerNewsSource:
    @pytest.mark.vcr()
    async def test_get_feed(self) -> None:
        news = await TheHackerNewsSource().get_feed()
        assert news.startswith('<?xml version="1.0" ')

    def test_clean(self) -> None:
        string_to_clean = "\\na       "
        result = TheHackerNewsSource()._clean(string_to_clean)
        assert result == "a"

    @pytest.mark.vcr()
    async def test_get_news(self) -> None:
        news = await TheHackerNewsSource().get_news()
        assert news.startswith('[{"title":')
