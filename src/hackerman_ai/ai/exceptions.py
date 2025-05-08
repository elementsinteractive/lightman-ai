import math
import re
from abc import ABC
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from openai import RateLimitError


class BaseHackermanError(Exception): ...


class BaseOpenAIError(BaseHackermanError): ...


class UnknownOpenAIError(BaseOpenAIError): ...


class OpenAIRateLimitError(BaseOpenAIError, ABC):
    regex: str

    @classmethod
    def get_match(cls, message: str) -> tuple[str, ...]:
        match = re.search(cls.regex, message)
        return match.groups() if match else ()


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


type TRateLimitErr = type[InputTooLargeError | LimitTokensExceededError]
RATE_LIMIT_ERRORS: list[TRateLimitErr] = [LimitTokensExceededError, InputTooLargeError]


@asynccontextmanager
async def map_exceptions() -> AsyncGenerator[Any, Any]:
    try:
        yield
    except RateLimitError as err:
        for error in RATE_LIMIT_ERRORS:
            if matches := error.get_match(err.message):
                raise error(matches) from err
        raise UnknownOpenAIError from err
