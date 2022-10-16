
Python Banking App

==================



[![image](https://img.shields.io/pypi/v/py_bank.svg)](https://pypi.python.org/pypi/py_bank)



[![image](https://img.shields.io/travis/ZordoC/py_bank.svg)](https://travis-ci.com/ZordoC/py_bank)



[![Documentation Status](https://readthedocs.org/projects/py-bank/badge/?version=latest)](https://py-bank.readthedocs.io/en/latest/?version=latest)



Demo project for a bank app.


# TLDR; Quick start (inside docker container)

Set-up both bank apps.

	make start-banks

Run tests and check coverage.

	make cov

Run transfers

	python -m py_bank.orchestrator

Review results in [Application] section!

# Definition

The software you will write in this test will be used for banks. `Banks` have accounts. `Accounts` hold

money. `Transfers` can be made between accounts. Banks store the history of transfers.

There can be two types of transfers:

- Intra-bank transfers, between accounts of the same bank. They don't have commissions, they
don't have limits and they always succeed.



- Inter-bank transfers, between accounts of different banks. They have 2,5€ commissions, they
have a limit of 2000€ per transfer. And they have a 33% chance of failure.


## Part 1



**REST back-end** application as the following actions:

1. Method to query movements of local account.

    **Method: GET**

    **URI**: `/account_id/list`

This end-point will send a formatted json with all account movements.


2. Method to perform an intra-bank transfer.

    Method: PUT

    **URI**: `/transfer`

    **BODY**: {
    “source” : “source_account_id”,
    “destination” : “destination_account_id”,
    “amount” : Quantity (Decimal),
    “info”: “Short string describing the purpose of the transfer”
    }

This operation will move money from one to another account, please consider cases were
account **does not have funding, or any other kind of possible errors.**



3. Method to add funds to the account.

    **Method**: PUT
    URI: /account_id/add
    BODY: {
    “amount” : Quantity (Decimal)
    “src_bank”: “source bank identifier”, (Optional in case the money comes from another
    bank)
    “info”: “Short string describing the purpose of the transfer”
    }

4. Method to remove funds from the account.

    **Method: PUT**

    **URI**: /account_id/retire

    **BODY**: {
    “amount”: Quantity (Decimal),
    “dst_bank”: “destination bank identifier”, (Optional in case the money goes to another
    bank)
    “info”: “Short string describing the purpose of the transfer”
    }



## Part 2

Create an initial system consisting of two banks with at least two different accounts each. Consider
each bank a separate invocation of your back-end application listening at a different port and using a
separate database.


Now, let’s start the fun part of the test. **Jim has an account on the first bank** and **Emma has an account
on the second bank. Jim owns Emma 20000€.** Emma is already a bit angry, because she did not get the
money although Jim told her that he already sent it.



Help Jim send his money by developing a transfer agent. You have to build up a transfer agent client
application that will consume your API, and perform transfers between those two banks.

This agent assures that everybody gets their money. When the agent receives an order to transfer money
from account A to account B, he issues transfers considering commissions, transfer limits and
possibility of transfer failures.


Now that Emma has received the money, please help her to pay her rent of 2500€ by issuing a transfer
to her landlord Steve who has an account at the first bank. She also wants to send a transfer of 3000€ to
her sister Sara who has an account at the second bank.

# Architecure

I try to follow KISS and SOLID approaches (not dogmatically though). For the overall architecture when it comes to data layer I take great inspiration in https://www.cosmicpython.com/book/preface.html, (free e-book) https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/ (hardcover) which was one of the firsts book I read when I transitioned from Data Science to Development. And I also use my own cookie-cutter (derived from another project).

	├── Makefile
	├── README.md
	├── api
	│   ├── __init__.py
	│   ├── __pycache__
	│   │   ├── __init__.cpython-38.pyc
	│   │   ├── config.cpython-38.pyc
	│   │   ├── database.cpython-38.pyc
	│   │   └── routes.cpython-38.pyc
	│   ├── config.py
	│   ├── database.py
	│   └── routes.py
	├── docker
	│   ├── Dockerfile.api
	│   └── Dockerfile.dev
	├── flask_api.py
	├── py_bank
	│   ├── __init__.py
	│   ├── domain
	│   │   ├── __init__.py
	│   │   └── _models.py
	│   ├── errors.py
	│   ├── orchestrator.py
	│   ├── service_layer
	│   │   ├── __init__.py
	│   │   ├── _orm.py
	│   │   └── _services.py
	│   └── transfer_agent
	│       ├── __init__.py
	│       ├── _agent.py
	│       ├── _base.py
	│       ├── _const.py
	│       └── _error_handling.py
	├── requirements.txt
	├── requirements_dev.txt
	├── setup.cfg
	├── setup.py
	├── start_banks_docker.sh
	├── start_banks_local.sh
	├── stop_banks_local.sh

	└── tests
	    ├── __init__.py
	    ├── conftest.py
	    ├── e2e
	    │   ├── __init__.py
	    │   └── test_emma_transfers.py
	    ├── integration
	    │   ├── __init__.py
	    │   ├── agent
	    │   │   ├── __init__.py
	    │   │   └── test_inter_transfers.py
	    │   ├── conftest.py
	    │   ├── test_send_money_inter.py
	    │   └── test_send_money_intra.py
	    ├── test_py_bank.py
	    └── unit
	        ├── __init__.py
	        └── services
	            ├── __init__.py
	            ├── test_add_funds.py
	            ├── test_create_transfer.py
	            ├── test_intra_transfer.py
	            ├── test_listr_transfers_account.py
	            └── test_remove_funds.py


The application is separated in a python package `py_bank` that contains logic used by the `api` . This way you don't need to fire up the API everytime you want to test your application. The API is only used as a wrapper for all the services that do the heavy work.

You can install it as a package (without the flask api)

	make install

And create a dist file:

	make dist

Or build:

	make build

The way I structure modules is very inspired in SKlearn design a module: https://github.com/scikit-learn/scikit-learn/tree/main/sklearn/compose

I basically pre-append with `_` all files in a module and consider them privately. If i need any asset I expose it from the `__init__.py` ,

## Service Layer


I use the ORM from SQLAlchemy in a bit of different way than usual -> https://www.cosmicpython.com/book/chapter_02_repository.html#_the_normal_orm_way_model_depends_on_orm

By applying DIP.
https://www.cosmicpython.com/book/chapter_02_repository.html#_inverting_the_dependency_orm_depends_on_model

> The end result will be that, if we call `start_mappers`, we will be able to easily load and save domain model instances from and to the database. But if we never call that function, our domain model classes stay blissfully unaware of the database.

I't s good way of having a more "independent" domain model. The other way around would also work just fine, I just learnt to do it this way in my previous experiences.

The service layer is where we find methods such as

`list_account_transfers`
`intra_money_transfer`
`add_funds`
`remove_funds`

I've organized them in functions but we are one step away from the Repository Pattern  https://www.youtube.com/watch?v=iO83BDj-Ju4&t=202s (shameless self-promoting :-) ).

However ....

> Don't Use a Hammer When You Only Need a Screw driver

So for now it's good enough!


## Domain

My system assumes that `Transfers` are stored in order and will have an unique identifier.

Our domain models are pretty simple (too much ...)

Just consists:

	@dataclass
	class  Account:
	"""Model for an Account."""
		account_owner: str
		account_id: int

		balance: float

	@dataclass()
	class  Transfer:
	"""Model for a Transfer."""
		transfer_id: int
		amount: float
		transfer_type: Literal["IntraBank", "InterBank"]
		src_account_id: int
		dest_account_id: int
		info: str = "Test"

Basically each database corresponds to a different bank. And each Bank as an `Account` and `Transfer` Tables. Very simple, but if we want to expand in the future it should be easy. (We can also add some methods to enhance development experience if necessary).

## Agent

I've created an abstract class for `Agent`

	class  AbstractAgent(ABC):
		"""Agent facilitates transfers between two distinct banks,"""
		@abstractmethod
		def  inter_transfer(self, source_bank_id: str,	dest_bank_id: str,	src_acc_id: int,	dest_acc_id: int, amount: float, info: str, failure_chance: int)
		):

		@abstractmethod
		def  intra_transfer(self, bank_id: str, src_acc_id: int, dest_acc_id: int, amount: float, info: str):

This will take care of handling transfers, the idea was to follow "Don't depend on implementations but rather abstractions", and although we only have one other `Agent`, `RequestsAgent` . However let's imagine we now switch to an async API with an Async DB engine? Client code doesn't need to change (`orchestrator.py`) , all we need to do is create an `AsyncAgent`

	def  _main():

	agent = RequestsAgent(URL_1, URL_2) # Applying DIP
	new_agent = AsyncAgent(URL_1, URL2) # or whatever necesary to the init
	.
	.
	.
	send_money_inter(agent, 2500, "Emma", "Steve", "September's Rent")

Function depends on the abstraction.

	def send_money_inter(agent: AbstractAgent, amount: float, sender: str, receiver: str, info: str):
	.
	.

In orchestrator I have other methods list_accounts and list_transfers, we could add them to the interface but honestly they shouldn't be there, they are there only to showcase the results of the task.

## Errors

All custom exception are stored in `py_bank.errors` such as `InsuficientBalance` `InvalidBankID` , to facilitate our lives. These exceptions are all raised at some point and they also have their own test cases.

## API

Finally the API is something very very simple, just a Flask wrapper and some ugly utilities to load the proper databases on start-up! We could use some tests for the API, we have a strong suite of unit and integration tests, this would be my next effort!!

# Instalation and setup

## Devcontainer
I've developed this small application inside a docker container using VSCode, so I recommend the same thing. The image is provided in the `docker/` folder, properly named `Dockerfile.dev`. (to be used in a dev container VScode). As soon as you open the project locally `.vscodesettings/docker` should offer you to open it in a container, otherwise you can manually open it via the command pallete.

## Dependencies

There are two requirements files, one for linting, and formatting tools (requirements_dev.txt) and one for the application itself (requirements.txt).
If you're in a docker container they should be installed by default. Otherwise:

	python -m venv .venv
	. .venv/bin/activate
	pip install -r requirements_dev.txt
	pip install -r requirements.txt

Also `python version` => 3.8

Sometimes to `git pull` when first inside the container we need to change the SSL backend (manually).

	apt-get install nano
	nano ~/.gitconfig

Change sslBackend to `gnutls`


## Setup

Now that we have all dependencies installed.  We can run our `main` program that does what's described in  Part 2. (Note: if you want to have pre-commit hooks enabled you need to type `pre-commit install` this comes quite in handy, for more info about the different stages look at the `pre-commit.yaml` file.

Now we need to launch our "two" banks.

They are two instances of the backend controlled by an environment variable `BANK_ID`, to facilitate this we have an helper bash script `start_bank_local.sh` or we can invoke a make command :`make start-bank` .
(launches the apps locally in the background),
In your first time you may get an error while trying to delete previous db files, but you can ignore them. and the app should launch if you're using bash shell. (inside dockerdev).

Check: `bank_logs_1.rpt` and `bank_logs_2.rpt` in order to see if everything launched without any issues.


# Application

Now we can finally run what was asked in Task 2. By invoking the following client code.

	python -m py_bank.orchestrator

(maybe `client `would be a better name :-) )

You should see the following output.

	NFO:  Starting payment pipeline
	INFO:  Bank 1 accounts: [{'account_id': 1, 'account_owner': 'Luke', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Jimmy', 'balance': 500000.28}, {'account_id': 3, 'account_owner': 'Steve', 'balance': 25000.0}]
	INFO:  Bank 2 accounts: [{'account_id': 1, 'account_owner': 'Sarah', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Emma', 'balance': 2000.28}]
	INFO:  Emma received money from Jimmy.
	INFO:  Steve received money from Emma.
	INFO:  Sarah received money from Emma.
	INFO:  Pipeline Finished
	INFO:  Bank 1 accounts: [{'account_id': 1, 'account_owner': 'Luke', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Jimmy', 'balance': 480000.28}, {'account_id': 3, 'account_owner': 'Steve', 'balance': 27497.5}]
	INFO:  Bank 2 accounts: [{'account_id': 1, 'account_owner': 'Sarah', 'balance': 4230.3}, {'account_id': 2, 'account_owner': 'Emma', 'balance': 16480.28}]
	INFO:
	 ### Listing Transfers of accounts involved  ###
	INFO:  Jimmy: [{'amount': 320.13, 'dest_account_id': 2, 'info': 'Vacation rental', 'src_account_id': 1, 'transfer_id': 2, 'transfer_type': 'IntraBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 3, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 4, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 5, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 6, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 7, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 8, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 9, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 10, 'transfer_type': 'InterBank'}]


	INFO:  Emma: [{'amount': 1203.23, 'dest_account_id': 1, 'info': 'Rent money', 'src_account_id': 2, 'transfer_id': 1, 'transfer_type': 'IntraBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 3, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 4, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 5, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 6, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 7, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 8, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 9, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 10, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': "September's Rent", 'src_account_id': 2, 'transfer_id': 11, 'transfer_type': 'InterBank'}, {'amount': 3000.0, 'dest_account_id': 1, 'info': '', 'src_account_id': 2, 'transfer_id': 12, 'transfer_type': 'IntraBank'}]


	INFO:  Steve: [{'amount': 1203.23, 'dest_account_id': 3, 'info': 'Rent money', 'src_account_id': 1, 'transfer_id': 1, 'transfer_type': 'IntraBank'}, {'amount': 2497.5, 'dest_account_id': 3, 'info': "September's Rent", 'src_account_id': 0, 'transfer_id': 11, 'transfer_type': 'InterBank'}]


	INFO:  Sarah: [{'amount': 1203.23, 'dest_account_id': 1, 'info': 'Rent money', 'src_account_id': 2, 'transfer_id': 1, 'transfer_type': 'IntraBank'}, {'amount': 320.13, 'dest_account_id': 1, 'info': 'Vacation rental', 'src_account_id': 10, 'transfer_id': 2, 'transfer_type': 'IntraBank'}, {'amount': 3000.0, 'dest_account_id': 1, 'info': '', 'src_account_id': 2, 'transfer_id': 12, 'transfer_type': 'IntraBank'}]

We can see that Emma and Jimmy have a lot more transactions this is because they had to be batched (you can check the logic in `py_bank.orchestrator.send_money_inter` and sometimes they fail! But we make sure that Emma get's her money by trying again (if transfer fails).


I'll be honest and admit that we are missing a functionality to track in the Transfers, the original id of the User when performing an Inter transfer, for now I've put it as 0. Everytime there's an inter transfer. An easy fix would be to add optionally the account_id of the user in the `PUT` of both add and retire endpoints. Or create a dataclass that has `src_bank` and `account_id`.

    URI: /account_id/add
    BODY: {
    “amount” : Quantity (Decimal)
    “src_bank_info”: “source bank identifier + account_id”, (Optional in case the money comes from another
    bank)
    “info”: “Short string describing the purpose of the transfer”
    }


I didn't do this because I wasn't sure if if this was an "hard" requirement or not, in any case. Easily fixable.

Even so the accounts tell the story of task two.

	INFO:  Bank 1 accounts: [{'account_id': 1, 'account_owner': 'Luke', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Jimmy', 'balance': 500000.28}, {'account_id': 3, 'account_owner': 'Steve', 'balance': 25000.0}]
	INFO:  Bank 2 accounts: [{'account_id': 1, 'account_owner': 'Sarah', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Emma', 'balance': 2000.28}]

Jimmy started with `500000.28` and Steve with `250000` (bank 1). I use Luke just for testing.
Emma with `2000`(she needs money to pay her landlord, that's why she's so annoyed I guess ahah :-) ) and Sarah with `1230.3`.

After the pipeline, everyone got their money :-) Luke "lost" his `20000`, which in term Emma gained, but she also had to send to `3000` to Sarah (1230/3 + 3000 = 4200.3, checks out) and Steve got his rent money (2500 - COMISSIONS), so I guess Sarah owes him a coffee or she needs to take into account that next time. I don't know if banks just deduct that automatically from the account or keep the transaction, but if we would want to force that 100% Steve gets all the money, we would need to just change very small logic in the `Agent`.  It's just a question of who gets their commissions deducted.

	INFO:  Bank 1 accounts: [{'account_id': 1, 'account_owner': 'Luke', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Jimmy', 'balance': 480000.28}, {'account_id': 3, 'account_owner': 'Steve', 'balance': 27497.5}]
	INFO:  Bank 2 accounts: [{'account_id': 1, 'account_owner': 'Sarah', 'balance': 4230.3}, {'account_id': 2, 'account_owner': 'Emma', 'balance': 16480.28}]

To showcase how easy it is to do so I actually changed the code (one line) in another branch, where commissions are deducted from the account of the sender instead of the amount sent to the recipient. `feature/comissions_on_sender`

Here are the results:

	INFO:  Starting payment pipeline
	INFO:  Bank 1 accounts: [{'account_id': 1, 'account_owner': 'Luke', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Jimmy', 'balance': 500000.28}, {'account_id': 3, 'account_owner': 'Steve', 'balance': 25000.0}]
	INFO:  Bank 2 accounts: [{'account_id': 1, 'account_owner': 'Sarah', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Emma', 'balance': 2000.28}]

And now everyone gets their exact  money!!

	INFO:  Pipeline Finished
	INFO:  Bank 1 accounts: [{'account_id': 1, 'account_owner': 'Luke', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Jimmy', 'balance': 479980.28}, {'account_id': 3, 'account_owner': 'Steve', 'balance': 27500.0}]
	INFO:  Bank 2 accounts: [{'account_id': 1, 'account_owner': 'Sarah', 'balance': 4230.3}, {'account_id': 2, 'account_owner': 'Emma', 'balance': 16497.78}]
	INFO:

Also if we run again the operations they will add up. (until someone runs out of money to send). Gladly I gave Luke a lot of money so this doesn't happen while testing :-)!

We can see only one line changed: https://github.com/ZordoC/py_bank/pull/2/files


	INFO:  Starting payment pipeline
	INFO:  Bank 1 accounts: [{'account_id': 1, 'account_owner': 'Luke', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Jimmy', 'balance': 479980.28}, {'account_id': 3, 'account_owner': 'Steve', 'balance': 27500.0}]
	INFO:  Bank 2 accounts: [{'account_id': 1, 'account_owner': 'Sarah', 'balance': 4230.3}, {'account_id': 2, 'account_owner': 'Emma', 'balance': 16497.78}]
	INFO:  Emma received money from Jimmy.
	INFO:  Steve received money from Emma.
	INFO:  Sarah received money from Emma.
	INFO:  Pipeline Finished
	INFO:  Bank 1 accounts: [{'account_id': 1, 'account_owner': 'Luke', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Jimmy', 'balance': 459960.28}, {'account_id': 3, 'account_owner': 'Steve', 'balance': 30000.0}]
	INFO:  Bank 2 accounts: [{'account_id': 1, 'account_owner': 'Sarah', 'balance': 7230.3}, {'account_id': 2, 'account_owner': 'Emma', 'balance': 30995.28}]
	INFO:

## Testing

My favorite part :-) ! I wrote a small suite of tests (not 100% coverage, but I tried to cover the most important parts).

Let's clear our database:

	make stop-banks
	make start-banks

Now we have a fresh database (you can see the initial data of the system in `api/database.py` `add_data_bank_1` and `add_data_bank_2`.

### Unit tests
We can start by the unit tests:

	make tests-unit
	#or
	pytest tests/unit

We have 12 unit tests all green. These cover the "`py_bank/services`" module which is crucial for the working of our backend application, so we need to make sure it keeps working as we expect so that we can make changes with confidence!!! I used a semi-TDD approach (some were pure TDD others not so much) However I always think of testing when developing software. Our tests should NOT bend to our code, but the other way around (if the tests are good obviously).

## Integration

These tests integrate the high level functions `py_bank.orchestrator.send_money_inter`  (inter-transfers) and `py_bank.orchestrator.send_money_intra`  (Intra transfers). with the `Transfer Agent` .

	 make tests-integration

## E2E

And finally I had an old small E2E test that could use some refactoring using `py_bank.orchestrator.send_money_inter`  and `py_bank.orchestrator.send_money_intra` , they were used to test `Transfer Agent` which I thought would be my final "worker" however design evolves but this test still stands true to the whole Task 2, using a very very "happy" path where failures do not exist. Refactoring it and moving the existing E2E  to Integration would be a nice solution!


# Deployment

Ofcourse we'd need to deploy our bank apps at some point and not run our API locally. We have `start_banks_docker.sh` which work outside the devcontainer.
You need to re-open project locally.

Install dependencies on your machine:

	python -m  venv .venv
	. .venv/bin/activate
	pip3 install -r requirements.txt

Run:
	bash start_banks_docker.sh

And to test it:
	python -m py_banks.orchestrator


Remember python version => 3.8

This works on my machine, MacMini M1.

	Running Bank18971ce37f496c4993723d532aad682f2b53fbcc1a48589779ef9fff0c463dc34
	Running Bank25f3416e0ce54d95eaae450fe7947e574aa4e7f83736d2684ae103d5a9db76693
	(.venv) joserodrigues@Joses-Mac-mini py_bank % docker ps
	CONTAINER ID   IMAGE                 COMMAND                  CREATED         STATUS         PORTS                              NAMES
	5f3416e0ce54   flask-api/api:0.1.0   "python3 flask_api.py"   9 seconds ago   Up 8 seconds   5001/tcp, 0.0.0.0:5002->5002/tcp   xenodochial_herschel
	8971ce37f496   flask-api/api:0.1.0   "python3 flask_api.py"   9 seconds ago   Up 8 seconds   0.0.0.0:5001->5001/tcp, 5002/tcp   musing_shamir
	(.venv) joserodrigues@Joses-Mac-mini py_bank % python3 -m py_bank.orchestrator
	INFO:  Starting payment pipeline
	INFO:  Bank 1 accounts: [{'account_id': 1, 'account_owner': 'Luke', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Jimmy', 'balance': 500000.28}, {'account_id': 3, 'account_owner': 'Steve', 'balance': 25000.0}]
	INFO:  Bank 2 accounts: [{'account_id': 1, 'account_owner': 'Sarah', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Emma', 'balance': 2000.28}]
	INFO:  Emma received money from Jimmy.
	INFO:  Steve received money from Emma.
	INFO:  Sarah received money from Emma.
	INFO:  Pipeline Finished
	INFO:  Bank 1 accounts: [{'account_id': 1, 'account_owner': 'Luke', 'balance': 1230.3}, {'account_id': 2, 'account_owner': 'Jimmy', 'balance': 480000.28}, {'account_id': 3, 'account_owner': 'Steve', 'balance': 27497.5}]
	INFO:  Bank 2 accounts: [{'account_id': 1, 'account_owner': 'Sarah', 'balance': 4230.3}, {'account_id': 2, 'account_owner': 'Emma', 'balance': 16480.28}]
	INFO:

	### Listing Transfers of accounts involved  ###
	INFO:  Jimmy: [{'amount': 320.13, 'dest_account_id': 2, 'info': 'Vacation rental', 'src_account_id': 1, 'transfer_id': 2, 'transfer_type': 'IntraBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 3, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 4, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 5, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 6, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 7, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 8, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 9, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 2, 'transfer_id': 10, 'transfer_type': 'InterBank'}]


	INFO:  Emma: [{'amount': 1203.23, 'dest_account_id': 1, 'info': 'Rent money', 'src_account_id': 2, 'transfer_id': 1, 'transfer_type': 'IntraBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 3, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 4, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 5, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 6, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 7, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 8, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 9, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 2, 'info': 'Sorry for the delay, Emma!', 'src_account_id': 0, 'transfer_id': 10, 'transfer_type': 'InterBank'}, {'amount': 2497.5, 'dest_account_id': 0, 'info': "September's Rent", 'src_account_id': 2, 'transfer_id': 11, 'transfer_type': 'InterBank'}, {'amount': 3000.0, 'dest_account_id': 1, 'info': '', 'src_account_id': 2, 'transfer_id': 12, 'transfer_type': 'IntraBank'}]


	INFO:  Steve: [{'amount': 1203.23, 'dest_account_id': 3, 'info': 'Rent money', 'src_account_id': 1, 'transfer_id': 1, 'transfer_type': 'IntraBank'}, {'amount': 2497.5, 'dest_account_id': 3, 'info': "September's Rent", 'src_account_id': 0, 'transfer_id': 11, 'transfer_type': 'InterBank'}]


	INFO:  Sarah: [{'amount': 1203.23, 'dest_account_id': 1, 'info': 'Rent money', 'src_account_id': 2, 'transfer_id': 1, 'transfer_type': 'IntraBank'}, {'amount': 320.13, 'dest_account_id': 1, 'info': 'Vacation rental', 'src_account_id': 10, 'transfer_id': 2, 'transfer_type': 'IntraBank'}, {'amount': 3000.0, 'dest_account_id': 1, 'info': '', 'src_account_id': 2, 'transfer_id': 12, 'transfer_type': 'IntraBank'}]



# Conclusion

You can generate HTML documentation:

	make docs

And view it via:

	make simple-http

Navigate to the folder.


This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [ZordoC/cookiecutter-simple-pypackage](https://github.com/ZordoC/cookiecutter-simple-pypackage) project template.
