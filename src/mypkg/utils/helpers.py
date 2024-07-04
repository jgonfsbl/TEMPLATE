#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" PROJECT NAME """

__updated__ = "2024-07-04 15:10:23"

from time import time
from flask import request, jsonify
from flask import current_app


def exectime(func):
    """Measure the time taken to execute a function."""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        return result

    return wrapper


def headerapikey(func):
    """Check the header for the API key"""

    def wrapper(*args, **kwargs):
        try:
            apikey = request.headers.get("X-API-KEY")
            if apikey in current_app.config["X-API-KEY"]:  # OR apikey in redis.get("api:keys")
                return func(*args, **kwargs)
            else:
                return {"error": "Unauthorized"}, 401  # Unauthorized
        except Exception as e:
            return jsonify({"wrapper_error": str(e)}), 500  # Internal Server Error

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__module__ = func.__module__

    return wrapper


def format_error_message(error_dict):
    """Parse the internal error messages and format them for using them in a JSON response"""

    error_messages = []
    for field, errors in error_dict.items():
        if isinstance(errors, dict):
            for index, field_errors in errors.items():
                for error, error_value in field_errors.items():
                    error_value_string = ", ".join(error_value) if isinstance(error_value, list) else error_value
                    error_messages.append(f"{field}[{index}].{error}: {error_value_string}")
        else:
            for error in errors:
                error_value_string = ", ".join(error) if isinstance(error, list) else error
                error_messages.append(f"{field}: {error_value_string}")

    return "\n".join(error_messages)
