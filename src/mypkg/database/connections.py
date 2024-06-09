#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-05-31 13:17:45"


from psycopg2 import pool
from flask import current_app, g


def init_db():
    """Initialize the database connection pool."""
    g.db_pool = pool.SimpleConnectionPool(
        1,
        20,
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASS"],
        host=current_app.config["DB_HOST"],
        port=current_app.config["DB_PORT"],
        database=current_app.config["DB_NAME"],
    )


def get_db():
    """Get a database connection from the pool."""
    if "db_conn" not in g:
        g.db_conn = g.db_pool.getconn()
    return g.db_conn


def close_db():
    """Close the database connection."""
    db_conn = g.pop("db_conn", None)
    if db_conn is not None:
        g.db_pool.putconn(db_conn)


def execute_query(query, params=None, commit=False):
    """Execute a SQL query."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    if commit:
        conn.commit()
    return cursor


def rollback():
    """Rollback the current transaction."""
    conn = get_db()
    conn.rollback()
    close_db()
