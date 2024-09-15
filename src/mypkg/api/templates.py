#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-07-06 17:43:40"


from flask import request, jsonify
from marshmallow.exceptions import ValidationError as MarshValidationError
from database.pg_conn_pool import close_db
from database.pg_models import (
    add_new_template,
    get_all_templates,
    get_by_templateid,
    update_template,
    delete_template,
)
from database.schemas import Template_Schema, TemplateId_Schema
from utils.helpers import headerapikey, format_error_message


@headerapikey
def add_templates():
    """Code to add a new template"""
    try:
        # -- Evaluate the request and return the appropriate response
        recv_data = request.get_json()

        # -- Schema validation
        schema = Template_Schema()
        try:
            validata = schema.load(recv_data)
        except MarshValidationError as error:
            formatted_error = format_error_message(error.messages)
            response = {"error": "invalid json data", "details": formatted_error}
            return response, 400  # Bad Request

        # -- Add the new session to the database if the schema is valid
        new_template = add_new_template(validata)
        return jsonify(new_template), 201  # Created

    except Exception as error:
        return jsonify({"error": str(error)}), 500  # Internal Server Error
    finally:
        close_db()


@headerapikey
def get_templates():
    """Code to fetch all templates"""
    try:
        # Retrieve limit and offset from query parameters, with defaults
        limit = request.args.get('limit', default=10, type=int)
        offset = request.args.get('offset', default=0, type=int)

        # Enforce the hard limit of 50 records per request
        if limit > 50:
            limit = 50

        # Fetch the templates using pagination with the adjusted limit
        templates = get_all_templates(limit=limit, offset=offset)
        
        # -- Evaluate the request and return the appropriate response
        templates = get_all_templates()

        # if templates and templates.get('data'):
        if templates:
            return jsonify(templates), 200  # OK
        else:
            return {"error": "no records found in database"}, 404  # Not Found

    except Exception as error:
        return jsonify({"error": str(error)}), 500  # Internal Server Error
    finally:
        close_db()


@headerapikey
def get_template_id(template_id: str):
    """Code to get an existing template"""
    try:
        # -- Evaluate the request and return the appropriate response
        template = get_by_templateid(template_id)
        if template:
            return jsonify(template), 200  # OK
        else:
            return jsonify({"error": "record not found"}), 404  # Not Found

    except Exception as error:
        return jsonify({"error": str(error)}), 500  # Internal Server Error
    finally:
        close_db()


@headerapikey
def update_template_id(template_id: str):
    """Code to update an existing template"""
    try:
        # -- Check if the request contains JSON
        if not request.is_json:
            return jsonify({"error": "request must be json"}), 400  # Bad Request

        # Validate the session_id
        templateid_schema = TemplateId_Schema()
        try:
            templateid_schema.load({"templateid": template_id})
        except MarshValidationError as error:
            formatted_error = format_error_message(error.messages)
            response = {"error": "invalid uuid", "details": formatted_error}
            return response, 400  # Bad Request

        # -- Receive data via PUT and uptdate the template in the database
        recv_data = request.get_json(force=True)

        # -- Schema validation
        template_schema = Template_Schema()
        try:
            validata = template_schema.load(recv_data)
        except MarshValidationError as error:
            formatted_error = format_error_message(error.messages)
            response = {"error": "Invalid JSON data", "details": formatted_error}
            return response, 400  # Bad Request

        # -- Update the template in the database
        template = get_by_templateid(template_id)
        if template is not None and template_id in template["templateid"]:
            update_template(template_id, validata)
            return jsonify({"message": "record updated"}), 200  # OK or 202 Accepted
        else:
            return jsonify({"error": "record not found"}), 404  # Not Found

    except Exception as error:
        return jsonify({"error": str(error)}), 500  # Internal Server Error
    finally:
        close_db()


@headerapikey
def delete_template_id(template_id: str):
    """Code to delete an existing template"""
    try:
        # -- Evaluate the request and return the appropriate response
        template = get_by_templateid(template_id)
        if template is not None and template_id in template["templateid"]:
            delete_template(template_id)
            return jsonify({"message": "record deleted"}), 200  # OK or 204 No Content
        else:
            return jsonify({"error": "record not found"}), 404  # Not Found

    except Exception as error:
        return jsonify({"error": str(error)}), 500  # Internal Server Error
    finally:
        close_db()
