"""``FakeAgent`` class module used for testing."""


from ._base import AbstractAgent
from ._agent import BANK_1_ID, BANK_2_ID



class FakeAgent(AbstractAgent):
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
        pass
