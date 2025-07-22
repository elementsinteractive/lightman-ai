from unittest.mock import Mock, call, patch

from click.testing import CliRunner
from lightman_ai.core.config import FileConfig, PromptConfig
from tests.conftest import patch_config_file

from eval import cli


class TestEvalCli:
    @patch("eval.cli.eval")
    @patch("eval.cli.load_dotenv")
    @patch("eval.cli.EvalFileConfig.get_config_from_file")
    @patch("eval.cli.PromptConfig.get_config_from_file")
    def test_env_file_parameter(self, m_prompt: Mock, m_config: Mock, m_load_dotenv: Mock, m_eval: Mock) -> None:
        runner = CliRunner()
        m_prompt.return_value = PromptConfig({"eval": "eval prompt"})
        m_config.return_value = FileConfig()
        with patch_config_file():
            result = runner.invoke(
                cli.run,
                [
                    "--agent",
                    "openai",
                    "--score",
                    "8",
                    "--samples",
                    "3",
                    "--prompt",
                    "eval",
                    "--env-file",
                    "custom.env",
                ],
            )

        assert result.exit_code == 0
        assert m_load_dotenv.call_args == call("custom.env")

    @patch("eval.cli.eval")
    @patch("eval.cli.load_dotenv")
    @patch("eval.cli.EvalFileConfig.get_config_from_file")
    @patch("eval.cli.PromptConfig.get_config_from_file")
    def test_default_env_file(self, m_prompt: Mock, m_config: Mock, m_load_dotenv: Mock, m_eval: Mock) -> None:
        runner = CliRunner()
        m_prompt.return_value = PromptConfig({"eval": "eval prompt"})
        m_config.return_value = FileConfig()
        with patch_config_file():
            result = runner.invoke(
                cli.run,
                [
                    "--agent",
                    "openai",
                    "--score",
                    "8",
                    "--samples",
                    "3",
                    "--prompt",
                    "eval",
                ],
            )

        assert result.exit_code == 0
        assert m_load_dotenv.call_args == call(".env")  # Default env file
