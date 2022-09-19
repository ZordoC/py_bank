"""Module for custom exceptions."""


class InsuficientBalanceforTransfer(ValueError):
    """Raised when sender as insuficient balance to send."""


class AccountForTransferNotFound(Exception):
    """Raised when either sender or destination don't exist."""
