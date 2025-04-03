import os
import pathlib
from typing import Any

import pytest
from dotenv import load_dotenv

RECORD_MODE = False


def pytest_configure() -> None:
    os.environ["OPENAI_API_KEY"] = "dummy"
    load_dotenv()  # TODO improve this


@pytest.fixture(scope="module")
def vcr_cassette_dir(request: Any) -> Any:
    return str(pathlib.Path(__file__).parent / "cassettes")


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, Any]:
    return {
        "match_on": ("method", "path", "query", "body"),
        "record_mode": "new_episodes" if RECORD_MODE else "none",
        "filter_headers": [
            ("authorization", "CENSORED"),
        ],
        "decode_compressed_response": True,
    }
