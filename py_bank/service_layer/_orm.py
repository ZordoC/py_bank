"""Module responsible for the ORM."""
from sqlalchemy import Column, Float, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper

from py_bank.domain._models import Account, TransferRecord

metadata = MetaData()

accounts = Table(
    "Accounts",
    metadata,
    Column("account_owner", String(255)),
    Column("account_id", Integer, primary_key=True),
    Column("balance", Float(255), nullable=False),
)

transfers = Table(
    "Transfers",
    metadata,
    Column("transfer_id", Integer, primary_key=True),
    Column("transfer_type", String(30)),
    Column("src_account_id", Integer),
    Column("dest_account_id", Integer),
    Column("amount", Float(255), nullable=False),
    Column("info", String(255)),
)


def start_mappers():
    """Map ``Account`` and ``Transfer`` to accounts and transfers."""
    mapper(Account, accounts)
    mapper(TransferRecord, transfers)
