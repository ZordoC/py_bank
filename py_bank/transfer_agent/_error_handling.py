"""Error handling."""
import requests

from py_bank.service_layer import AccountNotFound, InsuficientBalance

from ._const import BANK_1_ID, BANK_2_ID
from ._error import AgentError, InvalidBankID


def handle_reponses(response: requests.Response):
    """_summary_

    Args:
        response (_type_): _description_

    Raises:
        InsuficientBalance: _description_
        AccountNotFound: _description_
        AgentError: _description_
    """
    if response.status_code == 402:
        raise InsuficientBalance("Not enough balance to transfer")

    if response.status_code == 403:
        raise AccountNotFound("Account was not found")

    if response.status_code != 200:
        raise AgentError(f"Something is wrong with the response: \n {response.text},  code : {response.status_code}")


def check_bank_ids(source_bank_id: str, dest_bank_id: str):
    """Check for valid Bank Identifiers.

    Args:
        source_bank_id (str): Bank identifier of the source of transfer.
        dest_bank_id (str): Bank identifier of the destination of transfer.

    Raises:
        InvalidBankID: When passed an Invalid Bank ID.

    Returns:
        _type_: ``True`` if BANK_IDs are valid.
    """
    if source_bank_id not in (BANK_2_ID, BANK_1_ID) or dest_bank_id not in (BANK_2_ID, BANK_1_ID):
        raise InvalidBankID("Not a valid bank id")
    return True
