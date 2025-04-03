import asyncio

import click
from dotenv import load_dotenv
from hackerman_ai.main import hackerman


@click.group()
def entry_point() -> None:
    pass


@entry_point.command()
def run() -> int:
    """
    Entrypoint of the application.

    Holds no logic. Just calls the methods and return an exit code.
    """
    load_dotenv()

    return int(asyncio.run(hackerman()))
