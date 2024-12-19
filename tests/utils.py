from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, patch


@asynccontextmanager
async def patch_agent() -> AsyncIterator[None]:
    with patch("pydantic_ai.Agent.run", new=AsyncMock()):
        yield
