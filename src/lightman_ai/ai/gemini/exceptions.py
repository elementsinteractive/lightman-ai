from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from lightman_ai.core.exceptions import BaseLightmanError

if TYPE_CHECKING:
    from collections.abc import Generator


class BaseGeminiError(BaseLightmanError): ...


class GeminiError(BaseGeminiError): ...


@contextmanager
def map_gemini_exceptions() -> Generator[Any, Any]:
    try:
        yield
    except Exception as err:
        raise GeminiError from err
