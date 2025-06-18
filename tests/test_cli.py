from unittest.mock import Mock, call, patch

from click.testing import CliRunner
from hackerman_ai import cli
from hackerman_ai.ai.prompts import get_prompt
from tests.conftest import patch_config_file


class TestCli:
    @patch("hackerman_ai.cli.hackerman")
    @patch("hackerman_ai.cli.FileConfig.get_config_from_file")
    def test_arguments(self, m_config: Mock, m_hackerman: Mock) -> None:
        runner = CliRunner()
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
                "--config-path",
                "config-path",
                "--config",
                "my-config",
            ],
        )

        assert result.exit_code == 0
        assert m_hackerman.call_count == 1
        assert m_hackerman.call_args == call(
            model="gemini-2.5-pro-preview-05-06",
            prompt=get_prompt("eval"),
            score_threshold=1,
            iterations=2,
        )
        assert m_config.call_count == 1
        assert m_config.call_args == call(config_section="my-config", path="config-path")

    def test_invalid_config(self) -> None:
        runner = CliRunner()
        with patch("hackerman_ai.cli.hackerman") as m_hackerman, patch_config_file(content="") as m_config:
            result = runner.invoke(
                cli.run,
                [],
            )
        assert result.exit_code == 2
        assert (
            "Invalid configuration provided: [`iterations`: Input should be a valid integer,`prompt`: "
            "Input should be a valid string,`model`: Input should be a valid string,`score_threshold`:"
            " Input should be a valid integer]" in result.output
        )
        assert m_hackerman.call_count == 0
        assert m_config.call_count == 1
