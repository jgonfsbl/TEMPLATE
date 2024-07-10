#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-07-06 17:43:38"


from database.pg_conn_pool import execute_query


###############################################################################
#
# Model: Templates
#
###############################################################################


# CRUD operations
# C - Create
def add_new_template(template_data):
    """Add a new template to the database."""

    _template_id = template_data.get("templateid")

    query = f"SELECT * FROM templates WHERE templateid = '{_template_id}' ORDER BY tidx ASC;"
    cursor = execute_query(query)
    item_exists = cursor.fetchone()

    if not item_exists:
        return None  # The session does not exist
    else:
        query = f"SELECT * FROM templates WHERE templateid = '{_template_id}' ORDER BY tidx ASC;"
        cursor = execute_query(query)
        template_exists = cursor.fetchone()

        if template_exists:
            return None  # The template already exists
        else:
            #
            # Do some processing here with the template_data
            #
            query = f"""
                INSERT INTO templates (templateid, name, description, content)
                VALUES ('', '', '', '');
                RETURNING templateid;
            """
            cursor = execute_query(query, commit=True)
            return cursor.rowcount


# CRUD operations
# R - Read
def get_all_templates():
    """Retrieve all templates from the database."""
    query = "SELECT * FROM user_sessions ORDER BY tidx ASC;"
    cursor = execute_query(query)
    session_data = cursor.fetchall()
    #
    # Do some processing here with the session_data
    #
    response = {}
    return response


# CRUD operations
# R - Read
def get_by_templateid(template_id):
    """Retrieve a template from the database."""
    try:
        query = f"SELECT * FROM templates WHERE templateid = '{template_id}' ORDER BY tidx ASC;"
        cursor = execute_query(query)
        session_data = cursor.fetchone()
        #
        # Do some processing here with the session_data
        #
        response = {}
        return response
    except Exception as error:
        print(error)  # debug only
        return None


# CRUD operations
# U - Update
def update_template(template_id, template_data):
    """Update a template in the database."""

    # Extract data from session_data
    _var = template_data.get("var")

    # Combine all data into one dictionary
    data = {
        "template_id": template_id,
        "var": _var,
        #
        # Add more data here
        #
    }

    # Build the query with f-strings
    query = f"""
    UPDATE templates SET
        #...
        #...
        #...
        modified = NOW()
    WHERE templateid = '{data['template_id']}';
    """

    # Execute the query
    cursor = execute_query(query, data, commit=True)
    return cursor.rowcount


# CRUD operations
# D - Delete
def delete_template(template_id):
    """Delete a template from the database."""
    # Build the query
    query = f"DELETE FROM templates WHERE templateid = '{template_id}';"
    # Execute the query
    cursor = execute_query(query, commit=True)
    return cursor.rowcount
