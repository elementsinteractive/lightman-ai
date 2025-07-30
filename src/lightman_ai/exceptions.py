from lightman_ai.core.exceptions import BaseLightmanError


class MultipleDateSourcesError(BaseLightmanError):
    """Exception for when more than one date source is provided."""
