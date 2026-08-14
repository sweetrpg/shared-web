# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
config.py
- settings for the flask application object
"""


import os
import redis
import random
import hashlib
from sweetrpg_shared_web.application import constants


def _env_bool(name: str, default: bool) -> bool:
    """Parse a boolean env var. `os.environ.get(name) or default` doesn't work for this - any
    non-empty string (including "false") is truthy, so that pattern always evaluates true once
    the var is set at all, regardless of its value.
    """
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _redis_url(db: int) -> str:
    host = os.environ[constants.REDIS_HOST]
    port = int(os.environ.get(constants.REDIS_PORT) or 6379)
    password = os.environ.get(constants.REDIS_PASS)
    auth = f":{password}@" if password else ""
    return f"redis://{auth}{host}:{port}/{db}"


class BaseConfig(object):
    DEBUG = _env_bool(constants.DEBUG, False)
    PORT = os.environ.get(constants.PORT) or 5000
    ASSETS_DEBUG = True
    LOG_LEVEL = os.environ.get(constants.LOG_LEVEL) or "INFO"
    # used for encryption and session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or hashlib.sha256(f"{random.random()}".encode('utf-8')).hexdigest()
    CSRF_TOKEN = os.environ.get('CSRF_TOKEN') or hashlib.sha256(f"{random.random()}".encode('utf-8')).hexdigest()
    CACHE_REDIS_HOST = os.environ[constants.REDIS_HOST]
    CACHE_REDIS_PORT = int(os.environ.get(constants.REDIS_PORT) or 6379)
    CACHE_REDIS_DB = int(os.environ.get(constants.REDIS_DB) or 7)
    # None (not "") when unset, so redis-py skips the AUTH command entirely rather than sending
    # an empty password.
    CACHE_REDIS_PASSWORD = os.environ.get(constants.REDIS_PASS) or None
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url(_redis_url(int(os.environ.get(constants.REDIS_DB) or 7)))
    SEGMENT_WRITE_KEY = os.environ.get(constants.SEGMENT_WRITE_KEY)
    # base URL for admin-api; unset/empty disables the client (fail-open, no banners/maintenance checks)
    ADMIN_API_URL = os.environ.get(constants.ADMIN_API_URL)
    # base URL for shared branding assets (logo, favicon, stylesheet) - see
    # docs/frontend-conventions.md. Defaults to a local assets-web instance's own address,
    # matching every other frontend's fallback.
    SHARED_ASSETS_URL = os.environ.get(constants.SHARED_ASSETS_URL) or "http://localhost:8081"
