#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0102,E0712,C0103,R0903
""" MYPKG """

__updated__ = "2024-07-04 14:43:51"

from os import environ
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    """Set Flask configuration vars from .env file or environment variables"""

    # General
    FLASK_APP = environ.get("FLASK_APP" or "app.py")
    FLASK_ENV = environ.get("FLASK_ENV" or "production")
    FLASK_DEBUG = environ.get("FLASK_DEBUG" or "False")
    FLASK_HOST = environ.get("FLASK_HOST" or "localhost")
    FLASK_PORT = environ.get("FLASK_PORT" or "5000")

    # API
    API_KEY = environ.get("FLASK_API_KEY" or "you-will-never-guess-me")
    SECRET_KEY = environ.get("FLASK_SECRET_KEY" or "you-will-never-guess-me")

    # Logging
    LOG_LEVEL = environ.get("FLASK_LOG_LEVEL" or "DEBUG")

    # Database
    DB_ENGINE = environ.get("DB_ENGINE" or "pg")
    DB_USER = environ.get("DB_USER" or "root")
    DB_PASS = environ.get("DB_PASS" or "password")
    DB_HOST = environ.get("DB_HOST" or "127.0.0.1")
    DB_PORT = environ.get("DB_PORT" or "5432")
    DB_NAME = environ.get("DB_NAME" or "database")
