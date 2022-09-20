"""Module for agent errors"""


class InvalidBankID(ValueError):
    """Raised when invalid bank ID, associated with error 405"""


class AgentError(Exception):
    """Raised when Agent faces an unknown issue."""
