"""Controlls."""
from dataclasses import dataclass

from ._transactions import Transaction


@dataclass
class BankController:
    """Controller to execute commands."""

    def execute(self, command: Transaction) -> None:
        """Executes a command.

        Args:
            command (Transaction): Executes a transaction.
        """
        command.execute()
