"""Unit tests for ``py_bank.service_layer._services.add_funds``, some data has
been added to an in-memory SQLite3 database to run tests
``tests/conftest.py``"""
import random

import pytest

from py_bank.domain import Account
from py_bank.service_layer import AccountNotFound, InsuficientBalance, remove_funds


def test_remove_fund_happy_path(domain_session):
    account = domain_session.query(Account).all()[-1]
    balance = account.balance
    amount = random.randrange(10, 100)  # assumes an account balance > 100.

    remove_funds(domain_session, account.account_id, amount)

    new_balance = (
        domain_session.query(Account).filter_by(account_id=account.account_id).one().balance
    )

    assert new_balance == balance - amount


def test_account_does_not_exist(domain_session):
    accounts = domain_session.query(Account).all()
    account_ids = [account.account_id for account in accounts]

    # assuming sequenitalliy (not that safe).
    non_existing_id = account_ids[-1] + 1

    if 1203424 not in account_ids:
        with pytest.raises(AccountNotFound):
            remove_funds(domain_session, non_existing_id, 42934)  # amount doesn't matter


def test_removing_over_balance(domain_session):
    account = domain_session.query(Account).all()[-1]
    balance = account.balance
    amount = balance + 1

    with pytest.raises(InsuficientBalance):
        remove_funds(domain_session, account.account_id, amount)
