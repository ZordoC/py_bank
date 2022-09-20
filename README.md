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

## Part 2

Create an initial system consisting of two banks with at least two different accounts each. Consider
each bank a separate invocation of your back-end application listening at a different port and using a
separate database.

Now, let’s start the fun part of the test. Jim has an account on the first bank and Emma has an account
on the second bank. Jim owns Emma 20000€. Emma is already a bit angry, because she did not get the
money although Jim told her that he already sent it.

Help Jim send his money by developing a transfer agent. You have to build up a transfer agent client
application that will consume your API, and perform transfers between those two banks.
This agent assures that everybody gets their money. When the agent receives an order to transfer money
from account A to account B, he issues transfers considering commissions, transfer limits and
possibility of transfer failures.

Now that Emma has received the money, please help her to pay her rent of 2500€ by issuing a transfer
to her landlord Steve who has an account at the first bank. She also wants to send a transfer of 3000€ to
her sister Sara who has an account at the second bank.


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
