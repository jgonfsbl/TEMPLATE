#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-10-31 21:12:58"

# -- Third-party imports
import psutil
import time
from flask import Response, request
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
# -- Local imports
from database.pg_pool import execute_pg_query
from database.redis_pool import execute_command_redis
from util.logger import logger
from util.tracing import get_trace_id


# Define system resource gauges
CPU_USAGE = Gauge('container_cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('container_memory_usage_bytes', 'Memory usage in bytes')
MEMORY_AVAILABLE = Gauge('container_memory_available_bytes', 'Available memory in bytes')
PGSQL_QUERY_LATENCY = Gauge('pgsql_query_latency_seconds', 'Postgres query latency in seconds')
REDIS_QUERY_LATENCY = Gauge('redis_query_latency_seconds', 'Redis query latency in seconds')


def pgsql_query_latency():
    """
    This function queries the database for a predefined query to measure latency
    The query is: SELECT * FROM templates ORDER BY templateid DESC LIMIT 10;
    """
    # --Execute the query
    query = "SELECT * FROM templates ORDER BY templateid DESC LIMIT 100;"
    cursor = execute_pg_query(query, commit=False)
    return cursor.rowcount


def redis_query_latency():
    """
    This function queries the Redis database to measure latency
    The query is: SELECT * FROM templates ORDER BY templateid DESC LIMIT 10;
    """
    # -- Initialization of function trace id
    trace_id = get_trace_id()
    # --Execute the query
    try:
        # Example key for testing Redis latency
        command = "HGETALL"
        hash_table = "sec_apikeys"
        execute_command_redis(command, hash_table)
    except Exception as e:
        logger.error("%s | %s | Redis query failed: %s", trace_id, request.method, str(e))
        return None


def collect_system_metrics():
    """
    Collect system resource metrics.

    This function collects metrics on the current state of CPU usage, memory
    usage, and available memory. It also measures the latency of a database
    query to the PostgreSQL database.
    """
    # -- Initialization of function trace id
    trace_id = get_trace_id()
    # -- Measure CPU usage
    CPU_USAGE.set(psutil.cpu_percent(interval=1))
    # -- Measure memory usage
    memory = psutil.virtual_memory()
    MEMORY_USAGE.set(memory.used)
    MEMORY_AVAILABLE.set(memory.available)
    # -- Measure Postgres query latency
    start_time = time.time()
    pgsql_query_latency()
    end_time = time.time()
    PGSQL_QUERY_LATENCY.set(end_time - start_time)
    logger.info("%s | %s | Postgres query latency: %s", trace_id, request.method, end_time - start_time)
    # -- Measure Redis query latency
    start_time = time.time()
    redis_query_latency()
    end_time = time.time()
    REDIS_QUERY_LATENCY.set(end_time - start_time)
    logger.info("%s | %s | Redis query latency: %s", trace_id, request.method, end_time - start_time)


def get_metrics():
    """
    Expose Prometheus metrics.

    This function collects system resource metrics and the latency of a
    database query, and returns the metrics output.
    """
    # -- Initialization of function trace id
    trace_id = get_trace_id()
    # -- Log operational details
    logger.info("%s | %s | Gathering Prometheus metrics", trace_id, request.method)
    # -- Collect system metrics
    collect_system_metrics()
    # -- Generate and return the metrics output
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
