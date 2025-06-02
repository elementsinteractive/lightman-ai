from unittest.mock import Mock, patch

from hackerman_ai.article.models import Article, SelectedArticle, SelectedArticlesList

from eval.evaluator import ClassifyArticlesInput, classify_articles


class TestEval:
    def transform_articles_to_selected_articles(self, articles: list[Article], score: int) -> list[SelectedArticle]:
        return [
            SelectedArticle(title=article.title, link=article.link, why_is_relevant="", relevance_score=score)
            for article in articles
        ]

    @patch("eval.evaluator._classify_articles")
    def test__classify_articles(self, mock_classify: Mock) -> None:
        relevant_articles = [Article(title="", link=f"relevant {i}", description="") for i in range(2)]
        non_relevant_articles = [Article(title="", link=f"non relevant {i}", description="") for i in range(2)]

        selected_articles_above_threshold = self.transform_articles_to_selected_articles(
            [relevant_articles[0], non_relevant_articles[0]], score=7
        )
        selected_articles_below_threshold = self.transform_articles_to_selected_articles(
            non_relevant_articles[:1] + [relevant_articles[1]], score=1
        )

        mock_classify.return_value = SelectedArticlesList(
            articles=selected_articles_above_threshold + selected_articles_below_threshold
        )
        classified_articles = classify_articles(
            ClassifyArticlesInput(
                agent=Mock(),
                prompt="",
                score=7,
                iterations=1,
                relevant_articles=set(relevant_articles),
                non_relevant_articles=set(non_relevant_articles),
            )
        )
        assert classified_articles.total_results == 2

        assert classified_articles.total_correctly_found_articles == 1
        assert classified_articles.correctly_found_articles == {relevant_articles[0]}
        assert isinstance(classified_articles.correctly_found_articles.pop(), SelectedArticle)

        assert classified_articles.total_false_negatives == 1
        assert classified_articles.false_negatives == {relevant_articles[1]}
        assert isinstance(classified_articles.false_negatives.pop(), SelectedArticle)

        assert classified_articles.total_false_positives == 1
        assert classified_articles.false_positives == {non_relevant_articles[0]}
        assert isinstance(classified_articles.false_positives.pop(), SelectedArticle)
