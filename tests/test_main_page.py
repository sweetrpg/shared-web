# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Tests for the shared-web landing page at `/`.
"""


def test_main_page_renders_placeholder(app, client):
    # Regression: `main_page` rendered "index.html", which didn't exist in
    # src/templates/, so every `GET /` (i.e. dev.sweetrpg.com/shared) raised
    # jinja2.TemplateNotFound and returned 500.
    app.admin_client.fetch_maintenance_modes = lambda scopes: []

    response = client.get("/")

    assert response.status_code == 200
    assert b"SweetRPG Shared" in response.data
