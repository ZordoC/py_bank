"""Module to test ``py_bank.service_layer.services.create_transfer."""
import random

import pytest
from sqlalchemy import func

from py_bank.domain import Transfer
from py_bank.service_layer import create_transfer


def test_create_transfer(domain_session):

    largest_id = domain_session.query(func.max(Transfer.transfer_id)).one()[0]
    new_id = largest_id + 1

    transfer = create_transfer(domain_session, "1", "2", 200, "Test")

    assert transfer == Transfer(new_id, 200, "IntraBank", "1", "2", "Test")
