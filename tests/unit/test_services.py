"""Unit tests for ``py_bank.service_layer._services``"""

from py_bank.domain import Account, Transfer
from py_bank.service_layer import list_account_transfers


def insert_accounts(session):
    session.execute("INSERT INTO accounts (account_id, balance)" ' VALUES ("1AB", 1230.30)')
    session.execute("INSERT INTO accounts (account_id, balance)" ' VALUES ("2AB", 40102.28)')


def insert_transfers(session):
    session.execute(
        "INSERT INTO transfers (transfer_id, amount, transfer_type, src_account_id, dest_account_id)"
        ' VALUES ("1", 1200, "IntraBank", "2AB", "1AB")'
    )


def list_accounts(session):
    accounts = session.query(Account).all()
    return accounts


def list_transfers(session):
    transfers = session.query(Transfer).all()
    return transfers


def test_list_all_accounts(domain_session):
    insert_accounts(domain_session)
    accounts = list_accounts(domain_session)
    assert len(accounts) == 2


def test_list_all_transfers(domain_session):
    insert_transfers(domain_session)
    transfers = list_transfers(domain_session)
    assert len(transfers) == 1
