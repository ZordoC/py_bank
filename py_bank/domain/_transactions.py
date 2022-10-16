"""Module for Transaction Protocol."""
from typing import Protocol


#  pylint: disable=too-few-public-methods
class Transaction(Protocol):
    """Transaction Protocol."""

    def execute(self) -> None:
        """Executes a transaction."""
