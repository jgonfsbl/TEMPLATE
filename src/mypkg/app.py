#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-07-08 23:54:38"


# Import of general libraries
import psycopg2
from flask import Flask, url_for, g

# Import of local libraries
from config import Config
from database.pg_conn_pool import init_db, close_db
from utils.helpers import headerapikey
from utils.telemetry import capture_request, capture_response

# import of local api handlers
from api.templates import get_templates, add_templates, get_template_id, update_template_id, delete_template_id
from api.security import authenticate, authorize

# import integrations
from integrations.integration1 import integration1_message

# Create the Flask application
app = Flask(__name__)
app.config.from_object(Config)
app.json.sort_keys = False


###############################################################################
#
# ROUTES FOR API ENDPOINTS
#
###############################################################################

# Template routes
app.add_url_rule("/templates", "get_templates", get_templates, methods=["GET"])
app.add_url_rule("/templates", "add_templates", add_templates, methods=["POST"])
app.add_url_rule("/templates/<template_id>", "get_template_id", get_template_id, methods=["GET"])
app.add_url_rule("/templates/<template_id>", "update_template_id", update_template_id, methods=["PUT"])
app.add_url_rule("/templates/<template_id>", "delete_template_id", delete_template_id, methods=["DELETE"])

# Security routes
app.add_url_rule("/sec/authn", "authn", authenticate, methods=["POST"])
app.add_url_rule("/sec/authz", "authz", authorize, methods=["POST"])

# Integrations routes
app.add_url_rule("/int/integration", "integration1_message", integration1_message, methods=["POST"])


###############################################################################
#
# REQUEST HANDLERS
#
###############################################################################


@app.before_request
def before_request():
    """
    This function handles HTTP request as it arrives to the API
    """
    # Action 1 - Telemetry
    capture_request()
    # Action 2 - Connect to the database pool if not connected
    if not hasattr(g, "db_pool"):
        try:
            init_db()
        except psycopg2.OperationalError:
            print(f"Error: Connection to database failed")
            exit(1)


@app.after_request
def after_request(response):
    """
    This function handles HTTP response before send it back to client
    """
    # Action 1 - Return the response with telemetry data
    return capture_response(response)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Close the database connection at the end of each request
    """
    try:
        close_db()
    except psycopg2.OperationalError:
        print(f"Error: Connection to database failed")
        exit(1)


###############################################################################
#
# APPLICATION ENTRY POINT
#
###############################################################################


@app.route("/")
@headerapikey
def get_index():
    """Main index"""
    response = {"message": "Index HETEOAS", "links": []}
    return response


@app.route("/status")
def get_status():
    """Status endpoint"""
    return "OK"


if __name__ == "__main__":
    app.run(
        host=app.config["FLASK_HOST"],
        port=app.config["FLASK_PORT"],
        debug=app.config["FLASK_DEBUG"],
    )
