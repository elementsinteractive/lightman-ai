import httpx
from lightman_ai.integrations.service_desk.exceptions import ServiceDeskServerError

# Retry configuration for ServiceDeskIntegration
SERVICE_DESK_RETRY_ON = (httpx.TransportError, httpx.TimeoutException, ServiceDeskServerError)
SERVICE_DESK_RETRY_ATTEMPTS = 3
SERVICE_DESK_RETRY_TIMEOUT = 10
