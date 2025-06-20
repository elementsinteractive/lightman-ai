import logging

import click
from hackerman_ai.ai.prompts import PROMPTS_CHOICES, get_prompt
from hackerman_ai.ai.utils import MODEL_CHOICES
from hackerman_ai.constants import DEFAULT_CONFIG_SECTION
from hackerman_ai.core.config import FileConfig, FinalConfig
from hackerman_ai.core.exceptions import ConfigNotFoundError, InvalidConfigError
from hackerman_ai.main import hackerman

logger = logging.getLogger("hackerman")


@click.group()
def entry_point() -> None:
    pass


@entry_point.command()
@click.option("--model", type=click.Choice(MODEL_CHOICES), help=("Which model to use"))
@click.option("--prompt", type=click.Choice(PROMPTS_CHOICES), help=("Which prompt to use"))
@click.option("--iterations", type=int, help=("The number of iterations that the agent will run"), default=None)
@click.option(
    "--score",
    type=int,
    help=("The minimum score relevance that an article needs to have to be considered relevant"),
    default=None,
)
@click.option("--config-path", type=str, default=None, help=("The config file path"))
@click.option("--config", type=str, default=DEFAULT_CONFIG_SECTION, help=("The config settings to use"))
def run(
    model: str, prompt: str, iterations: int | None, score: int | None, config_path: str | None, config: str
) -> int:
    """
    Entrypoint of the application.

    Holds no logic. It calls the main method and returns 0 when succesful .
    """
    try:
        config_from_file = FileConfig.get_config_from_file(config_section=config, path=config_path)
        final_config = FinalConfig.init_from_dict(
            {
                "model": model or config_from_file.model,
                "prompt": prompt or config_from_file.prompt,
                "score_threshold": score or config_from_file.score_threshold,
                "iterations": iterations or config_from_file.iterations,
            }
        )
    except InvalidConfigError as err:
        raise click.BadParameter(err.args[0]) from None
    except ConfigNotFoundError:
        raise click.BadParameter("Config file `%s` not found!" % config_path) from None

    relevant_articles = hackerman(
        iterations=final_config.iterations,
        model=final_config.model,
        prompt=get_prompt(final_config.prompt),
        score_threshold=final_config.score_threshold,
    )
    relevant_articles_titles = [article.title for article in relevant_articles]
    logger.warning("Found these articles: %s", "\n".join(relevant_articles_titles))
    return 0
