.PHONY: docs
init:
	uv sync --group test
test:
	# This runs all of the tests.
	uv run pytest
ci:
	uv run pytest --junitxml=report.xml

coverage:
	uv run pytest --verbose --cov-report term --cov-report xml --cov=sweetrpg_shared_web tests

docs:
	cd docs && uv run --group docs make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"
