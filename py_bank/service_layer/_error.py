"""Module for custom exceptions."""


class InsuficientBalance(ValueError):
    """Raised when sender as insuficient balance to send."""


class AccountNotFound(Exception):
    """Raised when either sender or destination don't exist."""
