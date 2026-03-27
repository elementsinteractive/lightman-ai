import asyncio

import click
from dotenv import load_dotenv
from lightman_ai.ai.utils import AGENT_CHOICES
from lightman_ai.constants import DEFAULT_AGENT, DEFAULT_CONFIG_FILE, DEFAULT_ENV_FILE, DEFAULT_SCORE
from lightman_ai.core.config import PromptConfig

from eval.classified_articles import NON_RELEVANT_ARTICLES, RELEVANT_ARTICLES
from eval.constants import DEFAULT_EVAL_CONFIG_SECTION
from eval.evaluator import evaluate
from eval.utils import PARALLEL_WORKERS, EvalConfig, EvalFileConfig


@click.command()
@click.option("--tag", type=str, help=("Tag that identifies the run"), default=None)
@click.option(
    "--agent",
    type=click.Choice(AGENT_CHOICES),
    help=("The agent to use to analyze articles"),
)
@click.option("--score", type=int, help=("Minimum score to consider an article to be relevant"))
@click.option(
    "--samples",
    type=int,
    help=(
        "Number of times the evaluation will run with all its iterations. It will calculate averages for the results. "
    ),
)
@click.option("--prompt", type=str, help=("Which prompt to use."))
@click.option("--model", type=str, default=None, help=("Which model to use."))
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
@click.option(
    "--env-file",
    type=str,
    default=DEFAULT_ENV_FILE,
    help=(f"Path to the environment file. Defaults to `{DEFAULT_ENV_FILE}`."),
)
def run(
    agent: str,
    score: int,
    samples: int,
    prompt: str,
    config: str,
    config_file: str,
    prompt_file: str,
    env_file: str,
    tag: str | None = None,
    model: str | None = None,
) -> None:
    load_dotenv(env_file)

    config_from_file = EvalFileConfig.get_config_from_file(config_section=config, path=config_file)
    configured_prompts = PromptConfig.get_config_from_file(path=prompt_file)
    eval_config = EvalConfig.init_from_dict(
        {
            "agent": agent or config_from_file.agent or DEFAULT_AGENT,
            "prompt": prompt or config_from_file.prompt,
            "score_threshold": score or config_from_file.score_threshold or DEFAULT_SCORE,
            "samples": samples or config_from_file.samples,
            "model": model or config_from_file.model,
            "sources": [],
        }
    )

    asyncio.run(
        evaluate(
            score_threshold=eval_config.score_threshold,
            relevant_articles=RELEVANT_ARTICLES,
            non_relevant_articles=NON_RELEVANT_ARTICLES,
            samples=eval_config.samples,
            tag=tag,
            agent=eval_config.agent,
            prompt=configured_prompts.get_prompt(eval_config.prompt),
            model=eval_config.model,
            parallel_workers=PARALLEL_WORKERS,
            sources=eval_config.sources,
        )
    )


if __name__ == "__main__":
    run()
