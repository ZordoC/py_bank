"""Unit tests for ``py_bank.service_layer._services.add_funds``, some data has
been added to an in-memory SQLite3 database to run tests
``tests/conftest.py``"""
import random

import pytest

from py_bank.domain import Account, Deposit, Withdrawal
from py_bank.errors import InsuficientBalance
from py_bank.service_layer import execute_command


def test_deposit(domain_session):
    account = domain_session.query(Account).all()[-1]
    balance = account.balance
    amount = random.randrange(10, 100)

    execute_command(domain_session, Deposit(account, amount=amount))

    new_balance = domain_session.query(Account).filter_by(account_id=account.account_id).one().balance

    assert new_balance == balance + amount


def test_withdrawal(domain_session):
    account = domain_session.query(Account).all()[-1]
    balance = account.balance
    amount = random.randrange(10, 100)  # assumes an account balance > 100.

    execute_command(domain_session, Withdrawal(account, amount))

    new_balance = domain_session.query(Account).filter_by(account_id=account.account_id).one().balance

    assert new_balance == balance - amount


def test_withdrawal_account_insufficient_funds(domain_session):

    account = domain_session.query(Account).all()[-1]
    balance = account.balance
    amount = balance + 1

    with pytest.raises(InsuficientBalance):
        execute_command(domain_session, Withdrawal(account, amount))
