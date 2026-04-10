class BaseSourceError(Exception):
    """Base Exception class for errors."""


class MalformedSourceResponseError(BaseSourceError):
    """Exception for when the respose format does not match the expected one."""


class IncompleteArticleFromSourceError(MalformedSourceResponseError):
    """Exception for when all the mandatory fields could not be retrieved from an article."""


class SourceError(BaseSourceError):
    """Exception for when something went wrong while downloading or parsing the articles from source."""


class NoArticlesError(BaseSourceError):
    """Exception for when no articles where found after the download was successful."""
