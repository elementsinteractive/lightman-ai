from unittest.mock import Mock, patch

from lightman_ai.article.models import Article, SelectedArticle, SelectedArticlesList

from eval.classifier import Classifier
from eval.constants import MISSED_ARTICLE_REASON, MISSED_ARTICLE_RELEVANCE_SCORE


class TestClassifier:
    def transform_articles_to_selected_articles(self, articles: list[Article], score: int) -> list[SelectedArticle]:
        return [
            SelectedArticle(title=article.title, link=article.link, why_is_relevant="", relevance_score=score)
            for article in articles
        ]

    def test__get_false_negatives(self) -> None:
        relevant_articles = [Article(title="", link=f"relevant {i}", description="") for i in range(2)]
        non_relevant_articles = [Article(title="", link=f"non relevant {i}", description="") for i in range(2)]

        selected_articles_above_threshold = self.transform_articles_to_selected_articles(
            [relevant_articles[0]], score=7
        )
        selected_articles_below_threshold = self.transform_articles_to_selected_articles(non_relevant_articles, score=1)

        correctly_classified_articles = {selected_articles_above_threshold[0]}

        # We craft a list of the results that were returned by the LLM
        # where one of the articles is not there at all
        agent_results = SelectedArticlesList(
            articles=list(correctly_classified_articles) + selected_articles_below_threshold
        )

        false_negatives = Classifier(
            agent=Mock(),
            score=7,
            relevant_articles=set(relevant_articles),
            non_relevant_articles=set(non_relevant_articles),
            samples=1,
        )._get_false_negatives(correctly_classified_articles, agent_results)

        missed_article = relevant_articles[1]
        assert false_negatives == {
            SelectedArticle(
                title=missed_article.title,
                link=missed_article.link,
                why_is_relevant=MISSED_ARTICLE_REASON,
                relevance_score=MISSED_ARTICLE_RELEVANCE_SCORE,
            )
        }

    @patch("eval.classifier._classify_articles")
    @patch("eval.classifier.Classifier._can_run_in_parallel")
    def test__classify(self, mock_parallel: Mock, mock_classify: Mock) -> None:
        relevant_articles = [Article(title="", link=f"relevant {i}", description="") for i in range(2)]
        non_relevant_articles = [Article(title="", link=f"non relevant {i}", description="") for i in range(2)]

        selected_articles_above_threshold = self.transform_articles_to_selected_articles(
            [relevant_articles[0], non_relevant_articles[0]], score=7
        )
        selected_articles_below_threshold = self.transform_articles_to_selected_articles(
            non_relevant_articles[:1] + [relevant_articles[1]], score=1
        )

        mock_parallel.return_value = True
        mock_classify.return_value = SelectedArticlesList(
            articles=selected_articles_above_threshold + selected_articles_below_threshold
        )
        classified_articles = Classifier(
            agent=Mock(),
            score=7,
            relevant_articles=set(relevant_articles),
            non_relevant_articles=set(non_relevant_articles),
            samples=1,
        ).run()
        assert classified_articles[0].total_results == 2

        assert classified_articles[0].total_correctly_found_articles == 1
        assert classified_articles[0].correctly_found_articles == {relevant_articles[0]}
        assert isinstance(classified_articles[0].correctly_found_articles.pop(), SelectedArticle)

        assert classified_articles[0].total_false_negatives == 1
        assert classified_articles[0].false_negatives == {relevant_articles[1]}
        assert isinstance(classified_articles[0].false_negatives.pop(), SelectedArticle)

        assert classified_articles[0].total_false_positives == 1
        assert classified_articles[0].false_positives == {non_relevant_articles[0]}
        assert isinstance(classified_articles[0].false_positives.pop(), SelectedArticle)
