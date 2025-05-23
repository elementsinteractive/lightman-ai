from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from hackerman_ai.ai.base.exceptions import BaseHackermanError


class BaseGeminiError(BaseHackermanError): ...


class GeminiError(BaseGeminiError): ...


@contextmanager
def map_gemini_exceptions() -> Generator[Any, Any]:
    try:
        yield
    except Exception as err:
        breakpoint()
        raise GeminiError from err
