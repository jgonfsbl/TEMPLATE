#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-05-12 19:47:43"


from connections import execute_query
from schemas import templateSchema

###############################################################################
#
# Model: Templates
#
###############################################################################


def get_all_templates():
    """Retrieve all templates from the database."""
    cursor = execute_query("SELECT * FROM templates;")
    templates = cursor.fetchall()
    schema = templateSchema(many=True)
    try:
        templates = schema.load(templates)
    except Exception as e:
        print(f"Validation error: {e}")
    cursor.close()
    return templates


def add_template(template_data):
    """Add a new template to the database."""
    sql = "INSERT INTO templates (name, description, content) VALUES (%s, %s, %s) RETURNING id;"
    cursor = execute_query(
        sql, (template_data["name"], template_data["description"], template_data["content"]), commit=True
    )
    template_id = cursor.fetchone()[0]
    schema = templateSchema()
    try:
        template_data = schema.load(template_data)
    except Exception as e:
        print(f"Validation error: {e}")
    cursor.close()
    return template_id


def get_template(template_id):
    """Retrieve a template from the database."""
    cursor = execute_query("SELECT * FROM templates WHERE id = %s;", (template_id,))
    template = cursor.fetchone()
    schema = templateSchema()
    try:
        template = schema.load(template)
    except Exception as e:
        print(f"Validation error: {e}")
    cursor.close()
    return template


def update_template(template_id, template_data):
    """Update a template in the database."""
    sql = f"UPDATE templates \ 
            SET name = '{template_data['name']}', \
                description = '{template_data['description']}', \
                content = '{template_data['content']}' \
            WHERE id = {template_id};"
    execute_query(sql, commit=True)


def delete_template(template_id):
    """Delete a template from the database."""
    execute_query("DELETE FROM templates WHERE id = %s;", (template_id,), commit=True)
