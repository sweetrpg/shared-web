from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="sweetrpg-shared-web",
    install_requires=[
        "analytics-python~=1.0",
        "blinker~=1.0",
        "Flask-Caching~=2.0",
        "Flask-CORS~=5.0",
        "Flask-DotEnv~=0.1",
        "Flask-Session~=0.5",
        "Flask~=3.0",
        "hiredis~=3.0",
        "prometheus-flask-exporter~=0.22",
        "python-dateutil~=2.0",
        "python-dotenv~=1.0",
        "python-editor~=1.0",
        "python-logstash-async~=2.5",
        "PyYAML~=6.0",
        "hiredis~=3.0",
        "requests~=2.0",
        "sentry-sdk[flask]~=2.0",
        "sweetrpg-web-core",
        "sweetrpg-admin-api-client",
        "urllib3~=2.0",
    ],
    extras_require={},
)
