from abc import ABC, abstractmethod

from hackerman_ai.article.models import SelectedArticlesList


class BaseAgent(ABC):
    def get_prompt_result(self, prompt: str, iterations: int = 1) -> SelectedArticlesList:
        if not iterations > 0:
            raise ValueError("`iterations` must be > 0.")

        articles = self._run_prompt_multiple_times(prompt, iterations)
        return self._merge_results(articles)

    @abstractmethod
    def _run_prompt(self, prompt: str) -> SelectedArticlesList: ...

    def _run_prompt_multiple_times(self, prompt: str, iterations: int) -> list[SelectedArticlesList]:
        results = []
        for _ in range(iterations):
            results.append(self._run_prompt(prompt))
        return results

    def _merge_results(self, articles_list_of_lists: list[SelectedArticlesList]) -> SelectedArticlesList:
        """Merge all the news, removing repeated ones."""
        all_articles = set()
        for articles_list in articles_list_of_lists:
            for article in articles_list.articles:
                all_articles.add(article)
        return SelectedArticlesList(articles=list(all_articles))
