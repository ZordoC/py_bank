"""Module responsible for the ORM."""
from sqlalchemy import Column, Float, MetaData, String, Table
from sqlalchemy.orm import mapper

from py_bank.domain._models import Account, Transfer

metadata = MetaData()

accounts = Table(
    "Accounts",
    metadata,
    Column("account_id", String(255), primary_key=True),
    Column("balance", Float(255), nullable=False),
)

transfers = Table(
    "Transfers",
    metadata,
    Column("transfer_id", String(255), primary_key=True),
    Column("source_account_id", String(255)),
    Column("dest_account_id", String(255)),
    Column("anount", Float(255), nullable=False),
)


def start_mappers():
    """Map ``Account`` and ``Transfer`` to accounts and transfers."""
    mapper(Account, accounts)
    mapper(Transfer, transfers)
