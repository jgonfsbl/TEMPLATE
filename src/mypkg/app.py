#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-06-09 10:23:23"


# Import of general libraries
from flask import Flask

# Import of local libraries
from config import Config

from database.connections import db
from database.models import templateSchema

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
    """This function handles HTTP request as it arrives to the API"""


@app.after_request
def after_request(response):
    """This function handles HTTP response before send it back to client"""
    return response


###############################################################################
#
# APPLICATION ENTRY POINT
#
###############################################################################


if __name__ == "__main__":
    app.run()
