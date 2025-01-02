#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-10-31 21:37:15"


# -- Standard library imports
import json
from datetime import datetime
# -- Third-party imports
import psycopg2
import redis.exceptions
from flask import Flask, request, g, jsonify
# -- Local imports
from config import Config
from api.templates import get_templates, add_templates, get_template_id, update_template_id, delete_template_id
from database.pg_pool import init_pg, close_pg
from database.redis_pool import init_redis, close_redis
from util.decorators import no_db_connection
from util.logger import logger, setup_logging
from util.prometheus import get_metrics
from util.ratelimiter import init_limiter, rate_limit
from util.tracing import generate_trace_id, get_trace_id


# -- Custom encoder for JSON serialization
class CustomJSONEncoder(json.JSONEncoder):
    """
    This class is used to serialize datetime objects to ISO format
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


# -- Create the Flask application
app = Flask(__name__)
app.config.from_object(Config)
# -- Disable automatic sorting of JSON
app.json.sort_keys = False
# -- This custom encoder is used for JSON formatting of dates in ISO format
app.json_encoder = CustomJSONEncoder
# -- Call setup_logging early so that all logs are captured now onwards
setup_logging()
# -- Set up the application context
with app.app_context():
    # Initialize Redis connection pool and attach limiter
    init_redis()
    init_limiter(app)

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
    # -- Step 1: Initialization of Trace ID
    generate_trace_id()
    trace_id = get_trace_id()
    logger.info("%s | %s | New request on %s", trace_id, request.method, request.path)
    # -- Step 1: Analyze the need for database connection
    if not 'no_db_connection' in g:
        # -- Step 2: Redis initialization, if not initialized already
        if not hasattr(g, "redis_pool"):
            try:
                init_redis()
            except redis.exceptions.ConnectionError:
                logger.error("%s | %s | Connection to Redis failed", trace_id, request.method)
                exit(1)
        # -- Step 3: Connect to the Postgres database pool, if not connected
        if not hasattr(g, "pgsql_pool"):
            try:
                init_pg()
            except psycopg2.OperationalError:
                logger.error("%s | %s | Connection to PGSQL failed", trace_id, request.method)
                exit(1)
        logger.info("%s | %s | Evaluating PGSQL/Redis Conn Pool need", trace_id, request.method)


@app.after_request
def after_request(response):
    """
    This function handles HTTP response before send it back to client
    """
    # -- Log the request completion
    logger.info(
        "%s | %s | Completed request on %s",
        get_trace_id(),
        request.method,
        request.path,
    )
    logger.info(
        "%s | %s | Operation status was %s",
        get_trace_id(),
        request.method,
        response.status,
    )
    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Close the database connection at the end of each request
    """
    # -- Initialization of function trace id
    trace_id = get_trace_id()
    # -- Set TDAC (Tear Down Application Context) as the request method
    request_method = "TDAC"
    # -- Step 1: No DB connection
    if hasattr(g, 'no_db_connection'):
        delattr(g, 'no_db_connection')
        logger.info("%s | %s | No PGSQL/Redis Conn Pool used", trace_id, request_method)
    else:
        # -- Step 2: Postgres
        try:
            close_pg()
            logger.info("%s | %s | PGSQL Conn Pool closed", trace_id, request_method)
        except psycopg2.OperationalError as error:
            logger.warning("%s | %s | Closing connection to Postgres failed: %s", trace_id, request_method, str(error))
        # -- Step 3: Redis
        try:
            close_redis()
            logger.info("%s | %s | Redis Conn Pool closed", trace_id, request_method)
        except redis.exceptions.ConnectionError as error:
            logger.warning("%s | %s | Closing connection to Redis failed: %s", trace_id, request_method, str(error))


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


###############################################################################
#
# ROUTES FOR METRICS, LOGGING AND OBERVABILITY
#
###############################################################################

if Config.PROMETHEUS_ENABLED:
# Metrics routes for Prometheus
    app.add_url_rule("/metrics", "metrics", get_metrics, methods=["GET"])


###############################################################################
#
# ENDPOINT FOR HEALTH CHECK
#
###############################################################################

@app.route("/status")
@no_db_connection
@rate_limit(100)
def get_status():
    """
    Status endpoint for health checks
    """
    # -- Initialization of function trace id
    trace_id = get_trace_id()
    logger.info("%s | %s | Status edpoint called", trace_id, request.method)
    return jsonify({"status": "ok"})


###############################################################################
#
# ENDPOINT INDEX
#
###############################################################################

@app.route("/")
@no_db_connection
@rate_limit(100)
def get_index():
    """
    Main index
    """
    # -- Initialization of function trace id
    trace_id = get_trace_id()
    response = {"message": "Index HETEOAS", "links": []}
    logger.info("%s | %s | Index edpoint called", trace_id, request.method)
    return response


###############################################################################
#
# APPLICATION ENTRY POINT
#
###############################################################################

if __name__ == "__main__":
    app.run(host=app.config["FLASK_HOST"],port=app.config["FLASK_PORT"])
