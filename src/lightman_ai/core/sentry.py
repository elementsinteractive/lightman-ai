import logging
import os
from importlib import metadata

logger = logging.getLogger("lightman")


def configure_sentry() -> None:
    """Configure Sentry for error tracking."""
    try:
        import sentry_sdk
        from sentry_sdk.integrations.logging import LoggingIntegration
    except ImportError:
        logger.warning(
            "Could not initialize sentry, it is not installed! Add it by installing the project with `lightman-ai[sentry]`."
        )
        return

    try:
        if not os.getenv("SENTRY_DSN"):
            logger.info("SENTRY_DSN not configured, skipping Sentry initialization")
            return

        logging_level_str = os.getenv("LOGGING_LEVEL", "ERROR").upper()
        try:
            logging_level = getattr(logging, logging_level_str, logging.ERROR)
        except AttributeError:
            logger.warning("The specified logging level `%s` does not exist. Defaulting to ERROR.", logging_level_str)
            logging_level = logging.ERROR

        # Set up logging integration
        sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging_level)

        sentry_sdk.init(
            release=metadata.version("lightman-ai"),
            integrations=[sentry_logging],
        )
    except Exception as e:
        logger.warning("Could not instantiate Sentry! %s.\nContinuing with the execution.", e)
