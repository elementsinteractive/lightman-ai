import asyncio

import click
from hackerman_ai.main import hackerman


@click.group()
def entry_point() -> None:
    pass


@entry_point.command()
@click.option("--api-key", type=click.STRING)
def run(api_key: str) -> int:
    """
    Entrypoint of the application.

    Holds no logic. Just calls the methods and return an exit code.
    """
    return int(asyncio.run(hackerman(api_key)))
