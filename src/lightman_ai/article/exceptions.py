class ArticleBaseError(Exception):
    """Base class for article-related models errors."""


class NoTimeZoneError(ArticleBaseError):
    """Exception class for when there is no timezone associated to a date."""


class DifferentArticleClassesError(ArticleBaseError):
    """Exception for when we try to merge two Article Classes."""
