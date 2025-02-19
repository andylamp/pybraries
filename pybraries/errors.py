"""Module that includes the custom exceptions used throughout."""


class APIKeyMissingError(Exception):
    """Custom error for API Key missing."""


class SessionNotInitialisedError(Exception):
    """Custom error indicating that the session has not been initialised yet."""
