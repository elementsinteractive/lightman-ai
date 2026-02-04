from lightman_ai.sources.base import BaseSource
from lightman_ai.sources.the_hacker_news import TheHackerNewsSource

# Mapping of source names to their corresponding classes
SOURCE_REGISTRY = {
    "the_hacker_news": TheHackerNewsSource,
}

SOURCE_CHOICES = list(SOURCE_REGISTRY.keys())


def get_source_class_from_source_name(source_name: str) -> type[BaseSource]:
    """
    Get the source class for a given source name.

    Args:
        source_name: The name of the source (e.g., "the_hacker_news")

    Returns:
        The source class corresponding to the source name

    Raises:
        ValueError: If the source name is not supported
    """
    if source_name not in SOURCE_REGISTRY:
        supported_sources = ", ".join(SOURCE_CHOICES)
        raise ValueError(f"Unsupported source: {source_name}. Supported sources: {supported_sources}")

    return SOURCE_REGISTRY[source_name]
