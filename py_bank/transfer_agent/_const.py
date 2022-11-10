"""Module for constants."""

URL_1 = "http://bank1:5001"
URL_2 = "http://bank2:5002"

BANK_1_ID = "BANK1"
BANK_2_ID = "BANK2"

MAXIMUM_INTER_TRANSFER = 2500
COMISSIONS = 2.5
FAILURE_CHANCE = 33

ACCOUNT_MAPPING = {
    "Luke": {"acc_id": 1, "bank_id": "BANK1"},
    "Jimmy": {"acc_id": 2, "bank_id": "BANK1"},
    "Steve": {"acc_id": 3, "bank_id": "BANK1"},
    "Emma": {"acc_id": 2, "bank_id": "BANK2"},
    "Sarah": {"acc_id": 1, "bank_id": "BANK2"},
}
