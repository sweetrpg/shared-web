# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""feedback_widget.py
Standalone preview page for the shared feedback-form widget (feedback-widget.js/.css) -
doubles as a manual test page and as the live copy of the README's embed snippet, so the
documented usage is exercised by something other than prose.
"""

from flask import Blueprint, current_app, render_template


# Registered directly on the app (not nested under the `web` blueprint) - a static preview page
# must render without a session, admin-api call, or maintenance-mode check.
blueprint = Blueprint("feedback_widget", __name__)


@blueprint.route("/widgets/feedback-preview")
def feedback_preview():
    context = {
        "shared_url": current_app.config.get("SHARED_URL"),
        "feedback_api_url": current_app.config.get("FEEDBACK_API_URL", "/api/0/feedback"),
    }
    return render_template("feedback_widget_preview.html", **context)
