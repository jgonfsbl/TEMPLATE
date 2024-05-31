#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-05-12 12:23:37"


import pytest
from app import main


def test_main(capfd):
    main()
    captured = capfd.readouterr()
    assert captured.out == "Hello World!\n"
