import click
from hackerman_ai.ai.prompts import PROMPTS_CHOICES, get_prompt
from hackerman_ai.ai.utils import MODEL_CHOICES
from hackerman_ai.main import hackerman


@click.group()
def entry_point() -> None:
    pass


@entry_point.command()
@click.option("--model", type=click.Choice(MODEL_CHOICES), help=("Which model to use."), default="gpt-4.1")
@click.option("--prompt", type=click.Choice(PROMPTS_CHOICES), help=("Which prompt to use."), default="eval")
@click.option("--iterations", type=int, help=("The number of iterations that the agent will run"), default=None)
def run(model: str, prompt: str, iterations: int | None) -> int:
    """
    Entrypoint of the application.

    Holds no logic. It calls the methods and returns an exit code.
    """
    hackerman(model, get_prompt(prompt), iterations)

    return 0
