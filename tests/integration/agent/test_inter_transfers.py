"""Module to test inter transfers using ``AbstractAgent`` class types."""
import pytest

from py_bank.errors import AccountNotFound, InsuficientBalance, InterTransferFailed, InvalidBankID, OverAllowedAmount
from py_bank.transfer_agent import ACCOUNT_MAPPING


def test_insuficient_balance(agent):

    with pytest.raises(InsuficientBalance):
        agent.inter_transfer(
            source_bank_id=ACCOUNT_MAPPING["Luke"]["bank_id"],
            dest_bank_id=ACCOUNT_MAPPING["Jimmy"]["bank_id"],
            src_acc_id=ACCOUNT_MAPPING["Luke"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPPING["Jimmy"]["acc_id"],
            amount=2400,  # Luke shouldn't have enough money ....
            info="Luke owes money to Jimmy",
            failure_chance=0,
        )


def test_account_not_found(agent):
    with pytest.raises(AccountNotFound):
        agent.inter_transfer(
            source_bank_id=ACCOUNT_MAPPING["Jimmy"]["bank_id"],
            dest_bank_id=ACCOUNT_MAPPING["Emma"]["bank_id"],
            src_acc_id=1000000,
            dest_acc_id=ACCOUNT_MAPPING["Emma"]["acc_id"],
            amount=2000,
            info="Jim owes too much money to Emma",
            failure_chance=0,
        )


def test_invalid_bank_id(agent):
    with pytest.raises(InvalidBankID):
        agent.inter_transfer(
            source_bank_id="BANK5",
            dest_bank_id=ACCOUNT_MAPPING["Emma"]["bank_id"],
            src_acc_id=ACCOUNT_MAPPING["Jimmy"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPPING["Emma"]["acc_id"],
            amount=2000,
            info="Jim owes too much money to Emma",
            failure_chance=0,
        )


def test_over_amount(agent):
    with pytest.raises(OverAllowedAmount):
        agent.inter_transfer(
            source_bank_id="BANK5",
            dest_bank_id=ACCOUNT_MAPPING["Emma"]["bank_id"],
            src_acc_id=ACCOUNT_MAPPING["Jimmy"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPPING["Emma"]["acc_id"],
            amount=3000,
            info="Jim owes too much money to Emma",
            failure_chance=0,
        )


def test_force_failure(agent):
    with pytest.raises(InterTransferFailed):
        agent.inter_transfer(
            source_bank_id="BANK5",
            dest_bank_id=ACCOUNT_MAPPING["Emma"]["bank_id"],
            src_acc_id=ACCOUNT_MAPPING["Jimmy"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPPING["Emma"]["acc_id"],
            amount=2000,
            info="Jim owes too much money to Emma",
            failure_chance=100,
        )
