from hackerman_ai.article.models import Article


class TestNews:
    def test_compare_news_objects(self) -> None:
        new1 = Article(title="", description="", link="A")
        same_new = Article(title="", description="", link="A")
        different_new = Article(title="", description="", link="B")

        assert new1 == same_new
        assert new1 != different_new
