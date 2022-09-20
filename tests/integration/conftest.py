"""Conftest for integration."""
import pytest

from py_bank.transfer_agent import URL_1, URL_2, RequestsAgent


@pytest.fixture
def agent():
    agent = RequestsAgent(base_bank_1_url=URL_1, base_bank_2_url=URL_2)
    return agent
