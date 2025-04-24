import json
from xml.etree import ElementTree

import httpx
import stamina
from httpx import AsyncClient

_RETRY_ON = httpx.TransportError
_ATTEMPTS = 5
_TIMEOUT = 5


THN_URL = "https://feeds.feedburner.com/TheHackersNews"


class TheHackerNewsSource:
    async def get_news(self) -> str:
        """
        Return a stringified list with the news.

        The format is:
            [{"title": title, "description": description, "link": link, "date": pub_date}...]
        """
        feed = await self.get_feed()
        return self._clean(self._xml_to_str(feed))

    async def get_feed(self) -> str:
        """Retrieve the TheHackerNews' RSS Feed."""
        async for attempt in stamina.retry_context(
            on=_RETRY_ON,
            attempts=_ATTEMPTS,
            timeout=_TIMEOUT,
        ):
            async with AsyncClient() as http_client:
                with attempt:
                    hacker_news_feed = await http_client.get(THN_URL)
                    hacker_news_feed.raise_for_status()
        return hacker_news_feed.text

    @staticmethod
    def _xml_to_str(xml_string: str) -> str:
        """Transform an xml into a string that contains all the group of the xml, specifying their fields."""
        root = ElementTree.fromstring(xml_string)
        channel = root.find("channel")
        assert channel
        items = channel.findall("item")

        parsed = []

        for item in items:
            title = item.findtext("title", default="").strip()
            description = item.findtext("description", default="").strip()
            link = item.findtext("link", default="").strip()
            pub_date = item.findtext("pubDate", default="").strip()

            parsed.append({"title": title, "description": description, "link": link, "date": pub_date})
        return json.dumps(parsed)

    @staticmethod
    def _clean(text: str) -> str:
        """Remove non-useful characters."""
        return text.replace("\\n", "").replace("       ", "")
