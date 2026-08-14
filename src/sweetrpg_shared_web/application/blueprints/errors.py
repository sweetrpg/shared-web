# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""errors.py
Branded HTML error pages for the platform's *-web frontends, reached via each
frontend's Traefik `errors` middleware rather than per-frontend code.
"""

from flask import Blueprint, current_app, render_template, request


# Registered directly on the app (not nested under the `web` blueprint), so it never runs
# through the maintenance-mode/session/analytics before_request hooks - an error page must
# render from static content only, never depend on admin-api or any other external call.
blueprint = Blueprint("errors", __name__)

STATUS_COPY = {
    400: ("Bad Request", "The request could not be understood."),
    401: ("Unauthorized", "You need to sign in to view this page."),
    403: ("Forbidden", "You don't have permission to view this page."),
    404: ("Not Found", "The page you're looking for doesn't exist."),
    500: ("Internal Server Error", "Something went wrong on our end."),
    502: ("Bad Gateway", "The service is temporarily unreachable."),
    503: ("Service Unavailable", "The service is temporarily unavailable."),
    504: ("Gateway Timeout", "The service took too long to respond."),
}

DEFAULT_COPY = ("Something Went Wrong", "An unexpected error occurred.")


@blueprint.route("/errors/<int:status_code>")
def error_page(status_code):
    heading, description = STATUS_COPY.get(status_code, DEFAULT_COPY)
    context = {
        "status_code": status_code,
        "heading": heading,
        "description": description,
        "service": request.args.get("service"),
        "request_id": request.args.get("request_id"),
        "shared_assets_url": current_app.config.get("SHARED_ASSETS_URL"),
    }
    return render_template("error.html", **context), status_code
