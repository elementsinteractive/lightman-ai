from datetime import datetime
from unittest.mock import ANY, Mock, call, patch
from zoneinfo import ZoneInfo

import pytest
from click.testing import CliRunner
from freezegun import freeze_time
from lightman_ai import cli
from lightman_ai.core.config import FileConfig, PromptConfig
from tests.conftest import patch_config_file


class TestCli:
    @patch("lightman_ai.cli.load_dotenv")
    @patch("lightman_ai.cli.lightman")
    @patch("lightman_ai.cli.FileConfig.get_config_from_file")
    @patch("lightman_ai.cli.PromptConfig.get_config_from_file")
    @freeze_time("2025-07-29 19:00:00")
    def test_arguments(self, m_prompt: Mock, m_config: Mock, m_lightman: Mock, m_load_dotenv: Mock) -> None:
        runner = CliRunner()
        m_prompt.return_value = PromptConfig({"eval": "eval prompt"})
        m_config.return_value = FileConfig()
        with patch_config_file():
            result = runner.invoke(
                cli.run,
                [
                    "--agent",
                    "gemini",
                    "--prompt",
                    "eval",
                    "--prompt-file",
                    "prompt file",
                    "--score",
                    "1",
                    "--config-file",
                    "config-path",
                    "--config",
                    "my-config",
                    "--today",
                ],
            )

        assert result.exit_code == 0
        assert m_lightman.call_count == 1
        assert m_lightman.call_args == call(
            agent="gemini",
            prompt="eval prompt",
            score_threshold=1,
            dry_run=False,
            service_desk_project_key=None,
            service_desk_request_id_type=None,
            model=None,
            start_date=datetime(2025, 7, 29, 0, 0, tzinfo=ZoneInfo(key="UTC")),
        )
        assert m_config.call_count == 1
        assert m_config.call_args == call(config_section="my-config", path="config-path")
        assert m_prompt.call_args == call(path="prompt file")
        assert m_load_dotenv.call_args == call(".env")

    @pytest.mark.parametrize(
        ("field1", "field2", "field3"),
        [
            ("--today", "--yesterday", ""),
            ("--today", "--start-date", "2025-07-29"),
            ("--yesterday", "--start-date", "2025-07-29"),
        ],
    )
    @patch("lightman_ai.cli.load_dotenv")
    @patch("lightman_ai.cli.lightman")
    def test_today_yesterday_start_date_mutually_exlusive(
        self,
        m_lightman: Mock,
        m_dotenv: Mock,
        field1: str,
        field2: str,
        field3: str,
    ) -> None:
        runner = CliRunner()

        args = [field1, field2]
        if field3:
            args.append(field3)
        with patch_config_file():
            result = runner.invoke(
                cli.run,
                args,
            )

        assert result.exit_code == 2
        assert "--today, --yesterday and --start-date are mutually exclusive. Set one at a time." in result.output
        assert m_lightman.call_count == 0

    @patch("lightman_ai.cli.load_dotenv")
    @patch("lightman_ai.cli.lightman")
    @patch("lightman_ai.cli.FileConfig.get_config_from_file")
    @patch("lightman_ai.cli.PromptConfig.get_config_from_file")
    def test_custom_env_file(self, m_prompt: Mock, m_config: Mock, m_lightman: Mock, m_load_dotenv: Mock) -> None:
        runner = CliRunner()
        m_prompt.return_value = PromptConfig({"eval": "eval prompt"})
        m_config.return_value = FileConfig()
        with patch_config_file():
            result = runner.invoke(
                cli.run,
                [
                    "--agent",
                    "gemini",
                    "--prompt",
                    "eval",
                    "--score",
                    "1",
                    "--env-file",
                    "custom.env",
                ],
            )

        assert result.exit_code == 0
        assert m_load_dotenv.call_args == call("custom.env")

    @patch("lightman_ai.cli.load_dotenv")
    @patch("lightman_ai.cli.lightman")
    @patch("lightman_ai.cli.FileConfig.get_config_from_file")
    @patch("lightman_ai.cli.PromptConfig.get_config_from_file")
    def test_model_is_set_from_the_cli_when_set(
        self, m_prompt: Mock, m_config: Mock, m_lightman: Mock, m_load_dotenv: Mock
    ) -> None:
        runner = CliRunner()
        m_prompt.return_value = PromptConfig({"eval": "eval prompt"})
        m_config.return_value = FileConfig(model="not picked up")
        with patch_config_file():
            result = runner.invoke(
                cli.run,
                [
                    "--agent",
                    "gemini",
                    "--prompt",
                    "eval",
                    "--score",
                    "1",
                    "--env-file",
                    "custom.env",
                    "--model",
                    "picked up",
                ],
            )

        assert result.exit_code == 0
        assert m_lightman.call_count == 1
        assert m_lightman.call_args == call(
            agent="gemini",
            prompt="eval prompt",
            score_threshold=1,
            dry_run=False,
            service_desk_project_key=ANY,
            service_desk_request_id_type=ANY,
            model="picked up",
            start_date=None,
        )

    @patch("lightman_ai.cli.load_dotenv")
    def test_invalid_prompt(self, m_load_dotenv: Mock) -> None:
        runner = CliRunner()
        with (
            patch("lightman_ai.cli.lightman") as m_lightman,
            patch_config_file(content="") as m_config,
        ):
            result = runner.invoke(
                cli.run,
                [
                    "--agent",
                    "gemini",
                    "--prompt",
                    "eval",
                    "--score",
                    "1",
                ],
            )

        assert result.exit_code == 2
        assert "Invalid value: prompt `eval` not found in config file" in result.output
        assert m_lightman.call_count == 0
        assert m_config.call_count == 2

    @patch("lightman_ai.cli.load_dotenv")
    def test_prompt_file_not_found(self, m_load_dotenv: Mock) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli.run,
            [
                "--prompt-file",
                "non-existing-file.toml",
            ],
        )
        assert result.exit_code == 2
        assert "Invalid value: `non-existing-file.toml` not found!" in result.output

    @patch("lightman_ai.cli.load_dotenv")
    def test_service_desk_variables_missing_from_toml(self, m_load_dotenv: Mock) -> None:
        """Test CLI with TOML file that doesn't include service desk configuration."""
        runner = CliRunner()
        # TOML content without any service desk fields
        config_content = """
        [default]
        agent = 'openai'
        score_threshold = 8
        prompt = 'classify'
        [prompts]
        classify = 'Analyze security threats'
        """
        with (
            patch("lightman_ai.cli.lightman") as m_lightman,
            patch_config_file(content=config_content) as m_config,
        ):
            result = runner.invoke(
                cli.run,
                [
                    "--dry-run",
                ],
            )
        assert result.exit_code == 0
        assert m_lightman.call_count == 1
        assert m_lightman.call_args == call(
            agent="openai",
            prompt="Analyze security threats",
            score_threshold=8,
            dry_run=True,
            service_desk_project_key=None,
            service_desk_request_id_type=None,
            model=None,
            start_date=None,
        )
        assert m_config.call_count == 2

    @patch("lightman_ai.cli.metadata.version")
    def test_get_version_calls_metadata(self, mock_version: Mock) -> None:
        mock_version.return_value = "1.2.3"

        assert cli.get_version() == "1.2.3"
        mock_version.assert_called_once_with("lightman-ai")
