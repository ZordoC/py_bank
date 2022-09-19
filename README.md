Python Banking App
==================

[![image](https://img.shields.io/pypi/v/py_bank.svg)](https://pypi.python.org/pypi/py_bank)

[![image](https://img.shields.io/travis/ZordoC/py_bank.svg)](https://travis-ci.com/ZordoC/py_bank)

[![Documentation Status](https://readthedocs.org/projects/py-bank/badge/?version=latest)](https://py-bank.readthedocs.io/en/latest/?version=latest)

Demo project for a bank app

# Definition

The software you will write in this test will be used for banks. `Banks` have accounts. `Accounts` hold
money. `Transfers` can be made between accounts. Banks store the history of transfers.
There can be two types of transfers:

- Intra-bank transfers, between accounts of the same bank. They don't have commissions, they
don't have limits and they always succeed.

- Inter-bank transfers, between accounts of different banks. They have 2,5€ commissions, they
have a limit of 2000€ per transfer. And they have a 33% chance of failure.

## Part 1

Build up a REST back-end application that may perform the following actions:
1. Method to query movements of local account.
        Method: GET
URI: `/account_id/list`
This end-point will send a formatted json with all account movements.

2. Method to perform an intra-bank transfer.
    Method: PUT
    URI: `/transfer`
    BODY: {
                “source” : “source_account_id”,
                “destination” : “destination_account_id”,
                “amount” : Quantity (Decimal),
                “info”: “Short string describing the purpose of the transfer”
        }

This operation will move money from one to another account, please consider cases were
account does not have funding, or any other kind of possible errors.

3. Method to add funds to the account.
    Method: PUT
    URI: /account_id/add
    BODY: {
    “amount” : Quantity (Decimal)
    “src_bank”: “source bank identifier”, (Optional in case the money comes from another
    bank)
    “info”: “Short string describing the purpose of the transfer”
    }
4. Method to remove funds from the account.
    Method: PUT
    URI: /account_id/retire
    BODY: {
    “amount”: Quantity (Decimal),
    “dst_bank”: “destination bank identifier”, (Optional in case the money goes to another
    bank)
    “info”: “Short string describing the purpose of the transfer”
}

-   Free software: MIT license
-   Documentation: <https://py-bank.readthedocs.io>.

Features
--------

-   TODO

Credits
-------

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
