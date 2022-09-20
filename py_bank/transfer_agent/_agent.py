"""``RequestsAgent`` class module."""

import json
import random

import requests

from . import _error_handling as error_handling
from ._base import AbstractAgent
from ._const import BANK_1_ID, BANK_2_ID, COMMISSIONS, FAILURE_CHANCE, MAXIMUM_INTER_TRANSFER
from ._error import InterTransferFailed, InvalidBankID, OverAllowedAmount


class RequestsAgent(AbstractAgent):
    """Agent facilitates transfers between two distinct banks,"""

    def __init__(self, base_bank_1_url: str, base_bank_2_url: str):
        self.bank_1_url = base_bank_1_url
        self.bank_2_url = base_bank_2_url

        self.headers = {"Content-Type": "application/json"}

    def list_accounts(self, bank_id: str):
        base_url = self._get_url_from_bank_id(bank_id)

        response = requests.request("GET", f"{base_url}/list_accounts", headers=self.headers)

        return response.text

    def inter_transfer(
        self,
        source_bank_id: str,
        dest_bank_id: str,
        src_acc_id: int,
        dest_acc_id: int,
        amount: float,
        info: str,
        failure_chance: int = FAILURE_CHANCE,
    ):
        """Performs a transfer across banks.

        Args:
            source_bank_id (_type_): _description_
            src_id (int): _description_
            dest_id (int): _description_
            amount (float): _description_
        """
        if amount > MAXIMUM_INTER_TRANSFER:
            raise OverAllowedAmount(
                f"The allowed amount for inter transfers is {MAXIMUM_INTER_TRANSFER}. \nCurrent amount: {amount}"
            )
        chance = random.randint(1, 100)
        if chance <= failure_chance:
            raise InterTransferFailed(f"Transfer Failed ...")

        error_handling.check_bank_ids(source_bank_id, dest_bank_id)

        response = self._remove(source_bank_id, src_acc_id, amount, info)

        error_handling.handle_reponses(response)

        amount = amount - COMMISSIONS

        response = self._add(dest_bank_id, dest_acc_id, amount, info)

        error_handling.handle_reponses(response)

        return 200

    def intra_transfer(
        self, bank_id: str, src_acc_id: int, dest_acc_id: int, amount: float, info: str
    ):
        """_summary_

        Args:
            bank_id (str): _description_
            src_acc_id (int): _description_
            dest_acc_id (int): _description_
            amount (float): _description_
            info (str): _description_
        """

        base_url = self._get_url_from_bank_id(bank_id)

        url = f"{base_url}/transfer"

        payload = json.dumps(
            {"source": src_acc_id, "destination": dest_acc_id, "amount": amount, "info": info}
        )

        response = requests.request("POST", url, headers=self.headers, data=payload)

        return response

    def _check_bank_ids(source_bank_id: str, dest_bank_id: str):
        if source_bank_id != (BANK_2_ID, BANK_1_ID) or dest_bank_id not in (BANK_2_ID, BANK_1_ID):
            raise InvalidBankID("Not a valid bank id")
        return True

    def _add(self, bank_id: str, account_id: int, amount: float, info: str):
        """_summary_

        Args:
            account_id (int): _description_
            bank_id (str): _description_
            amount (float): _description_
            info (str): _description_
        """
        payload = json.dumps({"amount": amount, "src_bank": bank_id, "info": info})

        bank_url = self._get_url_from_bank_id(bank_id)

        response = requests.request(
            "PUT", f"{bank_url}/{account_id}/add", headers=self.headers, data=payload
        )
        return response

    def _remove(self, bank_id: str, account_id: int, amount: float, info: str):
        """_summary_

        Args:
            account_id (int): _description_
            dest_bank_id (str): _description_
            amount (float): _description_
            info (str): _description_
        """
        payload = json.dumps({"amount": amount, "dest_bank": bank_id, "info": info})

        bank_url = self._get_url_from_bank_id(bank_id)

        response = requests.request(
            "PUT", f"{bank_url}/{account_id}/retire", headers=self.headers, data=payload
        )
        return response

    def _get_url_from_bank_id(self, bank_id: str) -> str:
        """Get for bank api endpoint.

        Args:
            bank_id (str): _description_

        Returns:
            str: _description_
        """
        if bank_id == "BANK1":
            return self.bank_1_url
        elif bank_id == "BANK2":
            return self.bank_2_url
        else:
            raise InvalidBankID("Invalid bank ID when fetching URL.")
