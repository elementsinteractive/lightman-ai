from unittest.mock import Mock

import pytest
from hackerman_ai.ai.openai.exceptions import (
    InputTooLargeError,
    LimitTokensExceededError,
    UnknownOpenAIError,
    map_exceptions,
)
from openai import RateLimitError


class TestExceptions:
    @pytest.mark.parametrize(
        ("message", "exception"),
        [
            (
                "Error code: 429 - {'error': {'message': 'Request too "
                "large for gpt-4o in organization org- on tokens per min (TPM): "
                "Limit 30000, Used 23513, Requested 7841."
                " Please try again in 3.43s."
                " Visit https://platform.openai.com/account/rate-limits to learn more.', "
                "'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}}",
                LimitTokensExceededError,
            ),
            (
                "Error code: 429 - {'error': {'message': "
                "'Request too large for gpt-4o in organization org- on tokens per min (TPM):"
                " Limit 30000, Requested 78385. The input or output tokens must be reduced in"
                " order to run successfully."
                " Visit https://platform.openai.com/account/rate-limits to learn more.',"
                " 'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}}",
                InputTooLargeError,
            ),
            ("Good morning good afternoon", UnknownOpenAIError),
        ],
    )
    async def test_map_exceptions(self, message: str, exception: Exception) -> None:
        with pytest.raises(exception):  # type: ignore[call-overload]
            async with map_exceptions():
                raise RateLimitError(message, response=Mock(), body=Mock())
