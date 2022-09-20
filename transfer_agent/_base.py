"""Abstract class module for an ``Agent``"""
from abc import ABC, abstractmethod


class AbstractAgent(ABC):
    """Agent facilitates transfers between two distinct banks,"""

    @abstractmethod
    def inter_transfer(
        self,
        source_bank_id: str,
        dest_bank_id: str,
        src_acc_id: int,
        dest_acc_id: int,
        amount: float,
        info: str,
    ):
        """Performs a transfer across two distinct banks.

        Args:
            source_bank_id (_type_): _description_
            src_id (int): _description_
            dest_id (int): _description_
            amount (float): _description_
        """
        raise NotImplementedError("Interface does not have implementation")

    @abstractmethod
    def intra_transfer(
        self, bank_id: str, src_acc_id: int, dest_acc_id: int, amount: float, info: str
    ):
        """Peforms a transfer within the same bank.

        Args:
            bank_id (str): _description_
            src_acc_id (int): _description_
            dest_acc_id (int): _description_
            amount (float): _description_
            info (str): _description_
        """
        raise NotImplementedError("Interface does not have implementation")
