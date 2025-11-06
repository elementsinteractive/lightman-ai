import asyncio
import logging
from datetime import datetime

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.ai.utils import get_agent_class_from_agent_name
from lightman_ai.article.models import ArticlesList, SelectedArticle, SelectedArticlesList
from lightman_ai.integrations.service_desk.integration import (
    ServiceDeskIntegration,
)
from lightman_ai.sources.the_hacker_news import TheHackerNewsSource

logger = logging.getLogger("lightman")
logger.addHandler(logging.NullHandler())


def _get_articles_from_source(start_date: datetime | None = None) -> ArticlesList:
    return TheHackerNewsSource().get_articles(start_date)


def _classify_articles(articles: ArticlesList, agent: BaseAgent) -> SelectedArticlesList:
    return agent.run_prompt(prompt=str(articles))


def _create_service_desk_issues(
    selected_articles: list[SelectedArticle],
    service_desk_client: ServiceDeskIntegration,
    service_desk_project_key: str,
    service_desk_request_id_type: str,
) -> None:
    async def schedule_task(article: SelectedArticle) -> None:
        try:
            description = f"*Why is relevant:*\n{article.why_is_relevant}\n\n*Source:* {article.link}\n\n*Score:* {article.relevance_score}/10"
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

    async def create_all() -> None:
        tasks = []
        for article in selected_articles:
            tasks.append(schedule_task(article))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        errors = [result for result in results if isinstance(result, Exception)]
        if errors:
            raise ExceptionGroup("Could not create all ServiceDesk issues", errors)

    asyncio.run(create_all())


def lightman(
    agent: str,
    prompt: str,
    score_threshold: int,
    service_desk_project_key: str | None = None,
    service_desk_request_id_type: str | None = None,
    dry_run: bool = False,
    model: str | None = None,
    start_date: datetime | None = None,
) -> list[SelectedArticle]:
    articles: ArticlesList = _get_articles_from_source(start_date)

    agent_class = get_agent_class_from_agent_name(agent)
    agent_instance = agent_class(prompt, model, logger=logger)

    classified_articles = _classify_articles(
        articles=articles,
        agent=agent_instance,
    )

    selected_articles: list[SelectedArticle] = classified_articles.get_articles_with_score_gte_threshold(
        score_threshold
    )

    if not dry_run:
        if not service_desk_project_key or not service_desk_request_id_type:
            raise ValueError("Missing Service Desk's project key or request id type")

        service_desk_client = ServiceDeskIntegration.from_env()
        _create_service_desk_issues(
            selected_articles=selected_articles,
            service_desk_client=service_desk_client,
            service_desk_project_key=service_desk_project_key,
            service_desk_request_id_type=service_desk_request_id_type,
        )

    return selected_articles
