"""Module to test inter transfers using ``AbstractAgent`` class types."""
import pytest 
from transfer_agent import RequestsAgent, InvalidBankID

from py_bank.service_layer import InsuficientBalance, AccountNotFound


ACCOUNT_MAPS = {
    "Jimmy": {"acc_id": 2, "bank_id": "BANK1"},
    "Landlord": {"acc_id": 3, "bank_id": "BANK2"},
    "Emma": {"acc_id": 2, "bank_id": "BANK2"},
    "Sarah": {"acc_id": 1, "bank_id": "BANK2"},
}


def test_happy_path_transfer():

    URL_1 = "http://127.0.0.1:5001"
    URL_2 = "http://127.0.0.1:5002"

    agent = RequestsAgent(URL_1, URL_2)

    # From Jimmy (bank1 - account_id = 1) to Emma (bank2 - account_id = 2) -> inter
    status_code = agent.inter_transfer(
        source_bank_id=ACCOUNT_MAPS["Jimmy"]["bank_id"],
        dest_bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
        src_acc_id=ACCOUNT_MAPS["Jimmy"]["acc_id"],
        dest_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
        amount=20000,
        info="Jim owes money to Emma",
    )
    assert status_code == 200

    agent._add("BANK2", "2", 400, "Testing")

    # From Emma (bank2 - account_id = 2) to Landlord (bank2 - account_id = 1) -> intra
    response = agent.intra_transfer(
        bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
        src_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
        dest_acc_id=ACCOUNT_MAPS["Landlord"]["acc_id"],
        amount=2500,
        info="September's Rent",
    )
    assert response.status_code == 200
    assert (
        response.text
        == f"Successfully added funds from account {ACCOUNT_MAPS['Emma']['acc_id']} to {ACCOUNT_MAPS['Landlord']['acc_id']}"
    )

    # From Emma (bank2 - account_id = 2) to Sister (bank2 - account_id = 3) -> intra
    response = agent.intra_transfer(
        bank_id="BANK2",
        src_acc_id=ACCOUNT_MAPS['Emma']['acc_id'],
        dest_acc_id=ACCOUNT_MAPS['Sarah']['acc_id'],
        amount=3000,
        info="Lending money to my sister.",
    )

    assert (
        response.text
        == f"Successfully added funds from account {ACCOUNT_MAPS['Emma']['acc_id']} to {ACCOUNT_MAPS['Sarah']['acc_id']}"
    )

    assert response.status_code == 200


def test_sad_path():
    URL_1 = "http://127.0.0.1:5001"
    URL_2 = "http://127.0.0.1:5002"

    agent = RequestsAgent(URL_1, URL_2)

    # From Jimmy (bank1 - account_id = 1) to Emma (bank2 - account_id = 2) -> inter
    with pytest.raises(InsuficientBalance):
        agent.inter_transfer(
            source_bank_id=ACCOUNT_MAPS["Jimmy"]["bank_id"],
            dest_bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
            src_acc_id=ACCOUNT_MAPS["Jimmy"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
            amount=40000000000, # Jimmy does not have enough money for this ...
            info="Jim owes too much money to Emma",
        )

    with pytest.raises(AccountNotFound):
        agent.inter_transfer(
            source_bank_id=ACCOUNT_MAPS["Jimmy"]["bank_id"],
            dest_bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
            src_acc_id=1000000,
            dest_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
            amount=400000,
            info="Jim owes too much money to Emma",
        )
    
    with pytest.raises(InvalidBankID):
        agent.inter_transfer(
            source_bank_id="BANK5",
            dest_bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
            src_acc_id=ACCOUNT_MAPS["Jimmy"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
            amount=400000,
            info="Jim owes too much money to Emma",
        )
    