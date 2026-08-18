# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""main.py

Creates a Flask app instance and registers various services and middleware.
"""

from pathlib import Path
from flask import Flask, session, g
from flask_cors import CORS
from flask_session import Session
from dotenv import load_dotenv, find_dotenv
from sweetrpg_shared_web.application.cache import cache
from sweetrpg_shared_web.application import constants
from sweetrpg_shared_web.application.tracing import setup_tracing
from logging.config import dictConfig
from redis.client import Redis
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
from sweetrpg_admin_api_client import AdminClient
import analytics
import os
from prometheus_flask_exporter import PrometheusMetrics
import sweetrpg_shared_web


# Flask is constructed with app_name (a plain string, not this module's __name__), so it
# cannot infer root_path from an importable module and would otherwise fall back to the
# process's current working directory -- fragile, since that differs between `pytest`
# (repo root) and the Docker image (WORKDIR /app == src/). Point template_folder at the
# package's templates directory directly so template lookup is independent of cwd.
TEMPLATE_DIR = str(Path(__file__).resolve().parent.parent.parent / "templates")

ENV_FILE = find_dotenv()
if ENV_FILE:
    print(f"Loading environment from {ENV_FILE}...")
    load_dotenv(ENV_FILE)


def create_app(app_name=constants.APPLICATION_NAME):
    print("Configuring logging...")
    dictConfig(
        {
            "version": 1,
            "formatters": {
                # One JSON object per line to stdout - matches the Go/Swift services'
                # structured-logging convention so log aggregation parses all of them the same
                # way.
                "json": {
                    "class": "pythonjsonlogger.json.JsonFormatter",
                    "format": "%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s",
                },
            },
            "handlers": {
                "wsgi": {"class": "logging.StreamHandler", "stream": "ext://flask.logging.wsgi_errors_stream", "formatter": "json"},
            },
            "root": {
                "level": os.environ.get(constants.LOG_LEVEL) or "INFO",
                "handlers": [
                    "wsgi",
                ],
            },
        }
    )

    app = Flask(app_name, template_folder=TEMPLATE_DIR)
    app.debug = app.config.get(constants.DEBUG, False)
    app.config.from_object("sweetrpg_shared_web.application.config.BaseConfig")
    # env = DotEnv(app)

    app.logger.info("Setting up cache...")
    cache.init_app(app)

    app.logger.info("Setting up metrics...")
    metrics = PrometheusMetrics(app)
    # static information as metric
    metrics.info('app_info', sweetrpg_shared_web.__name__, version=sweetrpg_shared_web.__version__, build=sweetrpg_shared_web.__build__)

    app.logger.info("Setting up tracing...")
    setup_tracing(app)

    app.logger.info("Setting up admin-api client...")
    # constructed once and reused; fail-open (returns [] on any error, including no base_url set)
    app.admin_client = AdminClient(base_url=app.config.get(constants.ADMIN_API_URL))

    app.logger.info("Setting up analytics...")
    analytics.write_key = app.config.get(constants.SEGMENT_WRITE_KEY)
    analytics.debug = app.config.get(constants.DEBUG, False)

    app.logger.info("Setting up session manager...")
    session = Session(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    if not app.debug:
        app.logger.info("Setting up Sentry...")
        sentry = SentryWsgiMiddleware(app)

    app.logger.info("Setting up endpoints...")

    from sweetrpg_shared_web.application.blueprints import blueprint as main_blueprint
    from sweetrpg_shared_web.application.blueprints.errors import blueprint as errors_blueprint

    from sweetrpg_web_core.blueprints.health import blueprint as health_blueprint
    main_blueprint.register_blueprint(health_blueprint)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(errors_blueprint)

    # app.wsgi_app = SassMiddleware(app.wsgi_app, {
    #     'application': ('static/sass', 'static/css', '/static/css')
    # })
    # scss = Scss(app, static_dir='static', asset_dir='assets')

    # register_metrics(app, app_version=config["version"], app_config=config["config"])

    print(app.url_map)

    return app
