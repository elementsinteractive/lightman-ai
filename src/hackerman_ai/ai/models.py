from dataclasses import dataclass
from enum import StrEnum
from typing import override


class Priority(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class New:
    title: str
    description: str
    link: str

    @override
    def __eq__(self, value: object) -> bool:
        assert isinstance(value, New)
        return self.link == value.link

    @override
    def __hash__(self) -> int:
        return hash(self.link.encode())


@dataclass
class News:
    news: list[New]

    @property
    def titles(self) -> list[str]:
        return [new.title for new in self.news]

    @property
    def links(self) -> list[str]:
        return [new.link for new in self.news]
