from unittest.mock import Mock, call, patch

from click.testing import CliRunner
from hackerman_ai import cli
from hackerman_ai.core.config import PromptConfig
from tests.conftest import patch_config_file


class TestCli:
    @patch("hackerman_ai.cli.hackerman")
    @patch("hackerman_ai.cli.FileConfig.get_config_from_file")
    @patch("hackerman_ai.cli.PromptConfig.get_config_from_file")
    def test_arguments(self, m_prompt: Mock, m_config: Mock, m_hackerman: Mock) -> None:
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
                    "--iterations",
                    "2",
                    "--config-file",
                    "config-path",
                    "--config",
                    "my-config",
                ],
            )

        assert result.exit_code == 0
        assert m_hackerman.call_count == 1
        assert m_hackerman.call_args == call(
            model="gemini-2.5-pro-preview-05-06",
            prompt="eval prompt",
            score_threshold=1,
            iterations=2,
        )
        assert m_config.call_count == 1
        assert m_config.call_args == call(config_section="my-config", path="config-path")
        assert m_prompt.call_args == call(path="prompt file")

    def test_invalid_config(self) -> None:
        runner = CliRunner()
        config_content = """
        [prompts]
        eval = 'eval prompt'"""
        with patch("hackerman_ai.cli.hackerman") as m_hackerman, patch_config_file(content=config_content) as m_config:
            result = runner.invoke(
                cli.run,
                ["--prompt", "eval"],
            )
        assert result.exit_code == 2
        assert (
            "Invalid value: Invalid configuration provided: "
            "[`iterations`: Input should be a valid integer,"
            "`model`: Input should be a valid string,"
            "`score_threshold`: Input should be a valid integer]" in result.output
        )
        assert m_hackerman.call_count == 0
        assert m_config.call_count == 2

    def test_invalid_prompt(self) -> None:
        runner = CliRunner()
        with patch("hackerman_ai.cli.hackerman") as m_hackerman, patch_config_file(content="") as m_config:
            result = runner.invoke(
                cli.run,
                [
                    "--model",
                    "gemini-2.5-pro-preview-05-06",
                    "--prompt",
                    "eval",
                    "--score",
                    "1",
                    "--iterations",
                    "2",
                ],
            )
        assert result.exit_code == 2
        assert "Invalid value: prompt `eval` not found in config file" in result.output
        assert m_hackerman.call_count == 0
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
