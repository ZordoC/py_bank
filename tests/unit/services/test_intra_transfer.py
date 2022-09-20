"""Unit tests for ``py_bank.service_layer._services.intra_money_transfer``,
some data has been added to an in-memory SQLite3 database to run tests
``tests/conftest.py``"""
import random

import pytest
from sqlalchemy import func

from py_bank.domain import Account, Transfer
from py_bank.service_layer import AccountNotFound, InsuficientBalance, intra_money_transfer


def test_successfull_intra_transfer(domain_session):
    source_id = 1
    dest_id = 2

    before_sender_balance = domain_session.query(Account).filter_by(account_id=source_id).one().balance

    # To make sure we are sending less money than sender has
    transfered_amount = before_sender_balance - random.randrange(
        10, 100
    )  # assumes that sender has some minimu amount of money (100 euros)

    before_dest_balance = domain_session.query(Account).filter_by(account_id=dest_id).one().balance

    intra_money_transfer(domain_session, source_id, dest_id, transfered_amount)

    after_sender_balance = domain_session.query(Account).filter_by(account_id=source_id).one().balance
    after_dest_balance = domain_session.query(Account).filter_by(account_id=dest_id).one().balance

    assert after_dest_balance - transfered_amount == before_dest_balance  # destination "gained" amount.
    assert after_sender_balance + transfered_amount == before_sender_balance  # sender "lost" amount.


def test_insufficient_balance_intra_transfer(domain_session):
    source_id = 1
    dest_id = 2
    before_sender_balance = domain_session.query(Account).filter_by(account_id=source_id).one().balance

    # To make sure we are sending more money than sender has
    transfered_amount = before_sender_balance + random.randrange(10, 100)  # random integer
    with pytest.raises(InsuficientBalance):
        intra_money_transfer(domain_session, source_id, dest_id, transfered_amount)


def test_sender_not_exist(domain_session):
    # Assuming account_ids are sequential and in order (big assumption, I know! but bear with me! :-))
    largest_id = domain_session.query(func.max(Account.account_id)).one()[0]

    source_id = largest_id + 1
    dest_id = largest_id - 1
    with pytest.raises(AccountNotFound):
        intra_money_transfer(
            domain_session, source_id, dest_id, 1000
        )  # amount doesn't matter because accoutns don't exist.


def test_dest_does_not_exist(domain_session):
    # Assuming account_ids are sequential and in order (big assumption, I know! but bear with me! :-))
    largest_id = domain_session.query(func.max(Account.account_id)).one()[0]

    dest_id = largest_id + 1
    source_id = largest_id - 1
    with pytest.raises(AccountNotFound):
        intra_money_transfer(
            domain_session, source_id, dest_id, 1000
        )  # amount doesn't matter because dest don't exist.


def test_intra_transfer_generated_transfer(domain_session):
    source_id = "1"
    dest_id = "2"

    before_sender_balance = domain_session.query(Account).filter_by(account_id=source_id).one().balance

    # To make sure we are sending less money than sender has
    transfered_amount = before_sender_balance - random.randrange(10, 100)  # random integer

    transfers_before = domain_session.query(Transfer).all()

    intra_money_transfer(domain_session, source_id, dest_id, transfered_amount)

    transfers_after = domain_session.query(Transfer).all()

    assert len(transfers_after) > len(transfers_before)

    assert transfers_after[-1].transfer_id > transfers_before[-1].transfer_id
