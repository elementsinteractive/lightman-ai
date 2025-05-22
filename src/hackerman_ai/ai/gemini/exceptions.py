from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from hackerman_ai.ai.base.exceptions import BaseHackermanError


class BaseGeminiError(BaseHackermanError): ...


class GeminiError(BaseGeminiError): ...


@asynccontextmanager
async def map_gemini_exceptions() -> AsyncGenerator[Any, Any]:
    try:
        yield
    except Exception as err:
        raise GeminiError from err
