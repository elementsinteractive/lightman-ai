import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self, cast

import tomlkit
from hackerman_ai.core.exceptions import ConfigNotFoundError, InvalidConfigError, PromptNotFoundError
from pydantic import BaseModel, ConfigDict, PositiveInt, ValidationError

PROMPTS_SECTION = "prompts"
logger = logging.getLogger("hackerman")


def read_config_from_file(*, config_section: str, path: str) -> dict[str, Any]:
    fpath = Path(path)
    if not fpath.exists():
        raise ConfigNotFoundError(f"`{path}` not found!")

    content = fpath.read_text()
    parsed_content = tomlkit.parse(content)

    return cast("dict[str, Any]", parsed_content.get(config_section, {}))


@dataclass
class PromptConfig:
    prompts: dict[str, str]

    @classmethod
    def get_config_from_file(cls, path: str) -> Self:
        config = read_config_from_file(config_section=PROMPTS_SECTION, path=path)
        return cls(prompts=config)

    def get_prompt(self, prompt: str) -> str:
        if prompt not in self.prompts:
            raise PromptNotFoundError(f"prompt `{prompt}` not found in config file")
        return self.prompts[prompt]


class FileConfig(BaseModel):
    iterations: int | None = None
    prompt: str | None = None
    model: str | None = None
    score_threshold: int | None = None

    model_config = ConfigDict(extra="forbid")

    @classmethod
    def get_config_from_file(cls, config_section: str, path: str) -> Self:
        try:
            config = read_config_from_file(config_section=config_section, path=path)
        except ConfigNotFoundError:
            logger.warning("Config file `%s` not found! Proceeding with empty config.", path)
            config = {}
        return cls(**config)


class FinalConfig(BaseModel):
    iterations: PositiveInt
    prompt: str
    model: str
    score_threshold: PositiveInt

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
