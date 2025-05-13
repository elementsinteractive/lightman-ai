from unittest.mock import Mock, call, patch

from click.testing import CliRunner
from hackerman_ai import cli


class TestCli:
    @patch("hackerman_ai.cli.hackerman")
    def test_arguments(self, m_hackerman: Mock) -> None:
        runner = CliRunner()
        runner.invoke(cli.run, ["--model", "openai"])
        assert m_hackerman.call_count == 1
        assert m_hackerman.call_args == call("openai")

    @patch("hackerman_ai.cli.hackerman")
    def test_arguments_defaults(self, m_hackerman: Mock) -> None:
        runner = CliRunner()
        runner.invoke(cli.run)
        assert m_hackerman.call_count == 1
        assert m_hackerman.call_args == call("openai")
