#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-10-31 21:12:58"

import psutil
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

# Define system resource gauges
CPU_USAGE = Gauge('container_cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('container_memory_usage_bytes', 'Memory usage in bytes')
MEMORY_AVAILABLE = Gauge('container_memory_available_bytes', 'Available memory in bytes')

def collect_system_metrics():
    """Collect system resource metrics."""

    # CPU Usage
    CPU_USAGE.set(psutil.cpu_percent(interval=1))

    # Memory Usage
    memory = psutil.virtual_memory()
    MEMORY_USAGE.set(memory.used)
    MEMORY_AVAILABLE.set(memory.available)


def get_metrics():
    """Expose Prometheus metrics."""

    # Collect system metrics
    collect_system_metrics()

    # Generate and return the metrics output
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
