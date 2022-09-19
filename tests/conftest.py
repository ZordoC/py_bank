"""Conftest for `py_repo` package."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from py_bank.service_layer import metadata, start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def domain_session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


def insert_accounts(session):
    session.execute("INSERT INTO accounts (account_id, balance)" " VALUES (1, 1230.30)")
    session.execute("INSERT INTO accounts (account_id, balance)" " VALUES (2, 40102.28)")


def insert_transfers(session):
    session.execute(
        "INSERT INTO transfers (transfer_id, amount, transfer_type, src_account_id, dest_account_id)"
        ' VALUES (1, 1203.23, "IntraBank", 2, 1)'
    )
    session.execute(
        "INSERT INTO transfers (transfer_id, amount, transfer_type, src_account_id, dest_account_id)"
        ' VALUES (2, 320.13, "IntraBank", 10, 1)'
    )


@pytest.fixture(autouse=True)
def add_data(domain_session):
    # prepare something ahead of all tests
    insert_accounts(domain_session)
    insert_transfers(domain_session)
