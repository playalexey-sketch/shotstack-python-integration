"""Custom exceptions for Shotstack API client."""


class ShotstackError(Exception):
    """Base exception for Shotstack API errors."""

    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response


class AuthenticationError(ShotstackError):
    """Raised when API authentication fails (401)."""

    pass


class RenderError(ShotstackError):
    """Raised when video rendering fails (5xx)."""

    pass


class NotFoundError(ShotstackError):
    """Raised when a resource is not found (404)."""

    pass


class ValidationError(ShotstackError):
    """Raised when request validation fails (422)."""

    pass


class RateLimitError(ShotstackError):
    """Raised when API rate limit is exceeded (429)."""

    pass
