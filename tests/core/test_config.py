import pathlib

import pytest
from lightman_ai.constants import DEFAULT_CONFIG_FILE, DEFAULT_CONFIG_SECTION
from lightman_ai.core.config import FileConfig, FinalConfig, PromptConfig
from lightman_ai.core.exceptions import ConfigNotFoundError, InvalidConfigError, PromptNotFoundError
from pydantic import ValidationError
from tests.conftest import patch_config_file


class TestConfig:
    def test_get_from_file(self) -> None:
        content = """
        [default]
        agent = 'openai'
        score_threshold = 8
        prompt = 'eval-prompt'
        """
        with patch_config_file(content=content):
            config = FileConfig.get_config_from_file(config_section=DEFAULT_CONFIG_SECTION, path=DEFAULT_CONFIG_FILE)

        assert config.agent == "openai"
        assert config.score_threshold == 8
        assert config.prompt == "eval-prompt"

    def test_get_from_file_empty(self) -> None:
        content = ""
        with patch_config_file(content=content):
            config = FileConfig.get_config_from_file(config_section=DEFAULT_CONFIG_SECTION, path=DEFAULT_CONFIG_FILE)

        assert config.agent is None
        assert config.score_threshold is None

    def test_get_from_file_does_not_accept_random_keys(self) -> None:
        content = """[default]
        random_key = 1"""
        with pytest.raises(ValidationError), patch_config_file(content):
            FileConfig.get_config_from_file(config_section=DEFAULT_CONFIG_SECTION, path=DEFAULT_CONFIG_FILE)

    def test_load_different_config(self) -> None:
        content = """[default]
        agent = 'openai'
        [settings]
        agent = 'gpt-4.2'"""
        with patch_config_file(content):
            config = FileConfig.get_config_from_file(config_section="settings", path=DEFAULT_CONFIG_FILE)
        assert config.agent == "gpt-4.2"

    def test_get_from_file_config_not_found_and_no_path_specified(self) -> None:
        with patch_config_file(exists=False):
            config = FileConfig.get_config_from_file(config_section=DEFAULT_CONFIG_SECTION, path=DEFAULT_CONFIG_FILE)

        assert config.agent is None
        assert config.agent is None
        assert config.score_threshold is None
        assert config.prompt is None

    def test_file_is_loaded_from_location(self, tmp_path: pathlib.Path) -> None:
        path = "my_path.toml"
        content = """
        [default]
        agent = 'openai'
        score_threshold = 8
        prompt = 'eval-prompt'
        """
        fpath = tmp_path / path
        fpath.write_text(content)
        config = FileConfig.get_config_from_file(config_section=DEFAULT_CONFIG_SECTION, path=str(fpath))

        assert config.agent == "openai"
        assert config.score_threshold == 8
        assert config.prompt == "eval-prompt"

    def test_service_desk_fields_accept_str(self) -> None:
        config = FileConfig(
            prompt="prompt1",
            agent="openai",
            score_threshold=7,
            service_desk_project_key="123",
            service_desk_request_id_type="456",
        )
        assert config.service_desk_project_key == "123"
        assert config.service_desk_request_id_type == "456"

    def test_service_desk_fields_cast_int(self) -> None:
        config = FileConfig(
            prompt="prompt1",
            agent="openai",
            score_threshold=7,
            service_desk_project_key=123,  # type: ignore[arg-type]
            service_desk_request_id_type=456,  # type: ignore[arg-type]
        )
        assert config.service_desk_project_key == "123"
        assert config.service_desk_request_id_type == "456"

    def test_service_desk_fields_reject_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="must be a number"):
            FileConfig(
                prompt="prompt1",
                agent="openai",
                score_threshold=7,
                service_desk_project_key="notanumber",
                service_desk_request_id_type=None,
            )

    def test_service_desk_fields_accept_none(self) -> None:
        config = FileConfig(
            prompt="prompt1",
            agent="openai",
            score_threshold=7,
            service_desk_project_key=None,
            service_desk_request_id_type=None,
        )
        assert config.service_desk_project_key is None
        assert config.service_desk_request_id_type is None


class TestFinalConfig:
    def test_init_error(self) -> None:
        with pytest.raises(InvalidConfigError) as exc:
            FinalConfig.init_from_dict({})
        assert (
            exc.value.args[0] == "Invalid configuration provided: [`prompt`: Field required,"
            "`agent`: Field required,"
            "`score_threshold`: Field required]"
        )

    def test_score_must_be_positive_int(self) -> None:
        with pytest.raises(InvalidConfigError) as exc:
            FinalConfig.init_from_dict(
                {
                    "score_threshold": 0,
                }
            )
        assert "`score_threshold`: Input should be greater than 0" in exc.value.args[0]


class TestPromptConfig:
    def test_wrong_prompt(self) -> None:
        with pytest.raises(PromptNotFoundError) as exc:
            PromptConfig(prompts={}).get_prompt("aaa")
        assert exc.value.args[0] == "prompt `aaa` not found in config file"

    def test_prompt_is_loaded_from_file(self, tmp_path: pathlib.Path) -> None:
        path = "my_path.toml"
        content = """
        [prompts]
        eval = "my eval prompt"
        """
        fpath = tmp_path / path
        fpath.write_text(content)
        config = PromptConfig.get_config_from_file(path=str(fpath))

        assert config.prompts == {"eval": "my eval prompt"}

    def test_raises_error_if_file_not_found(self) -> None:
        with patch_config_file(exists=False), pytest.raises(ConfigNotFoundError):
            PromptConfig.get_config_from_file(path="fake_path")
