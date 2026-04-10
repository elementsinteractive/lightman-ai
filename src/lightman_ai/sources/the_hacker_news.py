import logging
from datetime import datetime
from typing import override
from xml.etree import ElementTree

import httpx
import stamina
from httpx import AsyncClient
from lightman_ai.article.models import Article, ArticlesList
from lightman_ai.sources.base import BaseSource
from lightman_ai.sources.exceptions import MalformedSourceResponseError, NoArticlesError, SourceError
from pydantic import ValidationError

logger = logging.getLogger("lightman")

_RETRY_ON = httpx.TransportError
_ATTEMPTS = 5
_TIMEOUT = 5


THN_URL = "https://feeds.feedburner.com/TheHackersNews"


class TheHackerNewsSource(BaseSource):
    @override
    async def get_articles(self, date: datetime | None = None) -> ArticlesList:
        """Return the articles that are present in THN feed."""
        try:
            logger.info("Downloading articles from %s", THN_URL)
            feed = await self.get_feed()
            articles = self._xml_to_list_of_articles(feed)
            if not articles:
                raise NoArticlesError
            logger.info("Articles properly downloaded and parsed.")
            if date:
                return ArticlesList.get_articles_from_date_onwards(articles=articles, start_date=date)
            else:
                return ArticlesList(articles=articles)
        except Exception as e:
            raise SourceError("Could not download articles from THN source") from e

    async def get_feed(self) -> str:
        """Retrieve the TheHackerNews' RSS Feed."""
        async with AsyncClient() as http_aclient:
            for attempt in stamina.retry_context(
                on=_RETRY_ON,
                attempts=_ATTEMPTS,
                timeout=_TIMEOUT,
            ):
                with attempt:
                    hacker_news_feed = await http_aclient.get(THN_URL)
                    hacker_news_feed.raise_for_status()
        return hacker_news_feed.text

    def _xml_to_list_of_articles(self, xml: str) -> list[Article]:
        """Parse the XML and return in as a list of Articles."""
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
                    logger.error("Missing publication date. link: `%s`", link)
                    raise ValueError
                published_at = datetime.strptime(published_at_str, "%a, %d %b %Y %H:%M:%S %z")

                parsed.append(Article(title=title, description=description, link=link, published_at=published_at))
            except (ValidationError, ValueError):
                logger.warning("Could not parse article %s", link)

        return parsed

    @staticmethod
    def _clean(text: str) -> str:
        """Remove non-useful characters. Helps cleaning the fields that will be sent to the Agent."""
        return text.replace("\\n", "").replace("       ", "")
