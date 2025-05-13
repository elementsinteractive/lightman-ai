import asyncio

import click
from hackerman_ai.ai.utils import MODEL_CHOICES
from hackerman_ai.main import hackerman


@click.group()
def entry_point() -> None:
    pass


@entry_point.command()
@click.option("--model", type=click.Choice(MODEL_CHOICES), help=("Which model to use."), default="openai")
def run(model: str) -> int:
    """
    Entrypoint of the application.

    Holds no logic. Just calls the methods and return an exit code.
    """
    return int(asyncio.run(hackerman(model)))
