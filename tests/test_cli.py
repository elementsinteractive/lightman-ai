from unittest.mock import Mock, call, patch

from click.testing import CliRunner
from lightman_ai import cli
from lightman_ai.core.config import PromptConfig
from tests.conftest import patch_config_file


class TestCli:
    @patch("lightman_ai.cli.lightman")
    @patch("lightman_ai.cli.FileConfig.get_config_from_file")
    @patch("lightman_ai.cli.PromptConfig.get_config_from_file")
    def test_arguments(self, m_prompt: Mock, m_config: Mock, m_lightman: Mock) -> None:
        runner = CliRunner()
        m_prompt.return_value = PromptConfig({"eval": "eval prompt"})
        with patch_config_file():
            result = runner.invoke(
                cli.run,
                [
                    "--model",
                    "gemini-2.5-pro-preview-05-06",
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
                ],
            )

        assert result.exit_code == 0
        assert m_lightman.call_count == 1
        from unittest.mock import ANY

        assert m_lightman.call_args == call(
            model="gemini-2.5-pro-preview-05-06",
            prompt="eval prompt",
            score_threshold=1,
            dry_run=False,
            project_key=ANY,
            request_id_type=ANY,
        )
        assert m_config.call_count == 1
        assert m_config.call_args == call(config_section="my-config", path="config-path")
        assert m_prompt.call_args == call(path="prompt file")

    def test_invalid_config(self) -> None:
        runner = CliRunner()
        config_content = """
        [prompts]
        eval = 'eval prompt'"""
        with patch("lightman_ai.cli.lightman") as m_lightman, patch_config_file(content=config_content) as m_config:
            result = runner.invoke(
                cli.run,
                ["--prompt", "eval"],
            )
        assert result.exit_code == 2
        assert (
            "Invalid value: Invalid configuration provided: "
            "[`model`: Input should be a valid string,"
            "`score_threshold`: Input should be a valid integer]" in result.output
        )
        assert m_lightman.call_count == 0
        assert m_config.call_count == 2

    def test_invalid_prompt(self) -> None:
        runner = CliRunner()
        with patch("lightman_ai.cli.lightman") as m_lightman, patch_config_file(content="") as m_config:
            result = runner.invoke(
                cli.run,
                [
                    "--model",
                    "gemini-2.5-pro-preview-05-06",
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

    def test_prompt_file_not_found(self) -> None:
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
