# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""errors.py
Branded HTML error pages for the platform's *-web frontends, reached via each
frontend's Traefik `errors` middleware rather than per-frontend code.
"""

from flask import Blueprint, current_app, render_template, request
from flask_babel import force_locale, gettext as _

from sweetrpg_shared_web.application.i18n import SUPPORTED_LOCALES


# Registered directly on the app (not nested under the `web` blueprint), so it never runs
# through the maintenance-mode/session/analytics before_request hooks - an error page must
# render from static content only, never depend on admin-api or any other external call.
blueprint = Blueprint("errors", __name__)

# Per-status locale keys (`errors.<code>.heading` / `errors.<code>.description` in
# translations/<locale>/LC_MESSAGES/messages.po) and the error-icon variant to render.
STATUS_KEYS = {
    400: 2,
    401: 1,
    403: 1,
    404: 3,
    409: 1,
    413: 2,
    500: 1,
    502: 2,
    503: 1,
    504: 3,
}

DEFAULT_ICON = 0


@blueprint.route("/errors/<int:status_code>")
def error_page(status_code):
    # Unmapped status codes fall back to the generic copy rather than rendering a raw
    # locale key - gettext returns the key itself for a missing translation.
    key = status_code if status_code in STATUS_KEYS else "default"
    icon = STATUS_KEYS.get(status_code, DEFAULT_ICON)
    # Traefik proxies these requests server-to-server, so there's no browser cookie for the
    # visitor's locale - the proxying frontend passes it explicitly as a query parameter
    # (see the `shared-error-pages` spec delta). Falls back to the normal resolution order.

    def render():
        context = {
            "status_code": status_code,
            "icon": icon,
            "heading": _(f"errors.{key}.heading"),
            "description": _(f"errors.{key}.description"),
            "service": request.args.get("service"),
            "request_id": request.args.get("request_id"),
            "request_id_label": _("Request ID:"),
            "shared_url": current_app.config.get("SHARED_URL"),
        }
        return render_template("error.html", **context), status_code

    locale = request.args.get("locale")
    if locale in SUPPORTED_LOCALES:
        # Only force a supported locale - babel raises UnknownLocaleError on an
        # unrecognized code, and an attacker-supplied query param must not 500 the page.
        with force_locale(locale):
            return render()
    return render()
