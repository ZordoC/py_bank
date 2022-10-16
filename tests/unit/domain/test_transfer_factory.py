"""Module to test ``py_bank.service_layer.services.create_transfer."""
from sqlalchemy import func

from py_bank.domain import TransferRecord


def test_transfer_factory(domain_session):
    largest_id = domain_session.query(func.max(TransferRecord.transfer_id)).one()[0]
    new_id = largest_id + 1

    transfer = TransferRecord.factory(domain_session, "1", "2", 200, "Test")

    assert transfer == TransferRecord(new_id, 200, "IntraBank", "1", "2", "Test")
