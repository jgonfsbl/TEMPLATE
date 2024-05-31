#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-05-12 19:24:37"


from marshmallow import Schema, fields, validate, validates, ValidationError


class templateSchema(Schema):
    """Schema for the templates table.

    Args:
        Schema (_type_): _description_

    Raises:
        ValidationError: _description_
        ValidationError: _description_
        ValidationError: _description_
    """

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(required=True, validate=validate.Length(min=1, max=100))
    content = fields.String(required=True, validate=validate.Length(min=1, max=1000))

    @validates("name")
    def validate_name(self, value):
        """Validate the name field"""
        if value == "bad":
            raise ValidationError("Name cannot be 'bad'")

    @validates("description")
    def validate_description(self, value):
        """Validate the description field"""
        if value == "bad":
            raise ValidationError("Description cannot be 'bad'")

    @validates("content")
    def validate_content(self, value):
        """Validate the content field"""
        if value == "bad":
            raise ValidationError("Content cannot be 'bad'")
