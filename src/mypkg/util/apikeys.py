#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-10-31 21:12:58"

# -- Standard library imports
from functools import wraps
# -- Third-party imports
from flask import request, jsonify
# -- Local imports
from database.redis_pool import get_redis
from util.logger import logger
from util.tracing import get_trace_id


def headerapikey(func):
    """
    Check the header for the API key.

    This function is a decorator that checks for the existence of the
    X-API-KEY header in the request. If the header is not present, it
    returns a 400 Bad Request response with a JSON object containing
    the error message.

    If the API key exists in the Redis hash "sec_apikeys", it returns
    the associated metadata. If the API key does not exist, it returns
    a 401 Unauthorized response with a JSON object containing the
    error message.

    :param func: The function to be decorated
    :return: The decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        trace_id = get_trace_id()

        try:
            apikey = request.headers.get("X-API-KEY")

            # -- Check if there is the X-API-KEY header
            if not apikey:
                logger.warning(
                    "%s | %s | API key is missing; Header does not contain X-API-KEY field",
                    trace_id,
                    request.method,
                )
                return jsonify({"error": "API key is missing"}), 400  # Bad Request

            # -- Check if the API key exists in the hash and retrieve the associated metadata
            redis_conn = get_redis()
            user_info = redis_conn.hget("sec_apikeys", apikey)

            # -- Check if the API key exists in the Redis set
            if user_info:
                logger.info("%s | %s | API key is valid", trace_id, request.method)
                return func(*args, **kwargs)
            else:
                logger.warning(
                    "%s | %s | Unauthorized access attempt with API key: %s",
                    trace_id,
                    request.method,
                    apikey,
                )
                return jsonify({"error": "Unauthorized"}), 401  # Unauthorized

        except Exception as error:
            logger.error(
                "%s | %s | Exception found while checking API key; %s",
                request.method,
                trace_id,
                error,
            )
            return jsonify({"wrapper_error": str(error)}), 500  # Internal Server Error

    return wrapper