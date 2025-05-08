from typing import Any

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    OPENAI_API_KEY: str = "dummy"

    PROMPT_ITERATIONS: int = 3


settings = Settings(_env_file=".env")
