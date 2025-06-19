import click
from dotenv import load_dotenv
from hackerman_ai.ai.prompts import PROMPTS_CHOICES
from hackerman_ai.ai.utils import MODEL_CHOICES

from eval.classified_articles import NON_RELEVANT_ARTICLES, RELEVANT_ARTICLES
from eval.constants import DEFAULT_MODEL
from eval.evaluator import eval
from eval.utils import EvalConfig, EvalFileConfig


@click.command()
@click.option("--tag", type=str, help=("Tag that identifies the run"), default=None)
@click.option(
    "--model", type=click.Choice(MODEL_CHOICES), help=("The model to use to analyze articles"), default=DEFAULT_MODEL
)
@click.option("--iterations", type=int, help=("Number of times that the prompt will run"), default=1)
@click.option("--score", type=int, help=("Minimum score to consider an article to be relevant"))
@click.option(
    "--samples",
    type=int,
    help=(
        "Number of times the evaluation will run with all its iterations. It will calculate averages for the results. "
    ),
)
@click.option("--prompt", type=click.Choice(PROMPTS_CHOICES), help=("Which prompt to use."))
def run(model: str, iterations: int, score: int, samples: int, prompt: str, tag: str | None = None) -> None:
    config_from_file = EvalFileConfig.get_config_from_file(config_section="eval")
    config = EvalConfig.init_from_dict(
        {
            "model": model or config_from_file.model,
            "prompt": prompt or config_from_file.prompt,
            "score_threshold": score or config_from_file.score_threshold,
            "iterations": iterations or config_from_file.iterations,
            "samples": samples or config_from_file.samples,
        }
    )
    eval(
        score_threshold=config.score_threshold,
        iterations=config.iterations,
        relevant_articles=RELEVANT_ARTICLES,
        non_relevant_articles=NON_RELEVANT_ARTICLES,
        samples=config.samples,
        tag=tag,
        model=config.model,
        prompt=config.prompt,
    )


if __name__ == "__main__":
    load_dotenv()
    run()
