import asyncio
import logging
import time

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.article.models import (
    Article,
    ArticlesList,
    PrimarySelectedArticle,
    SelectedArticlesList,
)
from lightman_ai.main import _classify_articles

from eval.constants import MAX_WORKERS, MISSED_ARTICLE_REASON, MISSED_ARTICLE_RELEVANCE_SCORE
from eval.utils import ClassifiedArticleResults

logger = logging.getLogger("eval")


class Classifier:
    def __init__(
        self,
        *,
        agent: BaseAgent,
        score: int,
        relevant_articles: set[Article],
        non_relevant_articles: set[Article],
        samples: int,
        workers: int,
    ) -> None:
        self.agent = agent
        self.score = score
        self.relevant_articles = relevant_articles
        self.non_relevant_articles = non_relevant_articles
        self.samples = samples
        self.workers = workers
        if overlapping_articles := self.relevant_articles & self.non_relevant_articles:
            raise RuntimeError("These articles are in both relevant and non-relevant sets! %s" % overlapping_articles)

    async def run(self) -> list[ClassifiedArticleResults]:
        if self.workers > MAX_WORKERS:
            raise RuntimeError("Too many workers specified while running `eval`.")

        # Use asyncio.Semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(self.workers)

        async def _classify_with_semaphore() -> ClassifiedArticleResults:
            async with semaphore:
                return await self._classify()

        # Use asyncio.gather for concurrent execution of async tasks
        tasks = [_classify_with_semaphore() for _ in range(self.samples)]
        return await asyncio.gather(*tasks)

    async def _classify(self) -> ClassifiedArticleResults:
        articles = ArticlesList(articles=list(self.relevant_articles) + list(self.non_relevant_articles))

        time_before = time.perf_counter()
        results = await _classify_articles(
            articles=articles,
            agent=self.agent,
        )
        time_delta = round(time.perf_counter() - time_before, 2)

        self._check_results_integrity(results)

        correctly_found_articles = set()
        false_positives = set()

        articles_above_threshold = results.get_articles_with_score_gte_threshold(self.score)
        for article in articles_above_threshold:
            if article in self.relevant_articles:
                correctly_found_articles.add(article)
            elif article in self.non_relevant_articles:
                false_positives.add(article)
            else:
                logger.error("%s is not present either in relevant_articles nor in non_relevant_articles", article)

        false_negatives = self._get_false_negatives(correctly_found_articles, results)
        return ClassifiedArticleResults(
            articles=articles_above_threshold,
            correctly_found_articles=correctly_found_articles,
            false_positives=false_positives,
            false_negatives=false_negatives,
            total_relevant_articles=len(self.relevant_articles),
            time_delta=time_delta,
        )

    def _check_results_integrity(self, results: SelectedArticlesList) -> None:
        if len(results.articles) > len(self.relevant_articles) + len(self.non_relevant_articles):
            # Sometimes, some LLM models fail to return all the articles
            # even if explicitly told so
            diff_count = len(results.articles) - len(self.relevant_articles) - len(self.non_relevant_articles)
            extra_articles = set(results.articles) - set(
                list(self.relevant_articles) + list(self.non_relevant_articles)  # type: ignore[arg-type]
            )
            logger.error("Got more articles than expected! Total: %s. articles: %s", diff_count, extra_articles)

        if len(results.articles) < len(self.relevant_articles) + len(self.non_relevant_articles):
            diff_count = len(self.relevant_articles) + len(self.non_relevant_articles) - len(results.articles)
            missing_articles = set(list(self.relevant_articles) + list(self.non_relevant_articles)) - set(
                results.articles  # type: ignore[arg-type]
            )
            logger.error("Got less articles than expected! Total: %s. articles: %s", diff_count, missing_articles)

    def _get_false_negatives(
        self, correctly_found_articles: set[PrimarySelectedArticle], results: SelectedArticlesList
    ) -> set[PrimarySelectedArticle]:
        false_negatives_no_score = set(self.relevant_articles).difference(correctly_found_articles)

        # We cannot use here `set(results.articles).insterection(false_negatives_no_score)` to retrieve
        # the `SelectedArticle`s classified as false negatives.
        # The reason is that even if `Article` and `SelectedArticle` can be compared against each other
        # because of our implementation, it is not guaranteed that doing and intersection of
        # selected_article_object_set & article_object_set will return `SelectedArticle` object,
        # as per Python implementation it will pick up the one that's optimum to select,
        # wich can be an instance of `Article` instead.
        # Because of this, we have to manually craft the set
        false_negatives: set[PrimarySelectedArticle] = {
            article for article in results.articles if article in false_negatives_no_score
        }
        if false_negatives_diff := false_negatives_no_score.difference(false_negatives):
            # The LLM did not return all the articles
            # We are going to add it to the set,
            # even if we don't have the computed values
            for article in false_negatives_diff:
                false_negatives.add(
                    PrimarySelectedArticle(
                        title=article.title,
                        link=article.link,
                        why_is_relevant=MISSED_ARTICLE_REASON,
                        relevance_score=MISSED_ARTICLE_RELEVANCE_SCORE,
                        published_at=article.published_at,
                    )
                )
        return false_negatives
