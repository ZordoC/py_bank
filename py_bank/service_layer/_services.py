"""Module contains the different services used."""
from typing import Literal

from sqlalchemy import func
from sqlalchemy.exc import NoResultFound  # type: ignore[attr-defined]
from sqlalchemy.orm.session import Session

from py_bank.domain._models import Account, Transfer
from py_bank.errors import AccountNotFound, InsuficientBalance

# pylint: disable=W0613


def list_account_transfers(
    session: Session,
    account_id: int,
):
    """List movements of local account."""
    transfers = (
        session.query(Transfer)
        .filter((Transfer.src_account_id == account_id) | (Transfer.dest_account_id == account_id))
        .all()
    )
    return transfers


def intra_money_transfer(session: Session, source_id: int, dest_id: int, amount: float, info: str = ""):
    """Perform an intra-bank transfer.

    Args:
        session (Session): Valid sqlalchemy session.
        source_id (str): Account id of origin.
        dest_id (str): Account ID of destination.
        amount (float): Amount of money to be transfered

    Raises:
        InsuficientBalance: Not enough funds available for transfer.
    """
    try:
        sender = session.query(Account).filter_by(account_id=source_id).one()
        dest = session.query(Account).filter_by(account_id=dest_id).one()

    except NoResultFound as exc:
        raise AccountNotFound("Sender or destination not present in records.") from exc

    if sender.balance < amount:
        raise InsuficientBalance("Not enough funds to transfer.")

    dest.balance += amount
    sender.balance -= amount

    transfer = Transfer.factory(session, source_id, dest_id, amount, info)

    session.add(transfer)
    session.commit()


def create_transfer(
    session,
    source_id: int,
    dest_id: int,
    amount: float,
    info: str,
    transfer_type: Literal["IntraBank", "InterBank"] = "IntraBank",
):  # pylint: disable=too-many-arguments
    """Add a Transfer to records.

    Args:
        session (Session): Valid sqlalchemy session.
        source_id (str): Account id of origin.
        dest_id (str): Account ID of destination.
        amount (float): Amount of money to be transfered
    """
    largest_id = session.query(func.max(Transfer.transfer_id)).one()[0]
    new_id = largest_id + 1  # hacky way to make sure it's doesn't break primary key constraint.
    return Transfer(new_id, amount, transfer_type, source_id, dest_id, info)


def add_funds(session: Session, account_id: str, amount: float):
    """Add funds from an account.

    Args:
        session (Session): Valid sqlalchemy session.
        account_id (str): ID of the account to be charged with funds.
        amount (float): Amount to charfe the account

    Raises:
        AccountNotFound: _description_
    """
    try:
        account = session.query(Account).filter_by(account_id=account_id).one()
    except NoResultFound as exc:
        raise AccountNotFound("Sender or destination not present in records.") from exc
    account.balance = account.balance + amount
    session.commit()


def remove_funds(session: Session, account_id: str, amount: float):
    """Remove funds from an account.

    Args:
        account_id (str): _description_
        amount (float): _description_
    """
    try:
        account = session.query(Account).filter_by(account_id=account_id).one()
    except NoResultFound as exc:
        raise AccountNotFound("Sender or destination not present in records.") from exc

    if account.balance < amount:
        raise InsuficientBalance("Amount surpasses balance.")

    account.balance = account.balance - amount
    session.commit()
