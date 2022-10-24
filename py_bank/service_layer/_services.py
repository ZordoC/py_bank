"""Module contains the different services used."""
from sqlalchemy.exc import NoResultFound  # type: ignore[attr-defined]
from sqlalchemy.orm.session import Session

from py_bank.domain._commands import Transfer
from py_bank.domain._models import Account, TransferRecord
from py_bank.domain._transactions import Transaction
from py_bank.errors import AccountNotFound, InsuficientBalance

# pylint: disable=W0613


def list_account_transfers(
    session: Session,
    account_id: int,
):
    """List movements of local account."""
    transfers = (
        session.query(TransferRecord)
        .filter((TransferRecord.src_account_id == account_id) | (TransferRecord.dest_account_id == account_id))
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

    command = Transfer(sender, dest, amount, info)
    command.execute()
    transfer_record = TransferRecord.factory(session, sender.account_id, dest.account_id, amount, info)

    session.add(transfer_record)
    session.commit()


def get_account_from_id(session: Session, account_id: int) -> Account:
    """Create an ``Account`` object given it's id.

    Args:
        session (Session): Session to the database.
        account_id (int): ``Account`` object identifer.

    Returns:
        Account: An ``Account`` object.
    """
    try:
        account = session.query(Account).filter_by(account_id=account_id).one()
    except NoResultFound as exc:
        raise AccountNotFound("Sender or destination not present in records.") from exc
    return account


def execute_command(session: Session, command: Transaction):
    """Executes a Transaction.

    Args:
        session (Session): Valid sqlalchemy session.
        command: ``Transaction`` type object.
    """
    command.execute()
    session.commit()
