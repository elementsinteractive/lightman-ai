from hackerman_ai.article.models import Article, ArticlesList, SelectedArticle, SelectedArticlesList


class TestBaseArticle:
    def test_compare_article_objects(self) -> None:
        new1 = Article(title="", description="", link="A")
        same_new = Article(title="", description="", link="A")
        different_new = Article(title="", description="", link="B")

        assert new1 == same_new
        assert new1 != different_new


class TestArticle:
    def test_number_of_tokens(self) -> None:
        article = Article(title="Elephant gives birth to a monkey", description="lorem ipsum", link="https://aaaa.com")
        assert article.number_of_tokens == 14


class TestSelectedArticle:
    def test_number_of_tokens(self) -> None:
        article = SelectedArticle(link="https://aaaa.com")
        assert article.number_of_tokens == 4


class TestArticlesList:
    def test_total_number_of_tokens(self) -> None:
        article1 = Article(title="Elephant gives birth to a monkey", description="lorem ipsum", link="https://aaaa.com")
        article2 = Article(title="Elephant gives birth to a monkey", description="lorem ipsum", link="https://aaaa.com")

        articles_list = ArticlesList(articles=[article1, article2])
        assert articles_list.total_number_of_tokens == 28


class TestSelectedArticlesList:
    def test_total_number_of_tokens(self) -> None:
        article1 = SelectedArticle(link="https://aaaa.com")
        article2 = SelectedArticle(link="https://aaaa.com")

        articles_list = SelectedArticlesList(articles=[article1, article2])
        assert articles_list.total_number_of_tokens == 8
