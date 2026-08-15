# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Shared test fixtures.
"""

import os

import pytest

os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("SENTRY_DSN", "")
os.environ.setdefault("SHARED_URL", "localhost:8081")

from sweetrpg_shared_web.application.main import create_app  # noqa: E402


@pytest.fixture(scope="session")
def app():
    # create_app() registers Prometheus metrics against the global default
    # registry, so it can only be called once per process without colliding
    # on duplicate timeseries -- share a single app instance across every
    # test module via session scope.
    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture
def client(app):
    return app.test_client()
