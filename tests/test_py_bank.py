#!/usr/bin/env python
"""Tests for `py_bank` package."""


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    status = response.status_code
    assert status == 200
