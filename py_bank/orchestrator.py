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

from py_bank.transfer_agent import (
    ACCOUNT_MAPPING,
    URL_1,
    URL_2,
    MAXIMUM_INTER_TRANSFER,
    AbstractAgent,
    RequestsAgent,
    InterTransferFailed,
)


def send_money_inter(agent: AbstractAgent, amount: float, sender: str, receiver: str, info: str):
    """Send money from one person to the other ()

    Args:
        agent (AbstractAgent): Any agent that follows the implementation.
    """
    if ACCOUNT_MAPPING[sender]["bank_id"] == ACCOUNT_MAPPING[receiver]["bank_id"]:
        raise ValueError("Same Bank ID")

    batches = int(amount / MAXIMUM_INTER_TRANSFER)

    total = batches * MAXIMUM_INTER_TRANSFER

    left = amount - total

    i = 0
    while i < batches:
        try:
            status_code = agent.inter_transfer(
                source_bank_id=ACCOUNT_MAPPING[sender]["bank_id"],
                dest_bank_id=ACCOUNT_MAPPING[receiver]["bank_id"],
                src_acc_id=ACCOUNT_MAPPING[sender]["acc_id"],
                dest_acc_id=ACCOUNT_MAPPING[receiver]["acc_id"],
                amount=MAXIMUM_INTER_TRANSFER,
                info= info,
                failure_chance=0
                
            )
            i += 1
        except InterTransferFailed:
            print("Failure ... retrying")
            pass
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
                    failure_chance=0
                )
            except InterTransferFailed:
                print("Failure ... retrying")
                sleep(1)
                continue


def send_money_intra(agent: AbstractAgent, amount: float, sender: str, receiver: str, info: str):
    """Send monkey within the same bank.

    Args:
        agent (AbstractAgent): _description_
        amount (float): _description_
        sender (str): _description_
        receiver (str): _description_
        bank_id (str): _description_
    """
    if ACCOUNT_MAPPING[sender]["bank_id"] != ACCOUNT_MAPPING[receiver]["bank_id"]:
        raise ValueError("Same Bank ID")

    bank_id = ACCOUNT_MAPPING[sender]["bank_id"]
    agent.intra_transfer(bank_id,ACCOUNT_MAPPING[sender]["acc_id"], ACCOUNT_MAPPING[receiver]["acc_id"], amount, info)

def _main():
    agent = RequestsAgent(URL_1, URL_2) # Applying DIP

    bank_1_accounts = agent.list_accounts("BANK1")
    bank_2_accounts = agent.list_accounts("BANK2")

    logging.basicConfig(format='%(levelname)s:  %(message)s', level=logging.INFO)


    logging.info("Starting payment pipeline")

    logging.info("Bank 1 accounts: %s", bank_1_accounts)
    logging.info("Bank 2 accounts: %s", bank_2_accounts)

    # Jimmy needs to  pay Emma 20000.
    send_money_inter(agent, 20000, "Jimmy", "Emma", "Sorry for the delay, Emma!" )
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

    logging.info("Bank 1 accounts: %s", bank_1_accounts)
    logging.info("Bank 2 accounts: %s", bank_2_accounts)



if __name__ == "__main__":
    _main()


# INFO:  Starting payment pipeline
# INFO:  Bank 1 accounts: Result [Account(account_owner='Luke', account_id=1, balance=1230.3), Account(account_owner='Jimmy', account_id=2, balance=500000.28), Account(account_owner='Steve', account_id=3, balance=25000.0)]
# INFO:  Bank 1 accounts: Result [Account(account_owner='Sarah', account_id=1, balance=1230.3), Account(account_owner='Emma', account_id=2, balance=2000.28)]
# INFO:  Emma received money from Jimmy.
# INFO:  Steve received money from Emma.
# INFO:  Sarah received money from Emma.
# INFO:  Pipeline Finished
# INFO:  Bank 1 accounts: Result [Account(account_owner='Luke', account_id=1, balance=1230.3), Account(account_owner='Jimmy', account_id=2, balance=480000.28), Account(account_owner='Steve', account_id=3, balance=27497.5)]
# INFO:  Bank 1 accounts: Result [Account(account_owner='Sarah', account_id=1, balance=4230.3), Account(account_owner='Emma', account_id=2, balance=16480.28)]