from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from lightman_ai.article.models import ArticlesList
from lightman_ai.sources.exceptions import MalformedSourceResponseError, SourceError
from lightman_ai.sources.the_hacker_news import TheHackerNewsSource
from tests.conftest import patch_httpx_client_get


class TestTheHackerNewsSource:
    def test_clean(self) -> None:
        string_to_clean = "\\na       "
        result = TheHackerNewsSource()._clean(string_to_clean)
        assert result == "a"

    async def test_get_articles(self, thn_xml: str) -> None:
        with patch_httpx_client_get(thn_xml):
            articles = await TheHackerNewsSource().get_articles()

        assert isinstance(articles, ArticlesList)
        assert len(articles.articles) == 50

    def test_xml_to_list_of_articles_success(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>Test Article 1</title>
                    <description>Test description 1</description>
                    <link>https://example.com/1</link>
                    <pubDate>Mon, 01 Jan 2024 12:00:00 +0000</pubDate>
                </item>
                <item>
                    <title>Test Article 2</title>
                    <description>Test description 2</description>
                    <link>https://example.com/2</link>
                    <pubDate>Tue, 02 Jan 2024 12:00:00 +0000</pubDate>
                </item>
            </channel>
        </rss>"""

        articles = TheHackerNewsSource()._xml_to_list_of_articles(xml)

        assert len(articles) == 2
        assert articles[0].title == "Test Article 1"
        assert articles[0].description == "Test description 1"
        assert articles[0].link == "https://example.com/1"
        assert articles[0].published_at == datetime(2024, 1, 1, 12, 0, 0, tzinfo=UTC)

        assert articles[1].title == "Test Article 2"
        assert articles[1].description == "Test description 2"
        assert articles[1].link == "https://example.com/2"
        assert articles[1].published_at == datetime(2024, 1, 2, 12, 0, 0, tzinfo=UTC)

    def test_xml_to_list_of_articles_no_channel(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
        </rss>"""

        with pytest.raises(MalformedSourceResponseError, match="No channel element found in RSS feed"):
            TheHackerNewsSource()._xml_to_list_of_articles(xml)

    def test_xml_error(self) -> None:
        xml = ""

        with pytest.raises(MalformedSourceResponseError, match="Invalid XML format"):
            TheHackerNewsSource()._xml_to_list_of_articles(xml)

    def test_xml_to_list_of_articles_missing_pub_date(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>Test Article</title>
                    <description>Test description</description>
                    <link>https://example.com/1</link>
                </item>
            </channel>
        </rss>"""

        assert not TheHackerNewsSource()._xml_to_list_of_articles(xml)

    def test_xml_to_list_of_articles_empty_pub_date(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>Test Article</title>
                    <description>Test description</description>
                    <link>https://example.com/1</link>
                    <pubDate></pubDate>
                </item>
            </channel>
        </rss>"""

        assert not TheHackerNewsSource()._xml_to_list_of_articles(xml)

    def test_xml_to_list_of_articles_validation_error(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <description>Test description</description>
                    <link>https://example.com/1</link>
                    <pubDate>Mon, 01 Jan 2024 12:00:00 +0000</pubDate>
                </item>
            </channel>
        </rss>"""  # no title

        assert not TheHackerNewsSource()._xml_to_list_of_articles(xml)

    def test_xml_to_list_of_articles_cleans_description(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>Test Article</title>
                    <description>Test\\n description        with spaces</description>
                    <link>https://example.com/1</link>
                    <pubDate>Mon, 01 Jan 2024 12:00:00 +0000</pubDate>
                </item>
            </channel>
        </rss>"""

        articles = TheHackerNewsSource()._xml_to_list_of_articles(xml)

        assert len(articles) == 1
        assert articles[0].description == "Test description with spaces"

    async def test_get_articles_raises_when_no_articles_in_feed(self, thn_xml: str) -> None:
        with (
            patch_httpx_client_get(thn_xml),
            patch("lightman_ai.sources.the_hacker_news.TheHackerNewsSource._xml_to_list_of_articles", return_value=[]),
            pytest.raises(SourceError),
        ):
            await TheHackerNewsSource().get_articles()
