import logging

import click
from hackerman_ai.ai.prompts import PROMPTS_CHOICES, get_prompt
from hackerman_ai.ai.utils import MODEL_CHOICES
from hackerman_ai.core.settings import settings
from hackerman_ai.main import hackerman

logger = logging.getLogger("hackerman")


@click.group()
def entry_point() -> None:
    pass


@entry_point.command()
@click.option("--model", type=click.Choice(MODEL_CHOICES), help=("Which model to use."), default="gpt-4.1")
@click.option("--prompt", type=click.Choice(PROMPTS_CHOICES), help=("Which prompt to use."), default="eval")
@click.option("--iterations", type=int, help=("The number of iterations that the agent will run"), default=None)
@click.option(
    "--score",
    type=int,
    help=("The minimum score relevance that an article needs to have to be considered relevant"),
    default=None,
)
def run(model: str, prompt: str, iterations: int | None, score: int | None) -> int:
    """
    Entrypoint of the application.

    Holds no logic. It calls the main method and returns 0 when succesful .
    """

    def validate_positive_int_field(field: str, value: int | None) -> None:
        if value is not None and not value > 0:
            raise click.BadParameter(f"`{field}` must be > 0.")

    validate_positive_int_field("iterations", iterations)
    validate_positive_int_field("score", score)

    relevant_articles = hackerman(
        model=model,
        prompt=get_prompt(prompt),
        score_threshold=score or settings.RELEVANCE_SCORE_THRESHOLD,
        iterations=iterations or settings.PROMPT_ITERATIONS,
    )
    relevant_articles_titles = [article.title for article in relevant_articles]
    logger.warning("Found these articles: %s", "\n".join(relevant_articles_titles))
    return 0
