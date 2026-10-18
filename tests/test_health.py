# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Tests that health probes stay up when the session store is unavailable.
"""

import pytest
import redis


@pytest.fixture
def unreachable_session_store(app):
    original_client = app.session_interface.client
    # Nothing listens on port 1, so any session read or write fails with a connection error.
    app.session_interface.client = redis.Redis(host="localhost", port=1)
    yield
    app.session_interface.client = original_client


def test_health_ping_succeeds_when_redis_is_down(client, unreachable_session_store):
    """A Redis outage must not fail the liveness/readiness probes, or the pod crash-loops."""
    response = client.get("/health/ping")

    assert response.status_code == 200
