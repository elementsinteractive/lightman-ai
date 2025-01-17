import asyncio
import os

import click
from dotenv import load_dotenv
from hackerman_ai.constants import API_KEY_ENV_KEY
from hackerman_ai.main import hackerman


@click.group()
def entry_point() -> None:
    pass


@entry_point.command()
@click.option("--api-key", type=click.STRING)
def run(api_key: str | None) -> int:
    """
    Entrypoint of the application.

    Holds no logic. Just calls the methods and return an exit code.
    """
    load_dotenv()

    if not api_key:
        api_key = str(os.getenv(API_KEY_ENV_KEY))

    return int(asyncio.run(hackerman(api_key)))
