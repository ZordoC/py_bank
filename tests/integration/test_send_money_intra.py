"""Testing module for ``py_bank/orchestrator.send_money_intra``"""
import pytest

from py_bank.orchestrator import send_money_intra
from py_bank.transfer_agent import ACCOUNT_MAPPING


def test_intra_same_bank(agent):

    jimmy_transfers = agent.list_transfers(
        ACCOUNT_MAPPING["Jimmy"]["bank_id"], ACCOUNT_MAPPING["Jimmy"]["acc_id"]
    ).json()

    send_money_intra(agent, 20, "Luke", "Jimmy", "Integration testing")

    assert len(
        agent.list_transfers(ACCOUNT_MAPPING["Jimmy"]["bank_id"], ACCOUNT_MAPPING["Jimmy"]["acc_id"]).json()
    ) > len(jimmy_transfers)


def test_intra_different_bank(agent):

    with pytest.raises(ValueError):
        send_money_intra(agent, 3000, "Jimmy", "Emma", "Integration testing")
