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
    400: ("A Garbled Missive", "Thy scroll bears words even our sages cannot parse.", 2),
    401: ("Halt, Traveler", "Thou must prove thy identity before passing this gate.", 1),
    403: ("The Gate Is Sealed", "Thy credentials do not grant passage beyond this ward.", 1),
    404: ("Lost in the Mists", "No such chamber exists within these halls - the path thou seek has vanished.", 3),
    409: ("Two Hands, One Scroll", "Another has already altered this record - thy changes clash with theirs.", 1),
    413: ("Thy Scroll Overflows", "The missive thou hast sent is too vast for our couriers to bear.", 2),
    500: ("A Curse Upon the Keep", "Something has gone dreadfully wrong within our walls.", 1),
    502: ("The Messenger Was Waylaid", "The realm beyond could not be reached.", 2),
    503: ("The Keep Is Under Siege", "Our halls are overwhelmed and cannot receive thee just now.", 1),
    504: ("The Herald Never Returned", "We awaited word from afar, but none arrived in time.", 3),
}

DEFAULT_COPY = ("By the Gods, Something Went Awry", "An unforeseen mishap has befallen this realm.", 0)


@blueprint.route("/errors/<int:status_code>")
def error_page(status_code):
    heading, description, icon = STATUS_COPY.get(status_code, DEFAULT_COPY)
    context = {
        "status_code": status_code,
        "icon": icon,
        "heading": heading,
        "description": description,
        "service": request.args.get("service"),
        "request_id": request.args.get("request_id"),
        "shared_url": current_app.config.get("SHARED_URL"),
        "assets_url": current_app.config.get("ASSETS_URL"),
    }
    return render_template("error.html", **context), status_code
