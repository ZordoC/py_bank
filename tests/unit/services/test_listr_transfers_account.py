"""Unit tests for ``py_bank.service_layer._services.list_account_transfers``,
some data has been added to an in-memory SQLite3 database to run tests
``tests/conftest.py``"""
from py_bank.service_layer import list_account_transfers


def test_list_transfers_from_account(domain_session):

    transfers_by_account_2 = list_account_transfers(domain_session, 2)
    assert len(transfers_by_account_2) == 1
    transfers_by_account_1 = list_account_transfers(domain_session, 1)
    assert len(transfers_by_account_1) == 2
    transfers_by_account_1 = list_account_transfers(domain_session, 100)
    assert len(transfers_by_account_1) == 0
