"""Module responsible for the ORM"""
from sqlalchemy import Column, Float, MetaData, String, Table
from sqlalchemy.orm import mapper

from py_bank.domain.models import Account, Transfer

metadata = MetaData()

accounts = Table(
    "Accounts",
    metadata,
    Column("account_id", String(255), primary_key=True),
    Column("amnount", Float(255), nullable=False)
)

transfers = Table(
    "Transfers",
    metadata,
    Column("account_id", String(255), primary_key=True),
    Column("amnount", Float(255), nullable=False)
)


def start_mappers():
    """Map ``Order`` to orders table."""
    mapper(Account, accounts)
    mapper(Transfer, transfers)
