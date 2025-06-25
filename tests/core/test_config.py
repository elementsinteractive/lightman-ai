import pathlib

import pytest
from hackerman_ai.constants import DEFAULT_CONFIG_FILE, DEFAULT_CONFIG_SECTION
from hackerman_ai.core.config import FileConfig, FinalConfig, PromptConfig
from hackerman_ai.core.exceptions import ConfigNotFoundError, InvalidConfigError, PromptNotFoundError
from pydantic import ValidationError
from tests.conftest import patch_config_file


class TestConfig:
    def test_get_from_file(self) -> None:
        content = """
        [default]
        iterations = 3
        model = 'gpt-4.1'
        score_threshold = 8
        prompt = 'eval-prompt'
        """
        with patch_config_file(content=content):
            config = FileConfig.get_config_from_file(config_section=DEFAULT_CONFIG_SECTION, path=DEFAULT_CONFIG_FILE)

        assert config.iterations == 3
        assert config.model == "gpt-4.1"
        assert config.score_threshold == 8
        assert config.prompt == "eval-prompt"

    def test_get_from_file_empty(self) -> None:
        content = ""
        with patch_config_file(content=content):
            config = FileConfig.get_config_from_file(config_section=DEFAULT_CONFIG_SECTION, path=DEFAULT_CONFIG_FILE)

        assert config.iterations is None
        assert config.model is None
        assert config.score_threshold is None

    def test_get_from_file_does_not_accept_random_keys(self) -> None:
        content = """[default]
        random_key = 1"""
        with pytest.raises(ValidationError), patch_config_file(content):
            FileConfig.get_config_from_file(config_section=DEFAULT_CONFIG_SECTION, path=DEFAULT_CONFIG_FILE)

    def test_load_different_config(self) -> None:
        content = """[default]
        iterations = 1
        [settings]
        iterations = 2"""
        with patch_config_file(content):
            config = FileConfig.get_config_from_file(config_section="settings", path=DEFAULT_CONFIG_FILE)
        assert config.iterations == 2

    def test_get_from_file_config_not_found_and_no_path_specified(self) -> None:
        with patch_config_file(exists=False):
            config = FileConfig.get_config_from_file(config_section=DEFAULT_CONFIG_SECTION, path=DEFAULT_CONFIG_FILE)

        assert config.iterations is None
        assert config.model is None
        assert config.score_threshold is None
        assert config.prompt is None

    def test_file_is_loaded_from_location(self, tmp_path: pathlib.Path) -> None:
        path = "my_path.toml"
        content = """
        [default]
        iterations = 3
        model = 'gpt-4.1'
        score_threshold = 8
        prompt = 'eval-prompt'
        """
        fpath = tmp_path / path
        fpath.write_text(content)
        config = FileConfig.get_config_from_file(config_section=DEFAULT_CONFIG_SECTION, path=str(fpath))

        assert config.iterations == 3
        assert config.model == "gpt-4.1"
        assert config.score_threshold == 8
        assert config.prompt == "eval-prompt"


class TestFinalConfig:
    def test_init_error(self) -> None:
        with pytest.raises(InvalidConfigError) as exc:
            FinalConfig.init_from_dict({})
        assert (
            exc.value.args[0] == "Invalid configuration provided: [`iterations`: Field required,"
            "`prompt`: Field required,"
            "`model`: Field required,"
            "`score_threshold`: Field required]"
        )

    def test_iterations_must_be_positive_int(self) -> None:
        with pytest.raises(InvalidConfigError) as exc:
            FinalConfig.init_from_dict(
                {
                    "iterations": 0,
                }
            )
        assert "`iterations`: Input should be greater than 0" in exc.value.args[0]

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
