# AGENTS.md

This file provides guidance to Claude Code, Codex, GitHub Copilot, and other coding agents
working in this repository.

## About This Project

`shared-web` is a Flask service that renders cross-cutting HTML pages other `*-web` frontends
would otherwise have to duplicate. Today that's the maintenance-mode banner
(`_check_maintenance` in `application/blueprints/__init__.py`, gated on `admin-api`'s active
maintenance-mode records for the `platform`/`service:shared` scopes). The
`shared-error-pages` OpenSpec change (`sweetrpg/platform`'s `openspec/changes/shared-error-pages`)
adds branded 400/401/403/404/500/502/503/504 error pages here next, reached via each frontend's
Traefik `Ingress`/`Middleware` rather than per-frontend code - see that change's `design.md` for
why a shared service is used instead of a shared Python library (this repo's sibling frontends
aren't all Python; `main-web` is Rust).

Depends on `sweetrpg/admin-api-client.py` (the maintenance-mode/banner client) and
`sweetrpg/web-core` (`sweetrpg-web-core`, shared Flask helpers used across the platform's Python
frontends).

## Localization

User-facing strings come from `translations/<code>/LC_MESSAGES/messages.po` via Flask-Babel,
never hardcoded in templates (`{{ _('...') }}` in Jinja, `_('...')` in view code). English is
the default/fallback locale; add a new locale by creating a new catalog under
`translations/<code>/` (compile with `pybabel compile`) and adding its code to
`SUPPORTED_LOCALES` in `src/sweetrpg_shared_web/application/i18n.py`. Locale resolution per
request: `locale` query parameter (error pages - they're rendered server-to-server via
Traefik's errors middleware, so there's no browser cookie), then `locale` cookie override,
then `Accept-Language`, then English. Error-page copy is keyed per status code
(`errors.<code>.heading`/`.description`, with `errors.default.*` for unmapped codes) - see the
`web-frontend-localization` and `shared-error-pages` specs in `sweetrpg/platform`'s
`openspec/changes/full-localization-web-apps`. CI runs `scripts/check-template-strings.sh`
(`locale-lint` job), which fails on literal text between HTML tags that isn't a whitelisted
brand string or wrapped in a gettext call.

## Committing Code

[Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <description>`.

## Branches and Workflow

Git-flow (see `docs/git-flow.md` in `sweetrpg/platform`): `develop` is the integration branch,
`master` reflects the latest release. Feature/fix branches off `develop`, PR back into `develop`.

## Running Checks Locally

```bash
pip install -r requirements/tests.txt -e .
python -m pytest tests
```

Requires a local Redis (`redis-server` on `localhost:6379`, no auth needed) - used for caching
and sessions.
