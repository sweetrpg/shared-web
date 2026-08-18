# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Tests for the shared branded error-page endpoint.
"""

import pytest

from markupsafe import escape

from sweetrpg_shared_web.application.blueprints.errors import DEFAULT_COPY, STATUS_COPY


@pytest.mark.parametrize("status_code", sorted(STATUS_COPY))
def test_supported_status_code_renders(client, status_code):
    response = client.get(f"/errors/{status_code}")

    assert response.status_code == status_code
    heading, description = STATUS_COPY[status_code]
    body = response.get_data(as_text=True)
    assert heading in body
    assert str(escape(description)) in body


def test_unsupported_status_code_falls_back(client):
    response = client.get("/errors/418")

    assert response.status_code == 418
    body = response.get_data(as_text=True)
    assert DEFAULT_COPY[0] in body


def test_service_and_request_id_render_when_present(client):
    response = client.get("/errors/404?service=catalog-web&request_id=abc-123")

    body = response.get_data(as_text=True)
    assert "catalog-web" in body
    assert "abc-123" in body


def test_service_and_request_id_omitted_when_absent(client):
    response = client.get("/errors/404")

    assert response.status_code == 404
    body = response.get_data(as_text=True)
    assert STATUS_COPY[404][0] in body
    assert "Request ID" not in body


def test_renders_shared_branding_assets(app, client):
    response = client.get("/errors/404")

    body = response.get_data(as_text=True)
    # shared_url = app.config["SHARED_URL"]
    assert f"/static/css/main.css" in body
    assert f"/static/img/sweetrpg-logo-black.svg" in body
