from hackerman_ai.article.models import ArticlesList, SelectedArticlesList


class Processor:
    """This class is responsible of formatting the subset of articles that have been selected."""

    def __init__(self, original_articles: ArticlesList, selected_articles: SelectedArticlesList) -> None:
        self.original_articles = original_articles
        self.selected_articles = selected_articles

    def process(self) -> ArticlesList:
        return self._select_original_articles_from_selected()

    def _select_original_articles_from_selected(self) -> ArticlesList:
        selected_articles = [
            original_article
            for original_article in self.original_articles.articles
            if original_article in self.selected_articles.articles
        ]
        return ArticlesList(articles=list(selected_articles))
