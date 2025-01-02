#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """


__updated__ = "2024-10-31 21:12:58"


# -- Standard library imports
import time
from functools import wraps
# -- Third-party imports
from flask import request, g
# -- Local imports
from util.logger import logger
from util.tracing import get_trace_id


def exectime(func):
    """
    Measure the time taken to execute a function.

    This decorator function measures the time taken to execute a function by
    recording the time before and after the function is called. The time taken is
    then printed to the console.

    Example:
    @exectime
    def my_function():
        pass

    my_function()
    # Output: 0.0012345 (example output)
    """
    def wrapper(*args, **kwargs):
        # Start timer
        start_time = time.time()
        # Call thw wrapped function; when done return here
        result = func(*args, **kwargs)
        # Stop timer
        end_time = time.time()
        # Calculate time taken
        reportedtime = end_time - start_time
        # Log time taken
        logger.info("%s | %s | Execution time was %s", get_trace_id(), request.method, reportedtime)
        # Return result
        return result
    return wrapper



def no_db_connection(f):
    """
    Decorator to indicate that a function does not require a database connection.

    This decorator is used to indicate that a function does not require a database connection.

    Args:
        f (function): The function to decorate.

    Returns:
        function: The decorated function.

    Example:
        @no_db_connection
        def my_function():
            pass

    my_function()
    # Output: None
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.no_db_connection = True
        return f(*args, **kwargs)
    return decorated_function