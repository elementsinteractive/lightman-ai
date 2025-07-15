import logging
import os
from typing import Any, Self

import httpx
import stamina
from lightman_ai.integrations.service_desk.constants import (
    SERVICE_DESK_RETRY_ATTEMPTS,
    SERVICE_DESK_RETRY_ON,
    SERVICE_DESK_RETRY_TIMEOUT,
)
from lightman_ai.integrations.service_desk.exceptions import (
    MissingIssueIDError,
    handle_service_desk_exceptions,
)

logger = logging.getLogger("lightman")


class ServiceDeskIntegration:
    """
    Service Desk integration using httpx to create tickets.

    Provides a simple interface to create Service Desk issues with proper
    authentication and error handling.
    """

    def __init__(
        self,
        base_url: str,
        username: str,
        api_token: str,
        verify_ssl: bool = True,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.api_token = api_token
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            auth=(username, api_token),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            verify=verify_ssl,
            timeout=timeout,
        )

    @classmethod
    def from_env(cls) -> Self:
        required_vars = ["SERVICE_DESK_URL", "SERVICE_DESK_USER", "SERVICE_DESK_TOKEN"]
        missing = [var for var in required_vars if not os.environ.get(var)]
        if missing:
            raise ValueError(f"Missing required environment variable(s): {', '.join(missing)}")
        return cls(
            base_url=os.environ["SERVICE_DESK_URL"],
            username=os.environ["SERVICE_DESK_USER"],
            api_token=os.environ["SERVICE_DESK_TOKEN"],
        )

    async def create_request_of_type(
        self,
        *,
        project_key: str,
        summary: str,
        description: str,
        request_id_type: str,
    ) -> str:
        payload: dict[str, Any] = {
            "serviceDeskId": project_key,
            "requestTypeId": request_id_type,
            "requestFieldValues": {"summary": summary, "description": description},
        }
        for attempt in stamina.retry_context(
            on=SERVICE_DESK_RETRY_ON,
            attempts=SERVICE_DESK_RETRY_ATTEMPTS,
            timeout=SERVICE_DESK_RETRY_TIMEOUT,
        ):
            with attempt:
                async with handle_service_desk_exceptions():
                    response = await self.client.post("/rest/servicedeskapi/request", json=payload)
                    response.raise_for_status()
                    data = response.json()
                    issue_id = data.get("issueId")
                    if not issue_id:
                        raise MissingIssueIDError()
                    logger.info("Successfully created Service Desk issue: %s", issue_id)
        return str(issue_id)
