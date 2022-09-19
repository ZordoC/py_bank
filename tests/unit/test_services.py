"""Unit tests for ``py_bank.service_layer._services``"""

from py_bank.domain import Account, Transfer
from py_bank.service_layer import list_account_transfers


def insert_accounts(session):
    session.execute("INSERT INTO accounts (account_id, balance)" ' VALUES ("1AB", 1230.30)')
    session.execute("INSERT INTO accounts (account_id, balance)" ' VALUES ("2AB", 40102.28)')


def insert_transfers(session):
    session.execute("INSERT INTO transfers (order_id, balance)" ' VALUES ("1AB", 1230.30)')


def list_transfers(session):
    accounts = session.query(Transfer).all()
    return accounts


def list_accounts(session):
    accounts = session.query(Account).all()
    return accounts


def test_list_all_accounts(domain_session):
    insert_accounts(domain_session)
    accounts = list_accounts(domain_session)
    assert len(accounts) == 2
