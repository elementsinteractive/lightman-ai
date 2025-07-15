from unittest.mock import patch

from lightman_ai.article.models import ArticlesList
from lightman_ai.sources.the_hacker_news import TheHackerNewsSource


class TestTheHackerNewsSource:
    def test_clean(self) -> None:
        string_to_clean = "\\na       "
        result = TheHackerNewsSource()._clean(string_to_clean)
        assert result == "a"

    async def test_get_articles(self, thn_xml: str) -> None:
        with patch("httpx.get") as mock:
            mock.return_value = thn_xml
            articles = TheHackerNewsSource().get_articles()

        assert isinstance(articles, ArticlesList)
        assert len(articles.articles) == 50
