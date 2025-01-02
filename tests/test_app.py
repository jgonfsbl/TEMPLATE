#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-07-05 10:43:22"


import json
import pytest
from src.mypkg.app import get_status, app


def test_get_index():
    client = app.test_client()
    headers = {"X-API-KEY": "12345678-90ab-cdef-1234-567890abcdef"}
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.content_type == "application/json"
    data = json.loads(response.data)
    assert data["message"] == "Index HETEOAS"


def test_get_status():
    """Test the get_status function"""
    expected = "OK"
    response = get_status()
    assert response == expected


if __name__ == "__main__":
    pytest.main()
