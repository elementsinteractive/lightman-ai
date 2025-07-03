from unittest.mock import Mock

import pytest
from lightman_ai.ai.openai.exceptions import (
    InputTooLargeError,
    LimitTokensExceededError,
    QuotaExceededError,
    UnknownOpenAIError,
    map_openai_exceptions,
)
from openai import RateLimitError
from pydantic_ai.exceptions import ModelHTTPError


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
    def test_map_openai_exceptions(self, message: str, exception: Exception) -> None:
        with pytest.raises(exception), map_openai_exceptions():  # type: ignore[call-overload]
            raise RateLimitError(message, response=Mock(), body=Mock())

    def test_map_quota_exceeded_exception(self) -> None:
        body = {
            "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.",
            "type": "insufficient_quota",
            "param": None,
            "code": "insufficient_quota",
        }
        with pytest.raises(QuotaExceededError), map_openai_exceptions():
            raise ModelHTTPError(status_code=Mock(), model_name=Mock(), body=body)
