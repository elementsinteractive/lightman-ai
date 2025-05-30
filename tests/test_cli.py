from unittest.mock import Mock, call, patch

from click.testing import CliRunner
from hackerman_ai import cli
from hackerman_ai.ai.prompts import get_prompt


class TestCli:
    @patch("hackerman_ai.cli.hackerman")
    def test_arguments(self, m_hackerman: Mock) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli.run,
            ["--model", "gemini-2.5-pro-preview-05-06", "--prompt", "eval", "--score", "1", "--iterations", "2"],
        )

        assert result.exit_code == 0
        assert m_hackerman.call_count == 1
        assert m_hackerman.call_args == call(
            model="gemini-2.5-pro-preview-05-06", prompt=get_prompt("eval"), score_threshold=1, iterations=2
        )

    @patch("hackerman_ai.cli.hackerman")
    def test_arguments_defaults(self, m_hackerman: Mock) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli.run,
            ["--score", "1", "--iterations", "2"],
        )

        assert result.exit_code == 0
        assert m_hackerman.call_count == 1
        assert m_hackerman.call_args == call(
            model="gpt-4.1", prompt=get_prompt("eval"), score_threshold=1, iterations=2
        )

    @patch("hackerman_ai.cli.hackerman")
    def test_iterations_must_be_positive(self, m_hackerman: Mock) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli.run,
            ["--iterations", "0", "--score", "1"],
        )
        assert result.exit_code == 2
        assert "Error: Invalid value: `iterations` must be > 0." in result.output
        assert m_hackerman.call_count == 0

    @patch("hackerman_ai.cli.hackerman")
    def test_score_must_be_positive(self, m_hackerman: Mock) -> None:
        runner = CliRunner()
        result = runner.invoke(
            cli.run,
            ["--score", "0", "--iterations", "1"],
        )
        assert result.exit_code == 2
        assert "Error: Invalid value: `score` must be > 0." in result.output
        assert m_hackerman.call_count == 0
