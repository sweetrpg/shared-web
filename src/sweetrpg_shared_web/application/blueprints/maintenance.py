# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""maintenance.py
Shared maintenance page for the platform's *-web frontends. Frontends whose
`platform` or own `service` scope has an active maintenance-mode record redirect
(302) here instead of rendering their own page in-place.
"""

from flask import Blueprint, current_app, render_template, request
from flask_babel import force_locale, gettext as _

from sweetrpg_shared_web.application.i18n import SUPPORTED_LOCALES


# Registered directly on the app (not nested under the `web` blueprint), so it never runs
# through the maintenance-mode before_request hook - the shared destination must not
# redirect to itself in a loop when its own scope is under maintenance.
blueprint = Blueprint("maintenance", __name__)


@blueprint.route("/maintenance")
def maintenance_page():
    # The redirecting frontend passes the active record's content (and which frontend
    # originated the redirect) as query parameters, so this page renders from what it
    # was handed rather than re-querying admin-api itself.

    def render():
        context = {
            "label": request.args.get("label"),
            "description": request.args.get("description"),
            "starts_at": request.args.get("starts_at"),
            "ends_at": request.args.get("ends_at"),
            "service": request.args.get("service"),
            "shared_url": current_app.config.get("SHARED_URL"),
        }
        return render_template("maintenance.html", **context), 200

    locale = request.args.get("locale")
    if locale in SUPPORTED_LOCALES:
        # Only force a supported locale - babel raises UnknownLocaleError on an
        # unrecognized code, and an attacker-supplied query param must not 500 the page.
        with force_locale(locale):
            return render()
    return render()
