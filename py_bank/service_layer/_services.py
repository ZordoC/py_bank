"""Module contains the different services used."""
from py_bank.domain._models import Account

# pylint: disable=W0613


def list_account_transfers(account_id: str):
    """List movements of local account."""


def transfer_money(source: Account, destination: Account, amount: float, info: str):
    """Perform an intra-bank transfer."""


def add_funds(account_id: str, amount: float):
    """Add funds from an account."""


def remove_funds(account_id: str, amount: float):
    """Remove funds from an account.

    Args:
        account_id (str): _description_
        amount (float): _description_
    """
