# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Tests for the maintenance-mode before_request hook and the shared maintenance page.
"""

from urllib.parse import parse_qs, urlparse

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


def test_active_mode_redirects_to_shared_maintenance_page(app, client):
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

    # Maintenance is a deliberate state: redirect to the shared page, not a 503.
    assert response.status_code == 302
    url = urlparse(response.headers["Location"])
    assert url.path == "/maintenance" or url.path.endswith("/maintenance")
    query = parse_qs(url.query)
    assert query["service"] == ["shared-web"]
    assert query["label"] == ["Scheduled maintenance"]
    assert query["description"] == ["Upgrading infrastructure"]
    assert fetch_calls == [["platform", "service:shared"]]


def test_redirect_omits_empty_record_fields(app, client):
    app.admin_client.fetch_maintenance_modes = lambda scopes: [
        MaintenanceMode(
            scope_type="platform",
            scope_value="",
            label=None,
            description=None,
            starts_at=None,
            ends_at=None,
        )
    ]

    response = client.get("/")

    assert response.status_code == 302
    query = parse_qs(urlparse(response.headers["Location"]).query)
    assert set(query) == {"service"}


def test_normal_request_proceeds_when_no_maintenance_mode_active(app, client):
    app.admin_client.fetch_maintenance_modes = lambda scopes: []

    response = client.get("/")

    # The maintenance hook must not short-circuit; whatever status the route
    # itself returns is what the client sees.
    assert response.status_code != 503
    assert response.status_code != 302


def test_fail_open_when_admin_client_missing(app, client):
    """If the admin client was never attached, the app must behave normally."""
    saved_client = app.admin_client
    del app.admin_client
    try:
        response = client.get("/")
        assert response.status_code != 503
        assert response.status_code != 302
    finally:
        app.admin_client = saved_client


def test_shared_maintenance_page_responds_200_with_record_content(client):
    response = client.get(
        "/maintenance?service=catalog-web"
        "&label=Scheduled+maintenance"
        "&description=Back+soon"
        "&starts_at=2026-08-01T00%3A00%3A00Z"
        "&ends_at=2026-08-01T02%3A00%3A00Z"
    )

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Scheduled maintenance" in body
    assert "Back soon" in body
    assert "2026-08-01T00:00:00Z" in body
    assert "2026-08-01T02:00:00Z" in body
    assert "catalog-web" in body


def test_shared_maintenance_page_renders_without_query_params(client):
    response = client.get("/maintenance")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "<h1>" in body
