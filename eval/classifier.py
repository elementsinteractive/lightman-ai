import logging
import time
from concurrent.futures import ThreadPoolExecutor

from lightman_ai.ai.base.agent import BaseAgent
from lightman_ai.ai.gemini.agent import GeminiAgent
from lightman_ai.ai.openai.agent import OpenAIAgent
from lightman_ai.article.models import Article, ArticlesList, SelectedArticle, SelectedArticlesList
from lightman_ai.core.settings import settings
from lightman_ai.main import _classify_articles

from eval.constants import EVAL_WORKERS, MAX_WORKERS, MISSED_ARTICLE_REASON, MISSED_ARTICLE_RELEVANCE_SCORE
from eval.utils import ClassifiedArticleResults

logger = logging.getLogger("eval")


class Classifier:
    def __init__(
        self,
        *,
        agent: BaseAgent,
        prompt: str,
        score: int,
        relevant_articles: set[Article],
        non_relevant_articles: set[Article],
        samples: int,
    ) -> None:
        self.agent = agent
        self.prompt = prompt
        self.score = score
        self.relevant_articles = relevant_articles
        self.non_relevant_articles = non_relevant_articles
        self.samples = samples

        if overlapping_articles := self.relevant_articles & self.non_relevant_articles:
            raise RuntimeError("These articles are in both relevant and non-relevant sets! %s" % overlapping_articles)

    def run(self) -> list[ClassifiedArticleResults]:
        if self._can_run_in_parallel(self.agent):
            return self._parallel_run()
        else:
            return self._sync_run()

    def _classify(self) -> ClassifiedArticleResults:
        articles = ArticlesList(articles=list(self.relevant_articles) + list(self.non_relevant_articles))

        time_before = time.perf_counter()
        results = _classify_articles(
            articles=articles,
            prompt=self.prompt,
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
        self, correctly_found_articles: set[SelectedArticle], results: SelectedArticlesList
    ) -> set[SelectedArticle]:
        false_negatives_no_score = set(self.relevant_articles).difference(correctly_found_articles)

        # We cannot use here `set(results.articles).insterection(false_negatives_no_score)` to retrieve
        # the `SelectedArticle`s classified as false negatives.
        # The reason is that even if `Article` and `SelectedArticle` can be compared against each other
        # because of our implementation, it is not guaranteed that doing and intersection of
        # selected_article_object_set & article_object_set will return `SelectedArticle` object,
        # as per Python implementation it will pick up the one that's optimum to select,
        # wich can be an instance of `Article` instead.
        # Because of this, we have to manually craft the set
        false_negatives: set[SelectedArticle] = {
            article for article in results.articles if article in false_negatives_no_score
        }
        if false_negatives_diff := false_negatives_no_score.difference(false_negatives):
            # The LLM did not return all the articles
            # We are going to add it to the set,
            # even if we don't have the computed values
            for article in false_negatives_diff:
                false_negatives.add(
                    SelectedArticle(
                        title=article.title,
                        link=article.link,
                        why_is_relevant=MISSED_ARTICLE_REASON,
                        relevance_score=MISSED_ARTICLE_RELEVANCE_SCORE,
                    )
                )
        return false_negatives

    @staticmethod
    def _can_run_in_parallel(agent: BaseAgent) -> bool:
        if isinstance(agent, OpenAIAgent):
            return False
        if isinstance(agent, GeminiAgent):
            return True
        raise RuntimeError(f"No information about if it is possible to run `{agent}` in parallel.")

    def _parallel_run(self) -> list[ClassifiedArticleResults]:
        if EVAL_WORKERS + settings.PARALLEL_WORKERS > MAX_WORKERS:
            raise RuntimeError("Too many workers specified while running `eval`.")

        with ThreadPoolExecutor(max_workers=EVAL_WORKERS) as executor:
            futures = [executor.submit(self._classify) for _ in range(self.samples)]
            return [f.result() for f in futures]

    def _sync_run(self) -> list[ClassifiedArticleResults]:
        return [self._classify() for _ in range(self.samples)]
