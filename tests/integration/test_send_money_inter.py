"""Testing module for ``py_bank/orchestrator.send_money_inter``"""
import pytest

from py_bank.orchestrator import send_money_inter
from py_bank.service_layer import create_transfer
from py_bank.transfer_agent import ACCOUNT_MAPPING


def test_inter_different_even_bank_batches(agent):
    jimmy_transfers = agent.list_transfers(
        ACCOUNT_MAPPING["Jimmy"]["bank_id"], ACCOUNT_MAPPING["Jimmy"]["acc_id"]
    ).json()

    send_money_inter(agent, 10000, "Jimmy", "Sarah", "Across different Banks")
    updated_jimmy_transfers = agent.list_transfers(
        ACCOUNT_MAPPING["Jimmy"]["bank_id"], ACCOUNT_MAPPING["Jimmy"]["acc_id"]
    ).json()

    difference = len(updated_jimmy_transfers) - len(jimmy_transfers)

    assert difference > 2
    print(updated_jimmy_transfers[-1])
    # even batches, means that last batch is not a "remainder" (smaller than normal batches due to division)
    assert updated_jimmy_transfers[-1]["amount"] == updated_jimmy_transfers[-2]["amount"]


def test_inter_different_uneven_bank_batches(agent):
    jimmy_transfers = agent.list_transfers(
        ACCOUNT_MAPPING["Jimmy"]["bank_id"], ACCOUNT_MAPPING["Jimmy"]["acc_id"]
    ).json()

    send_money_inter(agent, 11000, "Jimmy", "Sarah", "Across different Banks")

    updated_jimmy_transfers = agent.list_transfers(
        ACCOUNT_MAPPING["Jimmy"]["bank_id"], ACCOUNT_MAPPING["Jimmy"]["acc_id"]
    ).json()

    difference = len(updated_jimmy_transfers) - len(jimmy_transfers)

    assert difference > 2

    assert updated_jimmy_transfers[-1]["amount"] != updated_jimmy_transfers[-2]["amount"]


def test_inter_different_bank(agent):

    with pytest.raises(ValueError):
        send_money_inter(agent, 2400, "Jimmy", "Luke", "Across different Banks")
