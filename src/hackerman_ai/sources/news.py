import httpx
import stamina
from hackerman_ai.sources.constants import THN_URL
from httpx import AsyncClient

_RETRY_ON = httpx.TransportError
_ATTEMPTS = 5
_TIMEOUT = 5


async def get_thn_news() -> str:
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
