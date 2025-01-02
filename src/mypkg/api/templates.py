#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-10-31 21:19:57"

import json
from flask import request, jsonify
from marshmallow.exceptions import ValidationError as MarshValidationError
from database.pg_pool import close_pg
from database.pg_models import (
    add_new_template,
    get_all_templates,
    get_by_templateid,
    update_template,
    delete_template,
)
from database.schemas import Template_Schema, TemplateId_Schema
from util.apikeys import headerapikey
from util.errors import format_error_message
from util.logger import logger
from util.tracing import get_trace_id


@headerapikey
def add_templates():
    """
    Code to add a new template
    """
    # -- Initialization of function trace id
    trace_id = get_trace_id()
    try:
        # -- Evaluate the request and return the appropriate response
        recv_data = request.get_json()
        # -- Schema validation over the received JSON
        schema = Template_Schema()
        try:
            validata = schema.load(recv_data)
        except MarshValidationError as error:
            logger.error("%s | %s | Exception found; %s", trace_id, request.method, error)
            formatted_error = format_error_message(error.messages)
            response = {"error": "invalid json data", "details": formatted_error}
            return response, 400  # Bad Request
        # -- Log operational details
        logger.info("%s | %s | Template received", trace_id, request.method)
        # -- Add the new session to the database if the schema is valid
        new_template = add_new_template(validata)
        logger.info("%s | %s | Template stored with templateid %s", trace_id, request.method, new_template)
        return jsonify(new_template), 201  # Created
    except Exception as error:
        logger.error("%s | %s | Exception found; %s", trace_id, request.method, error)
        return jsonify({"error": str(error)}), 400  # Bad Request
    finally:
        close_pg()


@headerapikey
def get_templates():
    """
    Fetches all templates from the database, with pagination support.

    Retrieves templates based on the provided limit and offset query parameters.
    If no parameters are provided, it defaults to a limit of 10 and an offset of 0.

    Args:
        limit (int): The maximum number of records to return. Defaults to 10.
        offset (int): The starting point for the records. Defaults to 0.

    Returns:
        A JSON response containing the fetched templates, or an error message if no records are found.

    Raises:
        Exception: If an error occurs during the database query.
    """
    trace_id = get_trace_id()
    # Retrieve limit and offset from query parameters, with defaults
    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)

    # Enforce the hard limit of 100 records per request
    limit = min(limit, 100)
    # Enforce no negative offsets
    offset = max(offset, 0)
    try:
        # Fetch the templates using pagination
        templates = get_all_templates(limit=limit, offset=offset)
        if templates:
            return jsonify(templates), 200  # OK
        else:
            return {"error": "no records found in database"}, 404  # Not Found
    except Exception as error:
        logger.error("%s | %s | Exception found; %s", trace_id, request.method, str(error).rstrip("\n"))
        return jsonify({"error": str(error).rstrip("\n")}), 400  # Bad Request
    finally:
        close_pg()


@headerapikey
def get_template_id(template_id: str):
    """
    Code to get an existing template
    """
    # -- Initialization of function trace id
    trace_id = get_trace_id()
    try:
        # -- Evaluate the request and return the appropriate response
        template = get_by_templateid(template_id)
        if template:
            return jsonify(template), 200  # OK
        else:
            return jsonify({"error": "record not found"}), 404  # Not Found
    except Exception as error:
        logger.error("%s | %s | Exception found; %s", trace_id, request.method, str(error))
        return jsonify({"error": str(error).rstrip("\n")}), 400  # Bad Request
    finally:
        close_pg()


@headerapikey
def update_template_id(template_id: str):
    """
    Code to update an existing template
    """
    # -- Initialization of function trace id
    trace_id = get_trace_id()
    try:
        # -- Check if the request contains JSON
        if not request.is_json:
            return jsonify({"error": "request must be json"}), 400  # Bad Request
        # Validate the session_id
        templateid_schema = TemplateId_Schema()
        try:
            templateid_schema.load({"templateid": template_id})
        except MarshValidationError as error:
            logger.error("%s | %s | Exception found with UUID; %s", trace_id, request.method, error)
            formatted_error = format_error_message(error.messages)
            response = {"error": "invalid uuid", "details": formatted_error}
            return response, 400  # Bad Request
        # -- Receive data via PUT and uptdate the template in the database
        recv_data = request.get_json(force=True)
        logger.info("%s | %s | Received data is %s", trace_id, request.method, json.dumps(recv_data))
        # -- Schema validation over the received JSON
        template_schema = Template_Schema()
        try:
            validata = template_schema.load(recv_data)
            logger.info("%s | %s | Validata is %s", trace_id, request.method, json.dumps(validata))
        except MarshValidationError as error:
            logger.error("%s | %s | Exception found; %s", trace_id, request.method, error)
            formatted_error = format_error_message(error.messages)
            response = {"error": "Invalid JSON data", "details": formatted_error}
            return response, 400  # Bad Request
        # -- Update the template in the database
        template = get_by_templateid(template_id)
        logger.info("%s | %s | Template is %s", trace_id,request.method, json.dumps(str(template)))
        if template is not None and template_id in template["templateid"]:
            logger.info("%s | %s | Performing update", trace_id, request.method)
            update_template(template_id, validata)
            return jsonify({"message": "record updated"}), 200  # OK or 202 Accepted
        else:
            return jsonify({"error": "record not found"}), 404  # Not Found
    except Exception as error:
        logger.error("%s | %s | Exception found; %s", trace_id, request.method, error)
        return jsonify({"error": str(error)}), 400  # Bad Request
    finally:
        close_pg()


@headerapikey
def delete_template_id(template_id: str):
    """
    Code to delete an existing template
    """
    # -- Initialization of function trace id
    trace_id = get_trace_id()
    try:
        # -- Evaluate the request and return the appropriate response
        template = get_by_templateid(template_id)
        if template is not None and template_id in template["templateid"]:
            delete_template(template_id)
            return jsonify({"message": "record deleted"}), 200  # OK or 204 No Content
        else:
            return jsonify({"error": "record not found"}), 404  # Not Found
    except Exception as error:
        logger.error("%s | %s | Exception found; %s", trace_id, request.method, error)
        return jsonify({"error": str(error)}), 500  # Internal Server Error
    finally:
        close_pg()
