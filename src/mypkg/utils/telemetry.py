#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

import json
import requests
from flask import current_app, request, g
from time import time


def capture_request():
    """
    Capture the request data and store it in the 'g' global object
    """
    # Store the start time of the request
    g.start_time = time()
    # Build the request data dictionary
    request_data = {
        "timestamp": time(),
        "method": request.method,
        "endpoint": request.path,
        "query_params": request.args.to_dict(),
        "request_payload": request.get_json() if request.is_json else request.form.to_dict(),
        "ip_address": request.remote_addr,
        "user_agent": request.user_agent.string,
    }
    # Store the request data in the 'g' global object
    g.request_data = request_data


def capture_response(response):
    """
    Capture the response data, store it the 'g' global object and send the
    telemetry data to the telemetry service
    """
    # Calculate the response time
    response_time = round(time() - g.start_time, 6)
    # Build the response data dictionary
    response_data = {
        "status_code": response.status_code,
        "response_time": response_time,
    }
    # Store the response data in the 'g' global object
    g.response_data = response_data
    # Send the telemetry data to the telemetry service
    send_data(g.request_data, g.response_data)
    # Return the original response object unchanged
    return response


def send_data(request_data, response_data):
    """
    Send the telemetry data to the telemetry service over HTTP/MQTT/Kafka
    """
    # Build the telemetry data dictionary with the request and response data
    telemetry_data = {
        "request": request_data,
        "response": response_data,
    }
    # Send this data to your telemetry service
    # TODO: Replace this with actual sending logic
    print(json.dumps(telemetry_data))
    # response = requests.post(current_app.config["TELEMETRY_URL"], json=telemetry_data)
    # print(response.status_code)
