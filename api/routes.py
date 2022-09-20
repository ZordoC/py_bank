"""Routes for API."""
from flask import request
from api import app, FLAG

from py_bank.service_layer import (
    add_funds,
    list_account_transfers,
    intra_money_transfer,
    remove_funds,
    AccountNotFound,
    InsuficientBalance,
)

from transfer_agent import RequestsAgent


with app.app_context():
    from py_bank.service_layer import create_db_session, add_data_bank_2, add_data_bank_1
    db_session = create_db_session(FLAG)

    if FLAG == "BANK1":
        add_data_bank_1(db_session)
    elif FLAG == "BANK2":
        add_data_bank_2(db_session)


agent  = RequestsAgent("1", "2")


@app.route("/<account_id>/list", methods=["GET"])
def list_transfers(account_id: str):
    res = list_account_transfers(db_session, int(account_id))
    return f"Result {res}"


@app.route("/transfer", methods=["POST"])
def transfer():
    """Transfer money from account A to account B.

    Returns:
        str: Successfull or failed string + error code.
    """
    body = request.json
    try:
        intra_money_transfer(db_session, body["source"], body["destination"], body["amount"])
        return f"Successfully added funds from account {body['source']} to {body['destination']}"
    except InsuficientBalance:
        return "Unable to transfer due to insuficient balance", 404

    except AccountNotFound:
        return "Unable to transfer due to account not found", 404


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
        return f"Successfully added funds to account {account_id}"
    except (AccountNotFound):
        return "Unable to add due to account not found", 404


@app.route("/<account_id>/retire", methods=["PUT"])
def remove(account_id):
    """Remove money from an account.

    Returns:
        str: Successfull or failed string + error code.
    """
    account_id = int(account_id)
    body = request.json
    if body.dest_bank:
        # agent queries adds amount to other bank
        pass

    try:
        remove_funds(db_session, account_id, body["amount"])
        return f"Successfully removed funds to account {account_id}"

    except InsuficientBalance:
        return "Unable to remove capital due to insuficient balance", 404

    except AccountNotFound:
        return "Unable to remove capital due to account not found", 404
