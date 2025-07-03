import click
from dotenv import load_dotenv
from lightman_ai.ai.utils import MODEL_CHOICES
from lightman_ai.constants import DEFAULT_CONFIG_FILE
from lightman_ai.core.config import PromptConfig

from eval.classified_articles import NON_RELEVANT_ARTICLES, RELEVANT_ARTICLES
from eval.constants import DEFAULT_EVAL_CONFIG_SECTION, DEFAULT_MODEL
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
@click.option("--prompt", type=str, help=("Which prompt to use."))
@click.option(
    "--prompt-file",
    type=str,
    default=DEFAULT_CONFIG_FILE,
    help=(f"Location of the config file containing the prompts. Defaults to `{DEFAULT_CONFIG_FILE}`."),
)
@click.option(
    "--config-file",
    type=str,
    default=DEFAULT_CONFIG_FILE,
    help=(f"The config file path.  Defaults to `{DEFAULT_CONFIG_FILE}`."),
)
@click.option("--config", type=str, default=DEFAULT_EVAL_CONFIG_SECTION, help=("The config settings to use"))
def run(
    model: str,
    iterations: int,
    score: int,
    samples: int,
    prompt: str,
    config: str,
    config_file: str,
    prompt_file: str,
    tag: str | None = None,
) -> None:
    config_from_file = EvalFileConfig.get_config_from_file(config_section=config, path=config_file)
    configured_prompts = PromptConfig.get_config_from_file(path=prompt_file)
    eval_config = EvalConfig.init_from_dict(
        {
            "model": model or config_from_file.model,
            "prompt": prompt or config_from_file.prompt,
            "score_threshold": score or config_from_file.score_threshold,
            "iterations": iterations or config_from_file.iterations,
            "samples": samples or config_from_file.samples,
        }
    )

    eval(
        score_threshold=eval_config.score_threshold,
        iterations=eval_config.iterations,
        relevant_articles=RELEVANT_ARTICLES,
        non_relevant_articles=NON_RELEVANT_ARTICLES,
        samples=eval_config.samples,
        tag=tag,
        model=eval_config.model,
        prompt=configured_prompts.get_prompt(eval_config.prompt),
    )


if __name__ == "__main__":
    load_dotenv()
    run()
