"""Unit tests for ``py_bank.service_layer._services``, some data has been added
to an in-memory SQLite3 database to run tests ``tests/conftest.py``"""

from py_bank.domain import Account, Transfer
from py_bank.service_layer import list_account_transfers


def list_accounts(session):
    accounts = session.query(Account).all()
    return accounts


def list_transfers(session):
    transfers = session.query(Transfer).all()
    return transfers


def test_list_all_accounts(domain_session):
    # insert_accounts(domain_session)
    accounts = list_accounts(domain_session)
    assert len(accounts) == 2


def test_list_all_transfers(domain_session):
    # insert_transfers(domain_session)
    transfers = list_transfers(domain_session)
    assert len(transfers) == 2


def test_list_transfers_from_account(domain_session):

    transfers_by_account_2 = list_account_transfers(domain_session, "2")
    assert len(transfers_by_account_2) == 1
    transfers_by_account_1 = list_account_transfers(domain_session, "1")
    assert len(transfers_by_account_1) == 2


def test_intra_transfer(domain_session):
    pass
