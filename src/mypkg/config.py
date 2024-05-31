#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0102,E0712,C0103,R0903
""" MYPKG """

__updated__ = "2024-05-31 13:07:20"

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
    SECRET_KEY = environ.get("SECRET_KEY" or "you-will-never-guess-me")

    # Database
    DB_ENGINE = environ.get("DATABASE_USER" or "pg")
    DB_USER = environ.get("DATABASE_USER" or "root")
    DB_PASS = environ.get("DATABASE_PASS" or "password")
    DB_HOST = environ.get("DATABASE_HOST" or "127.0.0.1")
    DB_PORT = environ.get("DATABASE_PORT" or "5432")
    DB_NAME = environ.get("DATABASE_NAME" or "lab")

    # API
    API_KEY = environ.get("API_KEY" or "you-will-never-guess-me")

    # Logging
    LOG_LEVEL = environ.get("LOG_LEVEL" or "DEBUG")
    LOG_FILE = environ.get("LOG_FILE" or "resources/tresa.log")
