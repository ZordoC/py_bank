"""Module for ``pybank`` errors."""


class InvalidBankID(ValueError):
    """Raised when invalid bank ID, associated with error 405."""


class AgentError(Exception):
    """Raised when Agent faces an unknown issue."""


class OverAllowedAmount(ValueError):
    """Raised when trying to transfer more than the allowed amount."""


class InterTransferFailed(Exception):
    """Raise when an inter-bank transfer fails."""


class InsuficientBalance(ValueError):
    """Raised when sender as insuficient balance to send, associated with 402
    Error code."""


class AccountNotFound(Exception):
    """Raised when either sender or destination don't exist, associated with
    403 Error code."""
