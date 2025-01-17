import os
import pathlib
from typing import Any

import pytest
from dotenv import load_dotenv
from hackerman_ai.constants import API_KEY_ENV_KEY

RECORD_MODE = True


def pytest_configure() -> None:
    load_dotenv()


@pytest.fixture(scope="session")
def api_key() -> str:
    return str(os.getenv(API_KEY_ENV_KEY))


@pytest.fixture(scope="module")
def vcr_cassette_dir(request: Any) -> Any:
    return str(pathlib.Path(__file__).parent / "cassettes")


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, Any]:
    return {
        "match_on": ("method", "path", "query", "body"),
        "record_mode": "new_episodes" if RECORD_MODE else "none",
        "filter_headers": [
            ("x-goog-api-key", "CENSORED"),
        ],
        "decode_compressed_response": True,
    }
