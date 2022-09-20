"""Module for agent errors."""


class InvalidBankID(ValueError):
    """Raised when invalid bank ID, associated with error 405."""


class AgentError(Exception):
    """Raised when Agent faces an unknown issue."""


class OverAllowedAmount(ValueError):
    """Raised when trying to transfer more than the allowed amount."""


class InterTransferFailed(Exception):
    """Raise when an inter-bank transfer fails."""
