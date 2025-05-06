import pytest
from hackerman_ai.article.models import ArticlesList
from hackerman_ai.sources.the_hacker_news import TheHackerNewsSource


class TestTheHackerNewsSource:
    def test_clean(self) -> None:
        string_to_clean = "\\na       "
        result = TheHackerNewsSource()._clean(string_to_clean)
        assert result == "a"

    @pytest.mark.vcr()
    async def test_get_articles(self) -> None:
        articles = await TheHackerNewsSource().get_articles()

        assert isinstance(articles, ArticlesList)
        assert len(articles.articles) == 50
