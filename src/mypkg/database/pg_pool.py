#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-10-31 20:39:44"


from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from flask import current_app, g


minconn = 1  # Minimum number of connections to keep in the pool
maxconn = 20  # Maximum number of connections to keep in the pool


def init_pg():
    """
    Initialize the database connection pool
    """
    g.pgsql_pool = pool.SimpleConnectionPool(
        minconn,
        maxconn,
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASS"],
        host=current_app.config["DB_HOST"],
        port=current_app.config["DB_PORT"],
        database=current_app.config["DB_NAME"],
    )


def get_pg():
    """
    Get a database connection from the pool
    """
    if "pgsql_conn" not in g or g.pgsql_conn.closed != 0:
        g.pgsql_conn = g.pgsql_pool.getconn()
    return g.pgsql_conn


def close_pg():
    """
    Close the database connection and return it to the pool
    """
    if "pgsql_conn" in g:
        g.pgsql_pool.putconn(g.pop("pgsql_conn"))


def execute_pg_query(query, params=None, commit=False):
    """
    Execute a SQL query and return a RealDictCursor (a Python dictionary)
    """
    conn = get_pg()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(query, params or ())
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    return cursor


def rollback_pg():
    """
    Rollback the current transaction
    """
    conn = get_pg()
    conn.rollback()
    close_pg()
