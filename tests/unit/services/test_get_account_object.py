"""Unit tests for ``py_bank.service_layer._services.create_account_from_id``,
some data has been added to an in-memory SQLite3 database to run tests
``tests/conftest.py``"""
import random

import pytest

from py_bank.domain import Account, Deposit
from py_bank.errors import AccountNotFound
from py_bank.service_layer import get_account_from_id


def test_account_exists(domain_session):
    """Test when account exists."""
    account_id = 1
    account = get_account_from_id(domain_session, 1)

    assert account.account_owner == "Jimmy"


def test_account_not_exists(domain_session):
    """Test when account does not exist."""
    account_id = 99999
    with pytest.raises(AccountNotFound):
        account = get_account_from_id(domain_session, account_id)
