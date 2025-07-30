import tempfile

from lightman_ai.core.settings import Settings
from tests.conftest import patch_env_variables


class TestSettings:
    def test_init_settings_no_env_file_provided(self) -> None:
        """Default settings are loaded."""
        settings = Settings.try_load_from_file()
        assert settings.TIME_ZONE == "UTC"
        assert settings.SCORE == 8
        assert settings.AGENT == "openai"

    def test_init_settings_loads_variables_from_environment(self) -> None:
        with patch_env_variables({"TIME_ZONE": "my time zone"}):
            settings = Settings.try_load_from_file()
        assert settings.TIME_ZONE == "my time zone"

    def test_init_settings_environment_vars_take_precedence_over_settings_env_file_(self) -> None:
        content = "TIME_ZONE=Europe/Amsterdam"
        with patch_env_variables({"TIME_ZONE": "my time zone"}), tempfile.NamedTemporaryFile("w+") as tmp:
            tmp.write(content)
            tmp.flush()
            settings = Settings.try_load_from_file(tmp.name)
        assert settings.TIME_ZONE == "my time zone"

    def test_init_settings_wrong_env_file_provided(self) -> None:
        """Default settings are loaded, execution continues normally."""
        settings = Settings.try_load_from_file("fake.env")
        assert settings.TIME_ZONE == "UTC"
        assert settings.SCORE == 8
        assert settings.AGENT == "openai"

    def test_init_settings_env_file_provided(self) -> None:
        """.env file contents are loaded."""
        settings = Settings.try_load_from_file()
        # Check defaults are in place
        assert settings.TIME_ZONE == "UTC"
        assert settings.SCORE == 8
        assert settings.AGENT == "openai"
        content = """
                TIME_ZONE=Europe/Amsterdam
                AGENT=my-agent
                SCORE=2"""
        with tempfile.NamedTemporaryFile("w+") as tmp:
            tmp.write(content)
            tmp.flush()
            settings = Settings.try_load_from_file(tmp.name)
        assert settings.TIME_ZONE == "Europe/Amsterdam"
        assert settings.SCORE == 2
        assert settings.AGENT == "my-agent"
