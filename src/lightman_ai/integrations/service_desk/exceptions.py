import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import httpx
from lightman_ai.core.exceptions import BaseHackermanError

logger = logging.getLogger("lightman")


class BaseServiceDeskError(BaseHackermanError):
    """Base exception for all SERVICE_DESK integration errors."""


class ServiceDeskConnectionError(BaseServiceDeskError):
    """Raised when there are network or connection issues with SERVICE_DESK."""


class ServiceDeskAuthenticationError(BaseServiceDeskError):
    """Raised when authentication with SERVICE_DESK fails."""


class ServiceDeskPermissionError(BaseServiceDeskError):
    """Raised when user lacks permissions to perform the requested operation."""


class MissingIssueIDError(BaseServiceDeskError):
    """Error for when we don't get the issue ID in the response."""

    pass


class ServiceDeskHTTPStatusError(BaseServiceDeskError):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"SERVICE_DESK API error {status_code}: {message}")


class ServiceDeskClientError(ServiceDeskHTTPStatusError):
    """Exception for unmapped HTTP 4xx errors."""

    pass


class ServiceDeskServerError(ServiceDeskHTTPStatusError):
    """Exception for HTTP 5xx errors."""

    pass


class ServiceDeskApiResponseParsingError(BaseServiceDeskError):
    """Raised when SERVICE_DESK API returns an error response that cannot be parsed."""

    def __init__(self, status_code: int, raw_response: str) -> None:
        self.status_code = status_code
        self.raw_response = raw_response
        super().__init__(f"SERVICE_DESK API error {status_code}: Unable to parse error response")


@asynccontextmanager
async def handle_service_desk_exceptions() -> AsyncGenerator[Any, Any]:
    try:
        yield
    except httpx.HTTPStatusError as e:
        if e.response.status_code == httpx.codes.UNAUTHORIZED:
            raise ServiceDeskAuthenticationError from e
        elif e.response.status_code == httpx.codes.FORBIDDEN:
            raise ServiceDeskPermissionError from e
        elif e.response.is_client_error:
            raise ServiceDeskClientError(e.response.status_code, e.response.text) from e
        else:
            raise ServiceDeskServerError(e.response.status_code, e.response.text) from e
    except httpx.TransportError as e:
        raise ServiceDeskConnectionError(f"Network error: {e}") from e
