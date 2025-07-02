import logging

import click
from dotenv import load_dotenv
from hackerman_ai.ai.utils import MODEL_CHOICES
from hackerman_ai.constants import DEFAULT_CONFIG_FILE, DEFAULT_CONFIG_SECTION
from hackerman_ai.core.config import FileConfig, FinalConfig, PromptConfig
from hackerman_ai.core.exceptions import ConfigNotFoundError, InvalidConfigError, PromptNotFoundError
from hackerman_ai.main import hackerman

logger = logging.getLogger("hackerman")


@click.group()
def entry_point() -> None:
    pass


@entry_point.command()
@click.option("--model", type=click.Choice(MODEL_CHOICES), help=("Which model to use"))
@click.option(
    "--prompt-file",
    type=str,
    default=DEFAULT_CONFIG_FILE,
    help=(f"Location of the config file containing the prompts. Defaults to `{DEFAULT_CONFIG_FILE}`."),
)
@click.option("--prompt", type=str, help=("Which prompt to use"))
@click.option("--iterations", type=int, help=("The number of iterations that the agent will run"), default=None)
@click.option(
    "--score",
    type=int,
    help=("The minimum score relevance that an article needs to have to be considered relevant"),
    default=None,
)
@click.option(
    "--config-file",
    type=str,
    default=DEFAULT_CONFIG_FILE,
    help=(f"The config file path. Defaults to `{DEFAULT_CONFIG_FILE}`."),
)
@click.option(
    "--config",
    type=str,
    default=DEFAULT_CONFIG_SECTION,
    help=(f"The config settings to use. Defaults to `{DEFAULT_CONFIG_SECTION}`."),
)
@click.option(
    "--dry-run",
    is_flag=True,
    help=(
        "When set, runs the script without publishing the results to the integrated services, just shows them in stdout."
    ),
)
def run(
    model: str,
    prompt: str,
    prompt_file: str,
    iterations: int | None,
    score: int | None,
    config_file: str,
    config: str,
    dry_run: bool,
) -> int:
    """
    Entrypoint of the application.

    Holds no logic. It calls the main method and returns 0 when succesful .
    """
    load_dotenv()
    try:
        prompt_config = PromptConfig.get_config_from_file(path=prompt_file)
        config_from_file = FileConfig.get_config_from_file(config_section=config, path=config_file)
        final_config = FinalConfig.init_from_dict(
            data={
                "model": model or config_from_file.model,
                "prompt": prompt or config_from_file.prompt,
                "score_threshold": score or config_from_file.score_threshold,
                "iterations": iterations or config_from_file.iterations,
            }
        )

        prompt_text = prompt_config.get_prompt(final_config.prompt)
    except (InvalidConfigError, PromptNotFoundError, ConfigNotFoundError) as err:
        raise click.BadParameter(err.args[0]) from None

    relevant_articles = hackerman(
        iterations=final_config.iterations,
        model=final_config.model,
        prompt=prompt_text,
        score_threshold=final_config.score_threshold,
        dry_run=dry_run,
        project_key=config_from_file.service_desk_project_key,
        request_id_type=config_from_file.service_desk_request_id_type,
    )
    relevant_articles_titles = [article.title for article in relevant_articles]
    logger.warning("Found these articles: %s", "\n".join(relevant_articles_titles))
    return 0
