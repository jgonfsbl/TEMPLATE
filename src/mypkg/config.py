#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=W0102,E0712,C0103,R0903

""" MYPKG """

__updated__ = "2024-10-31 21:27:05"


from os import environ
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class Config:
    """Set Flask configuration vars from .env file or environment variables"""

    # -- Flask general configuration
    FLASK_APP = environ.get("FLASK_APP", "app.py")
    FLASK_ENV = environ.get("FLASK_ENV", "production")
    FLASK_HOST = environ.get("FLASK_HOST", "localhost")
    FLASK_PORT = environ.get("FLASK_PORT", "5000")
    FLASK_DEBUG = environ.get("FLASK_DEBUG", "False").lower() == "true"

    # -- Flask special security functionality
    # -- A random key used to encrypt cookies and secure client-side sessions
    SECRET_KEY = environ.get("SECRET_KEY", "you-will-never-guess-me")

    # -- Logging
    # -- In this app the Flask logging capability has been disabled in favor
    # -- of a custom logger that writes to STDOUT thinking on execuring the
    # -- application in the form of a Docker container
    LOG_LEVEL = environ.get("LOG_LEVEL", "DEBUG")

    # -- Postgres database
    DB_ENGINE = environ.get("DB_ENGINE", "pg")
    DB_USER = environ.get("DB_USER", "root")
    DB_PASS = environ.get("DB_PASS", "password")
    DB_HOST = environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = environ.get("DB_PORT", "5432")
    DB_NAME = environ.get("DB_NAME", "database")

    # -- Redis database
    REDIS_HOST = environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = environ.get("REDIS_PORT", "6379")
    REDIS_PASS = environ.get("REDIS_PASS", "password")
    REDIS_DB = environ.get("REDIS_DB", 0)
    REDIS_MAX_CONN = environ.get("REDIS_MAX_CONN", "100 per minute")

    # -- Rate Limiting; default to 100 requests/minute
    DEFAULT_RATE_LIMIT = environ.get("DEFAULT_RATE_LIMIT", 100)

    # -- Prometheus integration
    PROMETHEUS_ENABLED = environ.get("PROMETHEUS_ENABLED", "False").lower() == "true"
    PROMETHEUS_DBLAT_TABLE=environ.get("PROMETHEUS_PROMETHEUS_DBLAT_TABLE", "templates")
    PROMETHEUS_DBLAT_COLUMN=environ.get("PROMETHEUS_DBLAT_COLUMN", "templateid")

    # -- AWS specific settings
    AWS_REGION = environ.get("eu-south-2")
    AWS_S3_BUCKET = environ.get("AWS_S3_BUCKET", "")
    AWS_S3_BUCKET_PREFIX = environ.get("AWS_S3_BUCKET_PREFIX", "")
