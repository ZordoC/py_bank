"""Contains all commands issued by a Bank."""
from dataclasses import dataclass

from ._models import Account


@dataclass
class Transfer:
    """Executes a transfer."""

    src_account: Account
    dest_account: Account
    amount: float

    def execute(self) -> None:
        """Transfer money between two accounts of the same bank."""
        self.src_account.withdraw(self.amount)
        self.dest_account.deposit(self.amount)


@dataclass
class Deposit:
    """Executes a Deposit."""

    account: Account
    amount: float

    def execute(self) -> None:
        """Execute."""
        self.account.deposit(self.amount)


@dataclass
class Withdrawal:
    """Executes a withdrawl."""

    account: Account
    amount: float

    def execute(self) -> None:
        """Execute."""
        self.account.withdraw(self.amount)
