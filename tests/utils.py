from collections.abc import Iterator
from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, Mock, patch

from lightman_ai.article.models import SelectedArticlesList


@contextmanager
def patch_agent(response: SelectedArticlesList) -> Iterator[Mock]:
    with patch("pydantic_ai.Agent.run", new_callable=AsyncMock) as mock_run:
        mock_result = MagicMock()
        mock_result.output = response
        mock_run.return_value = mock_result
        yield mock_run


@contextmanager
def patch_agent_raise_exception() -> Iterator[Mock]:
    with patch("pydantic_ai.Agent.run", new_callable=AsyncMock) as mock_run:
        mock_run.side_effect = Exception
        yield mock_run
