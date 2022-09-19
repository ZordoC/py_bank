"""Module for domain-business models."""

from dataclasses import dataclass, field
from typing import  Literal


@dataclass
class Account:
    """Model for an Account."""
    account_id: str
    money: float


@dataclass(frozen=True)
class Transfer:
    """Model for a Transfer."""
    amount: float
    type: Literal["IntraBank", "InterBank"]
    source_id: str
    source_is: str
