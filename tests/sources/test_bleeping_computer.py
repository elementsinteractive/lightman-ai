from datetime import UTC, datetime

import pytest
from lightman_ai.article.models import ArticlesList
from lightman_ai.sources.bleeping_computer import BleepingComputerSource
from lightman_ai.sources.exceptions import MalformedSourceResponseError
from tests.conftest import patch_httpx_client_get


class TestBleepingComputerSource:
    def test_clean(self) -> None:
        # Test basic cleaning
        string_to_clean = "\\na       "
        result = BleepingComputerSource()._clean(string_to_clean)
        assert result == "a"

    def test_clean_cdata_with_brackets(self) -> None:
        # Test CDATA with content that has brackets
        cdata_string = "<![CDATA[ A new GlassWorm malware attack through compromised OpenVSX extensions focuses on stealing passwords. [...] ]]>"
        result = BleepingComputerSource()._clean(cdata_string)
        assert (
            result
            == "A new GlassWorm malware attack through compromised OpenVSX extensions focuses on stealing passwords. [...]"
        )

    async def test_get_articles(self, bc_xml: str) -> None:
        with patch_httpx_client_get(bc_xml):
            articles = await BleepingComputerSource().get_articles()

        assert isinstance(articles, ArticlesList)
        # Based on the provided XML sample, there should be 5 articles
        assert len(articles.articles) == 5

        # Check the first article details
        first_article = articles.articles[0]
        assert (
            first_article.title
            == "Coinbase confirms insider breach linked to leaked support tool screenshots - BleepingComputer"
        )
        assert first_article.link == "https://news.google.com/rss/articles/coinbase-insider-breach"
        assert first_article.description == "Coinbase confirms insider breach linked to leaked support tool screenshots"

        # Check that the date is parsed correctly (Wed, 04 Feb 2026 02:04:23 GMT)
        expected_date = datetime(2026, 2, 4, 2, 4, 23, tzinfo=UTC)
        assert first_article.published_at == expected_date

    def test_xml_to_list_of_articles_no_channel(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
        </rss>"""

        with pytest.raises(MalformedSourceResponseError, match="No channel element found in RSS feed"):
            BleepingComputerSource()._xml_to_list_of_articles(xml)

    def test_xml_error(self) -> None:
        xml = ""

        with pytest.raises(MalformedSourceResponseError, match="Invalid XML format"):
            BleepingComputerSource()._xml_to_list_of_articles(xml)

    def test_xml_to_list_of_articles_missing_pub_date(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>Test Article</title>
                    <description><![CDATA[ Test description ]]></description>
                    <link>https://example.com/1</link>
                </item>
            </channel>
        </rss>"""

        assert not BleepingComputerSource()._xml_to_list_of_articles(xml)

    def test_xml_to_list_of_articles_empty_pub_date(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <title>Test Article</title>
                    <description><![CDATA[ Test description ]]></description>
                    <link>https://example.com/1</link>
                    <pubDate></pubDate>
                </item>
            </channel>
        </rss>"""

        assert not BleepingComputerSource()._xml_to_list_of_articles(xml)

    def test_xml_to_list_of_articles_validation_error(self) -> None:
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <item>
                    <description><![CDATA[ Test description ]]></description>
                    <link>https://example.com/1</link>
                    <pubDate>Mon, 02 Feb 2026 17:04:19 GMT</pubDate>
                </item>
            </channel>
        </rss>"""  # no title

        assert not BleepingComputerSource()._xml_to_list_of_articles(xml)
