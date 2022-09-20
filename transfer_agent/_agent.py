"""``RequestsAgent`` class module"""
import json

import requests

from ._base import AbstractAgent


BANK_1_ID = "1"
BANK_2_ID = "2"


class RequestsAgent(AbstractAgent):
    """Agent facilitates transfers between two distinct banks,
    """
    def __init__(self, base_bank_1_url: str, base_bank_2_url: str):
        self.bank_1_url = base_bank_1_url
        self.bank_2_url = base_bank_2_url

        self.headers = {"Content-Type": "application/json"}

    def inter_transfer(self, source_bank_id: str , dest_bank_id: str,  src_acc_id: int, dest_acc_id: int, amount: float, info: str):
        """_summary_

        Args:
            source_bank_id (_type_): _description_
            src_id (int): _description_
            dest_id (int): _description_
            amount (float): _description_
        """
        self._check_bank_ids(source_bank_id, dest_bank_id)

        self.remove(dest_bank_id, src_acc_id, amount, info)

        self.add(source_bank_id,  dest_acc_id,  amount, info)



    @staticmethod
    def _check_bank_ids(source_bank_id: str, dest_bank_id: str):
        if source_bank_id != BANK_1_ID or dest_bank_id != BANK_2_ID:
            raise InvalidBankID("Not a valid bank id")
        return True
            

    def add(self,  src_bank_id: str, account_id: int, amount: float, info: str):
        """_summary_

        Args:
            account_id (int): _description_
            src_bank_id (str): _description_
            amount (float): _description_
            info (str): _description_
        """
        payload = json.dumps({"amount": amount, "src_bank": src_bank_id, "info": info})

        bank_url = self._get_url_from_bank_id(src_bank_id)

        response = requests.request(
            "PUT", f"{bank_url}/{account_id}/add", headers=self.headers, data=payload
        )

    def remove(self, dest_bank_id: str,  account_id: int , amount: float, info: str):
        """_summary_

        Args:
            account_id (int): _description_
            dest_bank_id (str): _description_
            amount (float): _description_
            info (str): _description_
        """
        payload = json.dumps({"amount": amount, "src_bank": dest_bank_id, "info": info})

        bank_url = self._get_url_from_bank_id(dest_bank_id)

        response = requests.request(
            "PUT", f"{bank_url}/{account_id}/retire", headers=self.headers, data=payload
        )

    def _get_url_from_bank_id(self, bank_id: str) -> str:
        """Get for bank api endpoint.

        Args:
            bank_id (str): _description_

        Returns:
            str: _description_
        """
        if bank_id == "1":
            return self.bank_1_url
        elif bank_id == "2":
            return self.bank_2_url


class InvalidBankID(ValueError):
    """Raised when invalid bank ID."""