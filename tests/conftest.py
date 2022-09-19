"""Conftest for `py_repo` package."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker


from py_bank.service_layer import start_mappers, metadata


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def domain_session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()