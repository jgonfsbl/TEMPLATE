#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-07-04 17:28:36"


from marshmallow import Schema, fields, validate, validates, ValidationError


class Template_Schema(Schema):
    pass


class TemplateId_Schema(Schema):
    sessionid = fields.Str(
        required=True,
        validate=validate.Regexp(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", error="Invalid UUID4 format"
        ),
    )
