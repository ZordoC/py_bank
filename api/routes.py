"""Routes for API."""
import os

from flask import request
from api import app

from py_bank.service_layer import (
    add_funds,
    create_transfer,
    list_account_transfers,
    intra_money_transfer,
    remove_funds,
    AccountNotFound,
    InsuficientBalance,
)


from py_bank.domain import Account

bank_id = os.environ.get("BANK_ID")


with app.app_context():
    from api.database import create_db_session, add_data_bank_2, add_data_bank_1
    db_session = create_db_session(bank_id)
    if bank_id == "BANK1":
        add_data_bank_1(db_session)
    elif bank_id == "BANK2":
        add_data_bank_2(db_session)



@app.route("/<account_id>/list", methods=["GET"])
def list_transfers(account_id: str):
    res = list_account_transfers(db_session, int(account_id))
    return res, 200


@app.route("/transfer", methods=["POST"])
def transfer():
    """Transfer money from account A to account B.

    Returns:
        str: Successfull or failed string + error code.
    """
    body = request.json
    try:
        intra_money_transfer(db_session, body["source"], body["destination"], body["amount"])
        return f"Successfully added funds from account {body['source']} to {body['destination']}", 200
    except InsuficientBalance:
        return "Unable to transfer due to insuficient balance", 402

    except AccountNotFound:
        return "Unable to transfer due to account not found", 403


@app.route("/<account_id>/add", methods=["PUT"])
def add(account_id):
    """Add money to an account.

    Returns:
        str: Successfull or failed string + error code.
    """
    body = request.json
    account_id = int(account_id)
    body = request.json
    try:
        add_funds(db_session, account_id, body["amount"])

        if body["src_bank"]:
            transfer = create_transfer(db_session, 0, account_id, body["amount"], info=body['info'], transfer_type="InterBank")
            db_session.add(transfer)
            db_session.commit()
            app.logger.info('%s Recorded Inter Transaction successfully.')

        return f"Successfully added funds to account {account_id}"
    except (AccountNotFound):
        return "Unable to add due to account not found", 403


@app.route("/<account_id>/retire", methods=["PUT"])
def remove(account_id):
    """Remove money from an account.

    Returns:
        str: Successfull or failed string + error code.
    """
    account_id = int(account_id)
    body = request.json

    try:
        remove_funds(db_session, account_id, body["amount"])
        if body['dest_bank']:
            transfer = create_transfer(db_session, account_id, 0, body["amount"], info=body['info'], transfer_type="InterBank")
            db_session.add(transfer)
            db_session.commit()
            app.logger.info('%s Recorded Inter Transaction successfully.')

        return f"Successfully removed funds to account {account_id}"

    except InsuficientBalance:
        return "Unable to remove capital due to insuficient balance", 402

    except AccountNotFound:
        return "Unable to remove capital due to account not found", 403


@app.route("/list_accounts", methods=["GET"])
def list_accounts():
    res = db_session.query(Account).all()
    return res, 200
