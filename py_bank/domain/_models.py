"""Module for domain-business models."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Account:
    """Model for an Account."""

    account_id: str
    balance: float


@dataclass()
class Transfer:
    """Model for a Transfer."""

    transfer_id: str
    amount: float
    transfer_type: Literal["IntraBank", "InterBank"]
    src_account_id: str
    dest_account_id: str
