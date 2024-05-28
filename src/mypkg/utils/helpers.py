#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" PROJECT NAME """

__updated__ = "2016-03-16 00:00:00"

from time import time


def exectime(func):
    """Measure the time taken to execute a function."""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        return result

    return wrapper
