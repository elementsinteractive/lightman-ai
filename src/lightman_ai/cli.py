import logging
from datetime import date
from importlib import metadata

import click
from dotenv import load_dotenv
from lightman_ai.ai.utils import AGENT_CHOICES
from lightman_ai.constants import DEFAULT_CONFIG_FILE, DEFAULT_CONFIG_SECTION, DEFAULT_ENV_FILE
from lightman_ai.core.config import FileConfig, FinalConfig, PromptConfig
from lightman_ai.core.exceptions import ConfigNotFoundError, InvalidConfigError, PromptNotFoundError
from lightman_ai.core.sentry import configure_sentry
from lightman_ai.core.settings import Settings
from lightman_ai.exceptions import MultipleDateSourcesError
from lightman_ai.main import lightman
from lightman_ai.utils import get_start_date

logger = logging.getLogger("lightman")


def get_version() -> str:
    """Read version from VERSION file."""
    return metadata.version("lightman-ai")


@click.group()
@click.version_option(version=get_version(), prog_name="lightman-ai")
def entry_point() -> None:
    pass


@entry_point.command()
@click.option("--agent", type=click.Choice(AGENT_CHOICES), help=("Which agent to use"))
@click.option(
    "--prompt-file",
    type=str,
    default=DEFAULT_CONFIG_FILE,
    help=(f"Location of the config file containing the prompts. Defaults to `{DEFAULT_CONFIG_FILE}`."),
)
@click.option("--prompt", type=str, help=("Which prompt to use"))
@click.option("--model", type=str, default=None, help=("Which model to use. Must be set in conjunction with --agent."))
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
    "--env-file",
    type=str,
    default=None,
    help=(f"Path to the environment file. Defaults to `{DEFAULT_ENV_FILE}`."),
)
@click.option(
    "--dry-run",
    is_flag=True,
    help=(
        "When set, runs the script without publishing the results to the integrated services, just shows them in stdout."
    ),
)
@click.option("--start-date", type=click.DateTime(formats=["%Y-%m-%d"]), help="Start date to retrieve articles")
@click.option("--today", is_flag=True, help="Retrieve articles from today.")
@click.option("--yesterday", is_flag=True, help="Retrieve articles from yesterday.")
def run(
    agent: str,
    prompt: str,
    prompt_file: str,
    model: str | None,
    score: int | None,
    config_file: str,
    config: str,
    env_file: str | None,
    dry_run: bool,
    start_date: date | None,
    today: bool,
    yesterday: bool,
) -> int:
    """
    Entrypoint of the application.

    Holds no logic. It loads the configuration, calls the main method and returns 0 when succesful .
    """
    load_dotenv(env_file or DEFAULT_ENV_FILE)
    configure_sentry()

    settings = Settings.try_load_from_file(env_file)
    try:
        start_datetime = get_start_date(settings, yesterday, today, start_date)
    except MultipleDateSourcesError as e:
        raise click.UsageError(e.args[0]) from e

    try:
        prompt_config = PromptConfig.get_config_from_file(path=prompt_file)
        config_from_file = FileConfig.get_config_from_file(config_section=config, path=config_file)
        final_config = FinalConfig.init_from_dict(
            data={
                "agent": agent or config_from_file.agent or settings.AGENT,
                "prompt": prompt or config_from_file.prompt,
                "score_threshold": score or config_from_file.score_threshold or settings.SCORE,
                "model": model or config_from_file.model,
            }
        )
        prompt_text = prompt_config.get_prompt(final_config.prompt)
    except (InvalidConfigError, PromptNotFoundError, ConfigNotFoundError) as err:
        raise click.BadParameter(err.args[0]) from None

    relevant_articles = lightman(
        agent=final_config.agent,
        prompt=prompt_text,
        score_threshold=final_config.score_threshold,
        dry_run=dry_run,
        service_desk_project_key=config_from_file.service_desk_project_key,
        service_desk_request_id_type=config_from_file.service_desk_request_id_type,
        model=final_config.model,
        start_date=start_datetime,
    )
    relevant_articles_metadata = [f"{article.title} ({article.link})" for article in relevant_articles]
    logger.warning("Found these articles: \n- %s", "\n- ".join(relevant_articles_metadata))
    return 0
