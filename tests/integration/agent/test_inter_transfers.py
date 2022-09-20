"""Module to test inter transfers using ``AbstractAgent`` class types."""
import pytest

from py_bank.service_layer import AccountNotFound, InsuficientBalance
from py_bank.transfer_agent import (
    InterTransferFailed,
    InvalidBankID,
    OverAllowedAmount,
    RequestsAgent,
)

ACCOUNT_MAPS = {
    "Luke": {"acc_id": 1, "bank_id": "BANK1"},
    "Jimmy": {"acc_id": 2, "bank_id": "BANK1"},
    "Steve": {"acc_id": 3, "bank_id": "BANK1"},
    "Emma": {"acc_id": 2, "bank_id": "BANK2"},
    "Sarah": {"acc_id": 1, "bank_id": "BANK2"},
}

URL_1 = "http://127.0.0.1:5001"
URL_2 = "http://127.0.0.1:5002"


def test_insuficient_balance():
    agent = RequestsAgent(URL_1, URL_2)

    print(agent.list_accounts("BANK2"))

    with pytest.raises(InsuficientBalance):
        agent.inter_transfer(
            source_bank_id=ACCOUNT_MAPS["Luke"]["bank_id"],
            dest_bank_id=ACCOUNT_MAPS["Jimmy"]["bank_id"],
            src_acc_id=ACCOUNT_MAPS["Luke"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPS["Jimmy"]["acc_id"],
            amount=2000,  # Sarah shouldn't have enough money ....
            info="Luke owes money to Jimmy",
            failure_chance=0,
        )


def test_account_not_found():
    agent = RequestsAgent(URL_1, URL_2)
    with pytest.raises(AccountNotFound):
        agent.inter_transfer(
            source_bank_id=ACCOUNT_MAPS["Jimmy"]["bank_id"],
            dest_bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
            src_acc_id=1000000,
            dest_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
            amount=2000,
            info="Jim owes too much money to Emma",
            failure_chance=0,
        )


def test_invalid_bank_id():
    agent = RequestsAgent(URL_1, URL_2)
    with pytest.raises(InvalidBankID):
        agent.inter_transfer(
            source_bank_id="BANK5",
            dest_bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
            src_acc_id=ACCOUNT_MAPS["Jimmy"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
            amount=2000,
            info="Jim owes too much money to Emma",
            failure_chance=0,
        )


def test_over_amount():
    agent = RequestsAgent(URL_1, URL_2)
    with pytest.raises(OverAllowedAmount):
        agent.inter_transfer(
            source_bank_id="BANK5",
            dest_bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
            src_acc_id=ACCOUNT_MAPS["Jimmy"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
            amount=3000,
            info="Jim owes too much money to Emma",
            failure_chance=0,
        )


def test_force_failure():
    agent = RequestsAgent(URL_1, URL_2)
    with pytest.raises(InterTransferFailed):
        agent.inter_transfer(
            source_bank_id="BANK5",
            dest_bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
            src_acc_id=ACCOUNT_MAPS["Jimmy"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
            amount=2000,
            info="Jim owes too much money to Emma",
            failure_chance=100,
        )
