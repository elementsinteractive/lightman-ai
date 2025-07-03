import math
import re
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, override

from lightman_ai.core.exceptions import BaseHackermanError
from pydantic_ai.exceptions import ModelHTTPError

from openai import RateLimitError


class BaseOpenAIError(BaseHackermanError): ...


class UnknownOpenAIError(BaseOpenAIError): ...


class OpenAIRateLimitError(BaseOpenAIError):
    regex: str

    @classmethod
    def get_matches(cls, message: str) -> tuple[str, ...]:
        match = re.search(cls.regex, message)
        return match.groups() if match else ()

    @classmethod
    def is_match(cls, message: str) -> bool:
        return bool(re.search(cls.regex, message))


class InputTooLargeError(OpenAIRateLimitError):
    limit: int
    requested: int

    regex: str = (
        r"Limit (\d+), Requested (\d+)\. The input or output tokens must be reduced in order to run successfully\."
    )

    def __init__(self, values: tuple[str, ...]) -> None:
        self.limit = int(values[0])
        self.requested = int(values[1])


class LimitTokensExceededError(OpenAIRateLimitError):
    limit: int
    used: int
    requested: int
    wait_time: int

    regex = r"Limit (\d+), Used (\d+), Requested (\d+)\. Please try again in (\d+\.?(\d+)?)s\."

    def __init__(self, values: tuple[str, ...]) -> None:
        self.limit = int(values[0])
        self.used = int(values[1])
        self.requested = int(values[2])
        self.wait_time = math.ceil(float(values[3]))


class QuotaExceededError(OpenAIRateLimitError):
    regex = r"You exceeded your current quota"

    @override
    @classmethod
    def get_matches(cls, message: str) -> tuple[str, ...]:
        match = re.search(cls.regex, message)
        return match.groups() if match else ()


type TRateLimitErr = type[InputTooLargeError | LimitTokensExceededError]
RATE_LIMIT_ERRORS: list[TRateLimitErr] = [LimitTokensExceededError, InputTooLargeError]


@contextmanager
def map_openai_exceptions() -> Generator[Any, Any]:
    try:
        yield
    except RateLimitError as err:
        for error in RATE_LIMIT_ERRORS:
            if matches := error.get_matches(err.message):
                raise error(matches) from err
        raise UnknownOpenAIError from err
    except ModelHTTPError as err:
        if QuotaExceededError.is_match(err.message):
            raise QuotaExceededError() from err
