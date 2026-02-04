import logging
from datetime import UTC, datetime
from typing import override
from xml.etree import ElementTree

import httpx
import stamina
from httpx import AsyncClient
from lightman_ai.article.models import Article, ArticlesList
from lightman_ai.sources.base import BaseSource
from lightman_ai.sources.exceptions import IncompleteArticleFromSourceError, MalformedSourceResponseError
from pydantic import ValidationError

logger = logging.getLogger("lightman")

_RETRY_ON = httpx.TransportError
_ATTEMPTS = 5
_TIMEOUT = 5

BLEEPING_COMPUTER_URL = "https://news.google.com/rss/search?q=site:bleepingcomputer.com&hl=en-US&gl=US&ceid=US:en"


class BleepingComputerSource(BaseSource):
    @override
    async def get_articles(self, date: datetime | None = None) -> ArticlesList:
        """Return the articles that are present in BleepingComputer feed."""
        logger.info("Downloading articles from %s", BLEEPING_COMPUTER_URL)
        feed = await self.get_feed()
        articles = self._xml_to_list_of_articles(feed)
        logger.info("Articles properly downloaded and parsed.")
        if date:
            return ArticlesList.get_articles_from_date_onwards(articles=articles, start_date=date)
        else:
            return ArticlesList(articles=articles)

    async def get_feed(self) -> str:
        """Retrieve the BleepingComputer RSS Feed."""
        async with AsyncClient() as http_client:
            for attempt in stamina.retry_context(
                on=_RETRY_ON,
                attempts=_ATTEMPTS,
                timeout=_TIMEOUT,
            ):
                with attempt:
                    bleeping_computer_feed = await http_client.get(BLEEPING_COMPUTER_URL)
                    bleeping_computer_feed.raise_for_status()
        return bleeping_computer_feed.text

    def _xml_to_list_of_articles(self, xml: str) -> list[Article]:
        try:
            root = ElementTree.fromstring(xml)
        except ElementTree.ParseError as e:
            raise MalformedSourceResponseError(f"Invalid XML format: {e}") from e

        channel = root.find("channel")
        if channel is None:
            raise MalformedSourceResponseError("No channel element found in RSS feed")

        items = channel.findall("item")
        parsed = []

        for item in items:
            try:
                title = item.findtext("title", default="").strip()
                description = self._clean(item.findtext("description", default="").strip())
                link = item.findtext("link", default="").strip()
                published_at_str = item.findtext("pubDate", default="").strip()

                if not published_at_str:
                    logger.exception("Missing publication date. link: `%s`", link)
                    raise IncompleteArticleFromSourceError()

                published_at = datetime.strptime(published_at_str, "%a, %d %b %Y %H:%M:%S %Z")
                if published_at.tzinfo is None:
                    published_at = published_at.replace(tzinfo=UTC)

                parsed.append(Article(title=title, description=description, link=link, published_at=published_at))

            except (ValidationError, ValueError, IncompleteArticleFromSourceError) as e:
                logger.warning("Failed to parse article. title: `%s`, link: `%s`, error: %s", title, link, str(e))

        return parsed

    @staticmethod
    def _clean(text: str) -> str:
        """Remove CDATA wrappers and non-useful characters."""
        # Remove CDATA wrapper if present
        if text.startswith("<![CDATA[") and text.endswith("]]>"):
            text = text[9:-3]  # Remove <![CDATA[ and ]]>

        # Clean up formatting
        return text.replace("\\n", "").replace("       ", "").strip()
