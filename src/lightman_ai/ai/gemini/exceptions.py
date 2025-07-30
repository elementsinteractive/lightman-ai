from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from lightman_ai.core.exceptions import BaseLightmanError


class BaseGeminiError(BaseLightmanError): ...


class GeminiError(BaseGeminiError): ...


@contextmanager
def map_gemini_exceptions() -> Generator[Any, Any]:
    try:
        yield
    except Exception as err:
        raise GeminiError from err
