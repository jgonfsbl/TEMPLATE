#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-07-06 18:00:25"


from flask import request, jsonify
from database.redis_conn_pool import record_exists, execute_command, read_record, update_record, delete_record


###############################################################################
#
# Model: Redis records
#
###############################################################################


# CRUD operations
# C - Create
def add_record(key):
    value = request.json
    if record_exists(key):
        return jsonify({"error": "Record already exists"}), 400
    execute_command("SET", key, value)
    return jsonify({"message": "Record created"}), 201


# CRUD operations
# R - Read
def get_record(key):
    if not record_exists(key):
        return jsonify({"error": "Record not found"}), 404
    record = read_record(key)
    return jsonify(record)


# CRUD operations
# U - Update
def modify_record(key):
    value = request.json
    if not record_exists(key):
        return jsonify({"error": "Record not found"}), 404
    update_record(key, value)
    return jsonify({"message": "Record updated"}), 200


# CRUD operations
# D - Delete
def remove_record(key):
    if not record_exists(key):
        return jsonify({"error": "Record not found"}), 404
    delete_record(key)
    return jsonify({"message": "Record deleted"}), 200
