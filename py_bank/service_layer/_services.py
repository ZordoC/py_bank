"""Module contains the different services used."""
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound  # type: ignore[attr-defined]
from sqlalchemy.orm.session import Session

from py_bank.domain._models import Account, Transfer

from ._error import AccountForTransferNotFound, InsuficientBalanceforTransfer

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


def intra_money_transfer(session: Session, source_id: int, dest_id: int, amount: float):
    """Perform an intra-bank transfer.

    Args:
        session (Session): Valid sqlalchemy session.
        source_id (str): Account id of origin.
        dest_id (str): Account ID of destination.
        amount (float): Amount of money to be transfered

    Raises:
        InsuficientBalanceforTransfer: _description_
    """
    try:
        sender = session.query(Account).filter_by(account_id=source_id).one()
        dest = session.query(Account).filter_by(account_id=dest_id).one()

    except NoResultFound as exc:
        raise AccountForTransferNotFound("Sender or destination not present in records.") from exc

    if sender.balance < amount:
        raise InsuficientBalanceforTransfer("Not enough money to transfer.")

    dest.balance += amount
    sender.balance -= amount

    transfer = _create_transfer(session, source_id, dest_id, amount)

    session.add(transfer)
    session.commit()


def _create_transfer(session, source_id: int, dest_id: int, amount: float):
    """Add a Transfer to records.

    Args:
        session (Session): Valid sqlalchemy session.
        source_id (str): Account id of origin.
        dest_id (str): Account ID of destination.
        amount (float): Amount of money to be transfered
    """
    largest_id = session.query(func.max(Transfer.transfer_id)).one()[0]
    new_id = largest_id + 1  # hacky way to make sure it's doesn't break primary key constraint.
    return Transfer(new_id, amount, "IntraBank", source_id, dest_id)


def add_funds(session: Session, account_id: str, amount: float):
    """Add funds from an account."""


def remove_funds(account_id: str, amount: float):
    """Remove funds from an account.

    Args:
        account_id (str): _description_
        amount (float): _description_
    """
