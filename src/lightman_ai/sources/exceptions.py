class BaseSourceError(Exception):
    """Base Exception class for errors."""


class MalformedSourceResponseError(BaseSourceError):
    """Exception for when the respose format does not match the expected one."""


class IncompleteArticleFromSourceError(MalformedSourceResponseError):
    """Exception for when all the mandatory fields could not be retrieved from an article."""
