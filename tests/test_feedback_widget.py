# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
Tests for the shared feedback-form widget's preview page.
"""


def test_preview_page_renders(client):
    response = client.get("/widgets/feedback-preview")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "feedback-widget.js" in body
    assert "feedback-widget.css" in body


def test_preview_page_passes_configured_api_url(app, client):
    app.config["FEEDBACK_API_URL"] = "https://api.admin.dev.sweetrpg.com/api/0/feedback"

    response = client.get("/widgets/feedback-preview")

    body = response.get_data(as_text=True)
    assert 'data-api-url="https://api.admin.dev.sweetrpg.com/api/0/feedback"' in body


def test_preview_page_defaults_api_url_when_unconfigured(app, client):
    app.config.pop("FEEDBACK_API_URL", None)

    response = client.get("/widgets/feedback-preview")

    body = response.get_data(as_text=True)
    assert 'data-api-url="/api/0/feedback"' in body


def test_feedback_preview_route_returns_html(client):
    response = client.get("/widgets/feedback-preview")
    assert response.content_type.startswith("text/html")
