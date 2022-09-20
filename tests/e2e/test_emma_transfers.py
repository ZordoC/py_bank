"""Module to test inter transfers using ``AbstractAgent`` class types."""
from py_bank.transfer_agent import RequestsAgent

ACCOUNT_MAPS = {
    "Luke": {"acc_id": 1, "bank_id": "BANK1"},
    "Jimmy": {"acc_id": 2, "bank_id": "BANK1"},
    "Steve": {"acc_id": 3, "bank_id": "BANK1"},
    "Emma": {"acc_id": 2, "bank_id": "BANK2"},
    "Sarah": {"acc_id": 1, "bank_id": "BANK2"},
}

URL_1 = "http://127.0.0.1:5001"
URL_2 = "http://127.0.0.1:5002"


def test_happy_path_transfer():

    agent = RequestsAgent(URL_1, URL_2)

    # Jimmy's debts
    i = 0
    while i < 10:
        status_code = agent.inter_transfer(
            source_bank_id=ACCOUNT_MAPS["Jimmy"]["bank_id"],
            dest_bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
            src_acc_id=ACCOUNT_MAPS["Jimmy"]["acc_id"],
            dest_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
            amount=2000,
            info="Jim owes money to Emma",
            failure_chance=0,
        )
        assert status_code == 200
        i = i + 1

    # Emma Paying Rent
    status_code = agent.inter_transfer(
        source_bank_id=ACCOUNT_MAPS["Emma"]["bank_id"],
        dest_bank_id=ACCOUNT_MAPS["Steve"]["bank_id"],
        src_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
        dest_acc_id=ACCOUNT_MAPS["Steve"]["acc_id"],
        amount=2500,
        info="September's Rent",
        failure_chance=0,
    )
    assert status_code == 200

    # Emma sending money to her sister
    response = agent.intra_transfer(
        bank_id="BANK2",
        src_acc_id=ACCOUNT_MAPS["Emma"]["acc_id"],
        dest_acc_id=ACCOUNT_MAPS["Sarah"]["acc_id"],
        amount=3000,
        info="Lending money to my sister.",
    )
    assert (
        response.text
        == f"Successfully added funds from account {ACCOUNT_MAPS['Emma']['acc_id']} to {ACCOUNT_MAPS['Sarah']['acc_id']}"
    )
    assert response.status_code == 200
