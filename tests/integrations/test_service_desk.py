from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest
from lightman_ai.integrations.service_desk.exceptions import (
    MissingIssueIDError,
    ServiceDeskAuthenticationError,
    ServiceDeskClientError,
    ServiceDeskConnectionError,
    ServiceDeskPermissionError,
)
from lightman_ai.integrations.service_desk.integration import ServiceDeskIntegration


@pytest.fixture
def service_desk_integration() -> ServiceDeskIntegration:
    return ServiceDeskIntegration(
        base_url="https://test.atlassian.net", username="user@example.com", api_token="token123"
    )


@pytest.mark.usefixtures("patch_service_desk_retry_wait_max")
class TestServiceDeskIntegration:
    async def test_create_request_of_type_success(self, service_desk_integration: ServiceDeskIntegration) -> None:
        mock_response = AsyncMock()
        mock_response.status_code = 201
        sync_mock = Mock()
        sync_mock.return_value = {"issueId": "PROJ-1"}
        mock_response.json = sync_mock
        mock_response.raise_for_status.return_value = None
        with patch.object(service_desk_integration.client, "post", return_value=mock_response):
            key = await service_desk_integration.create_request_of_type(
                project_key="PROJ", summary="summary", description="desc", request_id_type="REQ_TYPE"
            )
        assert key == "PROJ-1"

    async def test_create_request_of_type_auth_error(self, service_desk_integration: ServiceDeskIntegration) -> None:
        mock_response = AsyncMock()
        mock_response.status_code = 401
        http_error = httpx.HTTPStatusError(message="Unauthorized", request=AsyncMock(), response=mock_response)
        with (
            patch.object(service_desk_integration.client, "post", side_effect=http_error),
            pytest.raises(ServiceDeskAuthenticationError),
        ):
            await service_desk_integration.create_request_of_type(
                project_key="PROJ", summary="summary", description="desc", request_id_type="REQ_TYPE"
            )

    async def test_create_request_of_type_permission_error(
        self, service_desk_integration: ServiceDeskIntegration
    ) -> None:
        mock_response = AsyncMock()
        mock_response.status_code = 403
        http_error = httpx.HTTPStatusError(message="Forbidden", request=AsyncMock(), response=mock_response)
        with (
            patch.object(service_desk_integration.client, "post", side_effect=http_error),
            pytest.raises(ServiceDeskPermissionError),
        ):
            await service_desk_integration.create_request_of_type(
                project_key="PROJ", summary="summary", description="desc", request_id_type="REQ_TYPE"
            )

    async def test_create_request_of_type_api_error(self, service_desk_integration: ServiceDeskIntegration) -> None:
        mock_response = AsyncMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"errorMessages": ["Some error"]}
        mock_response.text = "Bad Request"
        http_error = httpx.HTTPStatusError(message="Bad Request", request=AsyncMock(), response=mock_response)
        with (
            patch.object(service_desk_integration.client, "post", side_effect=http_error),
            pytest.raises(ServiceDeskClientError),
        ):
            await service_desk_integration.create_request_of_type(
                project_key="PROJ", summary="summary", description="desc", request_id_type="REQ_TYPE"
            )

    async def test_create_request_of_type_connection_error(
        self, service_desk_integration: ServiceDeskIntegration
    ) -> None:
        connection_error = httpx.ConnectError("Connection refused")
        with (
            patch.object(service_desk_integration.client, "post", side_effect=connection_error),
            pytest.raises(ServiceDeskConnectionError),
        ):
            await service_desk_integration.create_request_of_type(
                project_key="PROJ", summary="summary", description="desc", request_id_type="REQ_TYPE"
            )

    async def test_create_request_of_type_timeout_error(self, service_desk_integration: ServiceDeskIntegration) -> None:
        timeout_error = httpx.TimeoutException("Timeout!")
        with (
            patch.object(service_desk_integration.client, "post", side_effect=timeout_error),
            pytest.raises(ServiceDeskConnectionError),
        ):
            await service_desk_integration.create_request_of_type(
                project_key="PROJ", summary="summary", description="desc", request_id_type="REQ_TYPE"
            )

    async def test_create_request_of_type_missing_key(self, service_desk_integration: ServiceDeskIntegration) -> None:
        mock_response = AsyncMock()
        mock_response.status_code = 201
        sync_mock = Mock()
        sync_mock.return_value = {"anotherKEy": "PROJ-1"}
        mock_response.json = sync_mock
        mock_response.raise_for_status.return_value = None
        with (
            patch.object(service_desk_integration.client, "post", return_value=mock_response),
            pytest.raises(MissingIssueIDError),
        ):
            await service_desk_integration.create_request_of_type(
                project_key="PROJ", summary="summary", description="desc", request_id_type="REQ_TYPE"
            )

    def test_base_url_trailing_slash(self) -> None:
        inst = ServiceDeskIntegration(
            base_url="https://test.atlassian.net/",
            username="user@example.com",
            api_token="token123",
        )
        assert not inst.base_url.endswith("/")

    def test_from_env_success(self) -> None:
        env = {
            "SERVICE_DESK_URL": "https://test.atlassian.net",
            "SERVICE_DESK_USER": "user@example.com",
            "SERVICE_DESK_TOKEN": "token123",
        }
        with patch.dict("os.environ", env, clear=True):
            inst = ServiceDeskIntegration.from_env()
            assert inst.base_url == "https://test.atlassian.net"
            assert inst.username == "user@example.com"
            assert inst.api_token == "token123"

    def test_from_env_missing(self) -> None:
        with (
            patch.dict("os.environ", {}, clear=True),
            pytest.raises(ValueError, match="Missing required environment variable"),
        ):
            ServiceDeskIntegration.from_env()

    async def test_create_request_of_type_payload(self, service_desk_integration: ServiceDeskIntegration) -> None:
        mock_response = AsyncMock()
        mock_response.status_code = 201
        sync_mock = Mock()
        sync_mock.return_value = {"issueId": "PROJ-1"}
        mock_response.json = sync_mock
        mock_response.raise_for_status.return_value = None
        with patch.object(service_desk_integration.client, "post", return_value=mock_response) as post_mock:
            await service_desk_integration.create_request_of_type(
                project_key="PROJ", summary="summary", description="desc", request_id_type="REQ_TYPE"
            )
            post_mock.assert_called_once()
            _, kwargs = post_mock.call_args
            assert kwargs["json"] == {
                "serviceDeskId": "PROJ",
                "requestTypeId": "REQ_TYPE",
                "requestFieldValues": {"summary": "summary", "description": "desc"},
            }

    async def test_create_request_of_type_logs_success(
        self, service_desk_integration: ServiceDeskIntegration, caplog: pytest.LogCaptureFixture
    ) -> None:
        mock_response = AsyncMock()
        mock_response.status_code = 201
        sync_mock = Mock()
        sync_mock.return_value = {"issueId": "PROJ-1"}
        mock_response.json = sync_mock
        mock_response.raise_for_status.return_value = None
        with patch.object(service_desk_integration.client, "post", return_value=mock_response), caplog.at_level("INFO"):
            await service_desk_integration.create_request_of_type(
                project_key="PROJ", summary="summary", description="desc", request_id_type="REQ_TYPE"
            )
        assert any("Successfully created Service Desk issue: PROJ-1" in m for m in caplog.messages)
