from typing import override
from xml.etree import ElementTree

import httpx
import stamina
from httpx import Client
from lightman_ai.article.models import Article, ArticlesList
from lightman_ai.sources.base import BaseSource

_RETRY_ON = httpx.TransportError
_ATTEMPTS = 5
_TIMEOUT = 5


THN_URL = "https://feeds.feedburner.com/TheHackersNews"


class TheHackerNewsSource(BaseSource):
    @override
    def get_articles(self) -> ArticlesList:
        """Return the articles that are present in THN feed."""
        feed = self.get_feed()
        articles = self._xml_to_list_of_articles(feed)
        return ArticlesList(articles=articles)

    def get_feed(self) -> str:
        """Retrieve the TheHackerNews' RSS Feed."""
        for attempt in stamina.retry_context(
            on=_RETRY_ON,
            attempts=_ATTEMPTS,
            timeout=_TIMEOUT,
        ):
            with Client() as http_client, attempt:
                hacker_news_feed = http_client.get(THN_URL)
                hacker_news_feed.raise_for_status()
        return hacker_news_feed.text

    def _xml_to_list_of_articles(self, xml: str) -> list[Article]:
        root = ElementTree.fromstring(xml)
        channel = root.find("channel")
        assert channel
        items = channel.findall("item")

        parsed = []

        for item in items:
            title = item.findtext("title", default="").strip()
            description = self._clean(item.findtext("description", default="").strip())
            link = item.findtext("link", default="").strip()

            parsed.append(Article(title=title, description=description, link=link))
        return parsed

    @staticmethod
    def _clean(text: str) -> str:
        """Remove non-useful characters."""
        return text.replace("\\n", "").replace("       ", "")
