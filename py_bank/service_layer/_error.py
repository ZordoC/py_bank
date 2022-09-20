"""Module for custom exceptions."""


class InsuficientBalance(ValueError):
    """Raised when sender as insuficient balance to send, associated with 402
    Error code."""


class AccountNotFound(Exception):
    """Raised when either sender or destination don't exist, associated with
    403 Error code."""
