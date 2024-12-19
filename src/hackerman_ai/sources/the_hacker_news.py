from hackerman_ai.sources.constants import THN_URL
from httpx import AsyncClient


class TheHackerNewsSource:
    @classmethod
    async def get_news(cls) -> str:
        async with AsyncClient() as http_client:
            hacker_news_feed = await http_client.get(THN_URL)
            hacker_news_feed.raise_for_status()
        return hacker_news_feed.text
