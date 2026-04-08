import asyncio
import logging
from datetime import datetime

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.ai.utils import get_agent_class_from_agent_name
from lightman_ai.article.models import ArticlesList, PrimarySelectedArticle, SelectedArticlesList
from lightman_ai.exceptions import NoSourcesError
from lightman_ai.integrations.service_desk.integration import (
    ServiceDeskIntegration,
)
from lightman_ai.sources.utils import get_source_class_from_source_name

logger = logging.getLogger("lightman")
logger.addHandler(logging.NullHandler())


async def _get_articles_from_source(source_name: str, start_date: datetime | None = None) -> ArticlesList:
    source_class = get_source_class_from_source_name(source_name)
    source_instance = source_class()
    logger.info("Retrieving articles from %s", source_class)
    return await source_instance.get_articles(start_date)


async def _classify_articles(articles: ArticlesList, agent: BaseAgent) -> SelectedArticlesList:
    return await agent.run_prompt(prompt=str(articles))


async def _create_service_desk_issues(
    selected_articles: list[PrimarySelectedArticle],
    service_desk_client: ServiceDeskIntegration,
    service_desk_project_key: str,
    service_desk_request_id_type: str,
) -> None:
    async def schedule_task(article: PrimarySelectedArticle) -> None:
        try:
            if article.related_articles:
                related_articles_raw = "\n".join(
                    [f"{related_article.title}: {related_article.link}" for related_article in article.related_articles]
                )
                related_articles = f"*Related Articles:*\n{related_articles_raw}\n\n"
            else:
                related_articles = ""

            description = f"*Why is relevant:*\n{article.why_is_relevant}\n\n*Source:* {article.link}\n\n{related_articles}*Score:* {article.relevance_score}/10"
            await service_desk_client.create_request_of_type(
                project_key=service_desk_project_key,
                summary=article.title,
                description=description,
                request_id_type=service_desk_request_id_type,
            )
            logger.info("Created issue for article %s", article.link)
        except Exception:
            logger.exception("Could not create ServiceDesk issue: %s, %s", article.title, article.link)
            raise

    tasks = []
    for article in selected_articles:
        tasks.append(schedule_task(article))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    errors = [result for result in results if isinstance(result, Exception)]
    if errors:
        raise ExceptionGroup("Could not create all ServiceDesk issues", errors)


async def lightman(
    agent: str,
    prompt: str,
    score_threshold: int,
    sources: list[str] | None = None,
    service_desk_project_key: str | None = None,
    service_desk_request_id_type: str | None = None,
    dry_run: bool = False,
    model: str | None = None,
    start_date: datetime | None = None,
) -> list[PrimarySelectedArticle]:
    if not sources:
        raise NoSourcesError

    articles = ArticlesList()
    for source in sources:
        articles += await _get_articles_from_source(source, start_date)

    multiple_sources = len(sources) > 1
    agent_class = get_agent_class_from_agent_name(agent)
    agent_instance = agent_class(multiple_sources, prompt, model, logger=logger)

    classified_articles = await _classify_articles(
        articles=articles,
        agent=agent_instance,
    )

    selected_articles: list[PrimarySelectedArticle] = classified_articles.get_articles_with_score_gte_threshold(
        score_threshold
    )

    if not dry_run:
        if not service_desk_project_key or not service_desk_request_id_type:
            raise ValueError("Missing Service Desk's project key or request id type")

        service_desk_client = ServiceDeskIntegration.from_env()
        await _create_service_desk_issues(
            selected_articles=selected_articles,
            service_desk_client=service_desk_client,
            service_desk_project_key=service_desk_project_key,
            service_desk_request_id_type=service_desk_request_id_type,
        )

    return selected_articles
