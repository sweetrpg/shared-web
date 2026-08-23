# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Tests for the shared branded error-page endpoint.
"""

import pytest

from sweetrpg_shared_web.application.blueprints.errors import STATUS_KEYS


@pytest.mark.parametrize("status_code", sorted(STATUS_KEYS))
def test_supported_status_code_renders(client, status_code):
    response = client.get(f"/errors/{status_code}")

    assert response.status_code == status_code
    body = response.get_data(as_text=True)
    # English copy comes from the locale catalog; a missing key would render the raw
    # `errors.<code>.*` key text instead of prose.
    assert f"errors.{status_code}." not in body
    assert "<h1>" in body


def test_unsupported_status_code_falls_back(client):
    response = client.get("/errors/418")

    assert response.status_code == 418
    body = response.get_data(as_text=True)
    assert "By the Gods, Something Went Awry" in body
    assert "errors.418." not in body


def test_service_and_request_id_render_when_present(client):
    response = client.get("/errors/404?service=catalog-web&request_id=abc-123")

    body = response.get_data(as_text=True)
    assert "catalog-web" in body
    assert "abc-123" in body


def test_service_and_request_id_omitted_when_absent(client):
    response = client.get("/errors/404")

    assert response.status_code == 404
    body = response.get_data(as_text=True)
    assert "Request ID" not in body


def test_locale_query_param_is_accepted_and_does_not_break_rendering(app, client):
    # Only English ships today; an explicit locale param must still render complete copy.
    response = client.get("/errors/404?locale=en")

    assert response.status_code == 404
    body = response.get_data(as_text=True)
    assert "Lost in the Mists" in body


def test_locale_query_param_with_unknown_locale_falls_back_to_english(client):
    response = client.get("/errors/404?locale=zz")

    assert response.status_code == 404
    body = response.get_data(as_text=True)
    assert "Lost in the Mists" in body


def test_renders_shared_branding_assets(app, client):
    response = client.get("/errors/404")

    body = response.get_data(as_text=True)
    # shared_url = app.config["SHARED_URL"]
    assert "/static/css/main.css" in body
    assert "/static/img/sweetrpg-error-3-black.svg" in body
