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
    400: ("A Garbled Missive", "Thy scroll bears words even our sages cannot parse."),
    401: ("Halt, Traveler", "Thou must prove thy identity before passing this gate."),
    403: ("The Gate Is Sealed", "Thy credentials do not grant passage beyond this ward."),
    404: ("Lost in the Mists", "No such chamber exists within these halls - the path thou seek has vanished."),
    500: ("A Curse Upon the Keep", "Something has gone dreadfully wrong within our walls."),
    502: ("The Messenger Was Waylaid", "The realm beyond could not be reached."),
    503: ("The Keep Is Under Siege", "Our halls are overwhelmed and cannot receive thee just now."),
    504: ("The Herald Never Returned", "We awaited word from afar, but none arrived in time."),
}

DEFAULT_COPY = ("By the Gods, Something Went Awry", "An unforeseen mishap has befallen this realm.")


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
