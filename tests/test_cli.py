from unittest.mock import Mock, patch

from click.testing import CliRunner
from hackerman_ai import cli


class TestCli:
    @patch("hackerman_ai.cli.hackerman")
    def test_arguments(self, hackerman: Mock) -> None:
        runner = CliRunner()
        runner.invoke(
            cli.run,
        )
        assert hackerman.call_count == 1
