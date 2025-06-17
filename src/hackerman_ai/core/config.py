import logging
from pathlib import Path
from typing import Any, Self

import tomlkit
from hackerman_ai.core.exceptions import ConfigNotFoundError, InvalidConfigError
from pydantic import BaseModel, ConfigDict, ValidationError

CONFIG_FILE = "hackerman.toml"

logger = logging.getLogger("hackerman")


class FinalConfig(BaseModel):
    iterations: int
    prompt: str
    model: str
    score_threshold: int

    @classmethod
    def init_from_dict(cls, data: dict[str, Any]) -> Self:
        try:
            return cls(**data)
        except ValidationError as error:
            error_list = []
            for err in error.errors():
                error_list.append(f"`{err['loc'][0]}`: {err['msg']}")
            err_msg = f"Invalid configuration provided: [{','.join(error_list)}]"
            raise InvalidConfigError(err_msg) from error


class FileConfig(BaseModel):
    iterations: int | None = None
    prompt: str | None = None
    model: str | None = None
    score_threshold: int | None = None

    model_config = ConfigDict(extra="forbid")

    @staticmethod
    def get_fpath(path: str | None) -> Path:
        if not path:
            return Path(CONFIG_FILE)
        return Path(path)

    @classmethod
    def get_config_from_file(cls, path: str | None = None) -> Self:
        fpath = cls.get_fpath(path)
        if not fpath.exists():
            if path:
                raise ConfigNotFoundError()

            logger.warning("Config file not %s found! Proceeding with empty config.", CONFIG_FILE)
            return cls()

        content = fpath.read_text()
        parsed_content = tomlkit.parse(content)

        return cls(**parsed_content.get("settings", {}))
