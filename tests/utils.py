from contextlib import contextmanager
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, MagicMock, Mock, patch

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator

    from lightman_ai.article.models import Article, SelectedArticlesList


@contextmanager
def patch_agent(response: SelectedArticlesList) -> Iterator[Mock]:
    with patch("pydantic_ai.Agent.run", new_callable=AsyncMock) as mock_run:
        mock_result = MagicMock()
        mock_result.output = response
        mock_run.return_value = mock_result
        yield mock_run


@contextmanager
def patch_get_articles_from_xml(articles: list[Article]) -> Generator[Any, Mock, Any]:
    with patch("lightman_ai.sources.the_hacker_news.TheHackerNewsSource._xml_to_list_of_articles") as mock:
        mock.return_value = articles
        yield mock


@contextmanager
def patch_agent_raise_exception() -> Iterator[Mock]:
    with patch("pydantic_ai.Agent.run", new_callable=AsyncMock) as mock_run:
        mock_run.side_effect = Exception
        yield mock_run
