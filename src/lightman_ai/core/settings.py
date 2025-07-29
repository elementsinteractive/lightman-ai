from typing import Any

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    PARALLEL_WORKERS: int = 5
    TIME_ZONE: str = "UTC"


settings = Settings()
