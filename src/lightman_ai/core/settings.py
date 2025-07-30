import logging
from pathlib import Path
from typing import Any, Self

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("lightman")


class Settings(BaseSettings):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    AGENT: str = "openai"
    SCORE: int = 8
    TIME_ZONE: str = "UTC"
    model_config = SettingsConfigDict(extra="ignore")

    @classmethod
    def try_load_from_file(cls, env_file: str | None = None) -> Self:
        """
        Initialize Settings class and returns an instance.

        It tries to load env variables from the env file. Variables set in the environment take precendence.

        If the env file is not present, it continues execution, following pydantic-settings' behaviour.
        """
        if env_file and not Path(env_file).exists():
            logger.warning("env file `%s` not found.", env_file)
        return cls(_env_file=env_file)
