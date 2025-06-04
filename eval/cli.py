import click
from dotenv import load_dotenv
from hackerman_ai.ai.prompts import PROMPTS_CHOICES
from hackerman_ai.ai.utils import MODEL_CHOICES
from hackerman_ai.core.settings import settings

from eval.classified_articles import NON_RELEVANT_ARTICLES, RELEVANT_ARTICLES
from eval.constants import DEFAULT_MODEL
from eval.evaluator import eval


@click.command()
@click.option("--tag", type=str, help=("Tag that identifies the run"), default=None)
@click.option(
    "--model", type=click.Choice(MODEL_CHOICES), help=("The model to use to analyze articles"), default=DEFAULT_MODEL
)
@click.option("--iterations", type=int, help=("Number of times that the prompt will run"), default=1)
@click.option("--score", type=int, help=("Minimum score to consider an article to be relevant"), default=None)
@click.option(
    "--samples",
    type=int,
    help=(
        "Number of times the evaluation will run with all its iterations. It will calculate averages for the results. "
    ),
    default=1,
)
@click.option("--prompt", type=click.Choice(PROMPTS_CHOICES), help=("Which prompt to use."), default="eval")
def run(model: str, iterations: int, score: int, samples: int, prompt: str, tag: str | None = None) -> None:
    def validate_positive_int(field: str, value: int) -> None:
        if value is not None and value < 1:
            raise click.BadParameter(f"`{field}` must be > 0.")

    validate_positive_int("samples", samples)
    validate_positive_int("score", score)
    validate_positive_int("iterations", iterations)

    eval(
        score_threshold=score or settings.RELEVANCE_SCORE_THRESHOLD,
        iterations=iterations,
        relevant_articles=RELEVANT_ARTICLES,
        non_relevant_articles=NON_RELEVANT_ARTICLES,
        samples=samples,
        tag=tag,
        model=model,
        prompt=prompt,
    )


if __name__ == "__main__":
    load_dotenv()
    run()
