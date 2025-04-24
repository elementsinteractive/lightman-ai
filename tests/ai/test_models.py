from hackerman_ai.ai.models import New


class TestNews:
    def test_compare_new_objects(self) -> None:
        new1 = New(title="", description="", link="A")
        same_new = New(title="", description="", link="A")
        different_new = New(title="", description="", link="B")

        assert new1 == same_new
        assert new1 != different_new
