"""Module for domain-business models."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Account:
    """Model for an Account."""

    account_owner: str
    account_id: int
    balance: float


@dataclass()
class Transfer:
    """Model for a Transfer."""

    transfer_id: int
    amount: float
    transfer_type: Literal["IntraBank", "InterBank"]
    src_account_id: int
    dest_account_id: int
    info: str = "Test"
