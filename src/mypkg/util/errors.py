#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """


__updated__ = "2024-10-31 21:12:58"


def format_error_message(error_dict):
    """
    Parse the internal error messages and format them for using them in a JSON response.

    The errors are presented in a dictionary where the keys are the field names and the values are the error messages
    for that field. The error messages can be either a string or a list of strings.

    The function will iterate over the dictionary and create a list of strings where each string is an error message
    in the format "field: error message". If the error message is a list, it will be joined with a comma and a space.

    :param error_dict: The dictionary of errors
    :return: A string with the error messages separated by newline characters
    """
    error_messages = []
    for field, errors in error_dict.items():
        if isinstance(errors, dict):
            # If the errors are a dictionary, iterate over the items and create a string for each item
            for index, field_errors in errors.items():
                for error, error_value in field_errors.items():
                    error_value_string = ", ".join(error_value) if isinstance(error_value, list) else error_value
                    error_messages.append(f"{field}[{index}].{error}: {error_value_string}")
        else:
            # If the errors are a list, iterate over the list and create a string for each item
            for error in errors:
                error_value_string = ", ".join(error) if isinstance(error, list) else error
                error_messages.append(f"{field}: {error_value_string}")
    return "\n".join(error_messages)
