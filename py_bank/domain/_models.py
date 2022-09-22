"""Module for domain-business models."""
from dataclasses import dataclass
from typing import Literal

from sqlalchemy import func
from sqlalchemy.orm.session import Session


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

    @classmethod
    def factory(
        cls,
        session: Session,
        source_id: int,
        dest_id: int,
        amount: float,
        info: str,
        transfer_type: Literal["IntraBank", "InterBank"] = "IntraBank",
    ):  # pylint: disable=too-many-arguments
        """Create a Transfer.

        Args:
            session (Session): Valid sqlalchemy session.
            source_id (str): Account id of origin.
            dest_id (str): Account ID of destination.
            amount (float): Amount of money to be transfered
        """
        largest_id = session.query(func.max(cls.transfer_id)).one()[0]
        new_id = largest_id + 1  # hacky way to make sure it's doesn't break primary key constraint.
        return cls(new_id, amount, transfer_type, source_id, dest_id, info)
