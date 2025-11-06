import logging
import os
from importlib import metadata

logger = logging.getLogger("lightman")


def configure_sentry(log_level: int) -> None:
    """Configure Sentry for error tracking."""
    try:
        import sentry_sdk  # noqa: PLC0415
        from sentry_sdk.integrations.logging import LoggingIntegration  # noqa: PLC0415
    except ImportError:
        if os.getenv("SENTRY_DSN"):
            logger.warning(
                "Could not initialize sentry, it is not installed! Install lightman with `pip install lightman-ai[sentry]` to solve it."
            )
        return

    if not os.getenv("SENTRY_DSN"):
        logger.warning("SENTRY_DSN not configured, skipping Sentry initialization")
        return

    try:
        sentry_logging = LoggingIntegration(level=logging.INFO, event_level=log_level)

        sentry_sdk.init(
            release=metadata.version("lightman-ai"),
            integrations=[sentry_logging],
        )
    except Exception as e:
        logger.warning("Could not instantiate Sentry! %s.\nContinuing with the execution.", e)
