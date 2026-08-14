# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Tests for the maintenance-mode before_request hook.
"""

from sweetrpg_admin_api_client import MaintenanceMode


def test_health_endpoint_is_never_gated(app, client):
    """Health checks must always pass, even during a maintenance window."""
    app.admin_client.fetch_maintenance_modes = lambda scopes: [
        MaintenanceMode(
            scope_type="platform",
            scope_value="",
            label="Scheduled maintenance",
            description="Upgrading infrastructure",
            starts_at="2026-08-01T00:00:00Z",
            ends_at=None,
        )
    ]

    response = client.get("/health/status")

    assert response.status_code == 200


def test_maintenance_page_renders_when_mode_active(app, client):
    fetch_calls = []

    def fake_fetch(scopes):
        fetch_calls.append(scopes)
        return [
            MaintenanceMode(
                scope_type="platform",
                scope_value="",
                label="Scheduled maintenance",
                description="Upgrading infrastructure",
                starts_at="2026-08-01T00:00:00Z",
                ends_at="2026-08-01T02:00:00Z",
            )
        ]

    app.admin_client.fetch_maintenance_modes = fake_fetch

    response = client.get("/")

    assert response.status_code == 503
    body = response.get_data(as_text=True)
    assert "Scheduled maintenance" in body
    assert "Upgrading infrastructure" in body
    assert fetch_calls == [["platform", "service:shared"]]


def test_normal_request_proceeds_when_no_maintenance_mode_active(app, client):
    app.admin_client.fetch_maintenance_modes = lambda scopes: []

    response = client.get("/")

    # The maintenance hook must not short-circuit; whatever status the route
    # itself returns is what the client sees.
    assert response.status_code != 503


def test_fail_open_when_admin_client_missing(app, client):
    """If the admin client was never attached, the app must behave normally."""
    saved_client = app.admin_client
    del app.admin_client
    try:
        response = client.get("/")
        assert response.status_code != 503
    finally:
        app.admin_client = saved_client
