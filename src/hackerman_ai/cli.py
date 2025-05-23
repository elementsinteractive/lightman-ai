import click
from hackerman_ai.ai.utils import MODEL_CHOICES
from hackerman_ai.main import hackerman


@click.group()
def entry_point() -> None:
    pass


@entry_point.command()
@click.option("--model", type=click.Choice(MODEL_CHOICES), help=("Which model to use."), default="gpt-4.1")
@click.option("--iterations", type=int, help=("The number of iterations that the agent will run"), default=None)
def run(model: str, iterations: int | None) -> int:
    """
    Entrypoint of the application.

    Holds no logic. Just calls the methods and return an exit code.
    """
    hackerman(model, iterations)

    return 0
