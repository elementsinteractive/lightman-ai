from dataclasses import dataclass
from enum import StrEnum


class Priority(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class New:
    title: str
    priority: Priority
    description: str
    why_is_relevant: str
    link: str


@dataclass
class News:
    news: list[New]
