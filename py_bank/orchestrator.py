"""Playground script.

Jim has an account on the first bank and Emma has an account
on the second bank.

Jim owns Emma 20000€. Emma is already a bit angry, because she did not get the
money although Jim told her that he already sent it.

Now that Emma has received the money, please help her to pay her rent of 2500€ by issuing a transfer
to her landlord Steve who has an account at the first bank.

She also wants to send a transfer of 3000€ to
her sister Sara who has an account at the second bank.
"""
import logging
from time import sleep

from py_bank.errors import InterTransferFailed
from py_bank.transfer_agent import ACCOUNT_MAPPING, MAXIMUM_INTER_TRANSFER, URL_1, URL_2, AbstractAgent, RequestsAgent


def send_money_inter(agent: AbstractAgent, amount: float, sender: str, receiver: str, info: str = ""):
    """Send money from one person to the other ()

    Args:
        agent (AbstractAgent): Any transfer agent that follows the interface.
    """
    if ACCOUNT_MAPPING[sender]["bank_id"] == ACCOUNT_MAPPING[receiver]["bank_id"]:
        raise ValueError("Same Bank ID")

    batches = int(amount / MAXIMUM_INTER_TRANSFER)

    total = batches * MAXIMUM_INTER_TRANSFER

    left = amount - total

    i = 0
    while i < batches:
        try:
            _ = agent.inter_transfer(
                source_bank_id=str(ACCOUNT_MAPPING[sender]["bank_id"]),
                dest_bank_id=str(ACCOUNT_MAPPING[receiver]["bank_id"]),
                src_acc_id=int(ACCOUNT_MAPPING[sender]["acc_id"]),
                dest_acc_id=int(ACCOUNT_MAPPING[receiver]["acc_id"]),
                amount=MAXIMUM_INTER_TRANSFER,
                info=info,
            ).status_code
            i += 1
        except InterTransferFailed:
            logging.warning("Failure ... retrying")

    if left:
        status_code = 0
        while status_code != 200:
            try:
                status_code = agent.inter_transfer(
                    source_bank_id=ACCOUNT_MAPPING[sender]["bank_id"],
                    dest_bank_id=ACCOUNT_MAPPING[receiver]["bank_id"],
                    src_acc_id=ACCOUNT_MAPPING[sender]["acc_id"],
                    dest_acc_id=ACCOUNT_MAPPING[receiver]["acc_id"],
                    amount=left,
                    info=info,
                ).status_code
            except InterTransferFailed:
                logging.warning("Failure ... retrying")
                sleep(1)
                continue


def send_money_intra(agent: AbstractAgent, amount: float, sender: str, receiver: str, info: str = ""):
    """Send monkey within the same bank.

    Args:
        agent (AbstractAgent): Any transfer agent that follows the interface.
        amount (float): Money to be sent
        sender (str): Sender Name.
        receiver (str): Receiver name.
        bank_id (str): Bank Identifier.
    """
    if ACCOUNT_MAPPING[sender]["bank_id"] != ACCOUNT_MAPPING[receiver]["bank_id"]:
        raise ValueError("Different Bank ID")

    bank_id = ACCOUNT_MAPPING[sender]["bank_id"]
    agent.intra_transfer(
        bank_id,
        ACCOUNT_MAPPING[sender]["acc_id"],
        ACCOUNT_MAPPING[receiver]["acc_id"],
        amount,
        info,
    )


def _main():  # pragma: no cover

    agent = RequestsAgent(URL_1, URL_2)  # Applying DIP

    bank_1_accounts = agent.list_accounts("BANK1")
    bank_2_accounts = agent.list_accounts("BANK2")

    logging.basicConfig(format="%(levelname)s:  %(message)s", level=logging.INFO)

    logging.info("Starting payment pipeline")

    logging.info("Bank 1 accounts: %s", bank_1_accounts.json())
    logging.info("Bank 2 accounts: %s", bank_2_accounts.json())

    # Jimmy needs to  pay Emma 20000.
    send_money_inter(agent, 20000, "Jimmy", "Emma", "Sorry for the delay, Emma!")
    logging.info("Emma received money from Jimmy.")
    # Emma pays rent to her Landlord Steve.
    send_money_inter(agent, 2500, "Emma", "Steve", "September's Rent")
    logging.info("Steve received money from Emma.")
    # Emma sends money to her sister Sarah
    send_money_intra(agent, 3000, "Emma", "Sarah", "Money for my sister!")
    logging.info("Sarah received money from Emma.")

    logging.info("Pipeline Finished")

    bank_1_accounts = agent.list_accounts("BANK1")
    bank_2_accounts = agent.list_accounts("BANK2")

    logging.info("Bank 1 accounts: %s", bank_1_accounts.json())
    logging.info("Bank 2 accounts: %s", bank_2_accounts.json())

    logging.info("\n \n ### Listing Transfers of accounts involved  ###")
    logging.info(
        "Jimmy: %s \n \n",
        agent.list_transfers(ACCOUNT_MAPPING["Jimmy"]["bank_id"], ACCOUNT_MAPPING["Jimmy"]["acc_id"]).json(),
    )
    logging.info(
        "Emma: %s \n \n",
        agent.list_transfers(ACCOUNT_MAPPING["Emma"]["bank_id"], ACCOUNT_MAPPING["Emma"]["acc_id"]).json(),
    )
    logging.info(
        "Steve: %s \n \n",
        agent.list_transfers(ACCOUNT_MAPPING["Steve"]["bank_id"], ACCOUNT_MAPPING["Steve"]["acc_id"]).json(),
    )
    logging.info(
        "Sarah: %s \n \n",
        agent.list_transfers(ACCOUNT_MAPPING["Sarah"]["bank_id"], ACCOUNT_MAPPING["Sarah"]["acc_id"]).json(),
    )


if __name__ == "__main__":
    _main()  # pragma: no cover
