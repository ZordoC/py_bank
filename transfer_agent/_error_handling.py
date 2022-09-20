"""Error handling."""
import requests

from py_bank.service_layer import InsuficientBalance, AccountNotFound
from ._error import AgentError


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

    elif response.status_code == 403:
        raise AccountNotFound("Account was not found")

    elif response.status_code != 200:
        raise AgentError(
            f"Something is wrong with the response: \n {response.text},  code : {response.status_code}"
        )
