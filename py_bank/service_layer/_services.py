"""Module contains the different services used."""
from sqlalchemy.orm.session import Session

from py_bank.domain._models import Account, Transfer

# pylint: disable=W0613


def list_account_transfers(
    session: Session,
    account_id: str,
):
    """List movements of local account."""
    transfers = (
        session.query(Transfer)
        .filter((Transfer.src_account_id == account_id) | (Transfer.dest_account_id == account_id))
        .all()
    )
    return transfers


def intra_money_transfer(
    session: Session, source: Account, destination: Account, amount: float, info: str
):
    """Perform an intra-bank transfer."""


def add_funds(account_id: str, amount: float):
    """Add funds from an account."""


def remove_funds(account_id: str, amount: float):
    """Remove funds from an account.

    Args:
        account_id (str): _description_
        amount (float): _description_
    """
