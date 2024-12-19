from unittest.mock import Mock, call, patch

from click.testing import CliRunner
from hackerman_ai import cli


class TestCli:
    @patch("hackerman_ai.cli.hackerman")
    def test_arguments(self, hackerman: Mock) -> None:
        runner = CliRunner()
        runner.invoke(
            cli.run,
            ["--api-key", "my-api-key"],
        )
        assert hackerman.call_count == 1
        assert hackerman.call_args_list == [call("my-api-key")]
