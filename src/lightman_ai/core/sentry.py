import logging
import os
from importlib import metadata

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


def configure_sentry() -> None:
    """Configure Sentry for error tracking and performance monitoring using env vars with fallbacks."""
    try:
        if not os.getenv("SENTRY_DSN"):
            logging.getLogger("lightman").info("SENTRY_DSN not configured, skipping Sentry initialization")
            return

        # Logging level from ENV
        logging_level_str = os.getenv("LOGGING_LEVEL", "ERROR").upper()
        logging_level = getattr(logging, logging_level_str, logging.ERROR)

        # Set up logging integration
        sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging_level)

        sentry_sdk.init(
            release=metadata.version("lightman-ai"),
            integrations=[sentry_logging],
        )
    except Exception as e:
        logging.getLogger("lightman").warning("Could not instantiate Sentry! %s.\nContinuing with the execution.", e)
