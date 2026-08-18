# Shared web

[![Unit tests](https://github.com/sweetrpg/shared-web/actions/workflows/python-ci.yml/badge.svg)](https://github.com/sweetrpg/shared-web/actions/workflows/python-ci.yml)
[![Coverage](https://github.com/sweetrpg/shared-web/blob/develop/coverage.svg)](https://github.com/sweetrpg/shared-web)
[![License](https://img.shields.io/github/license/sweetrpg/shared-web.svg)](https://img.shields.io/github/license/sweetrpg/shared-web.svg)
[![Issues](https://img.shields.io/github/issues/sweetrpg/shared-web.svg)](https://img.shields.io/github/issues/sweetrpg/shared-web.svg)
[![PRs](https://img.shields.io/github/issues-pr/sweetrpg/shared-web.svg)](https://img.shields.io/github/issues-pr/sweetrpg/shared-web.svg)
[![Dependabot](https://badgen.net/github/dependabot/sweetrpg/shared-web)](https://badgen.net/github/dependabot/sweetrpg/shared-web)
[![Deployment](https://argocd.dev.pilgrimagesoftware.com/api/badge?name=sweetrpg-shared-web&revision=true&showAppName=true&namespace=sweetrpg-system)](https://argocd.dev.pilgrimagesoftware.com/applications/sweetrpg-shared-web)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
[![Built with love](https://ForTheBadge.com/images/badges/built-with-love.svg)](https://ForTheBadge.com/images/badges/built-with-love.svg)

Flask service for cross-cutting concerns other `*-web` frontends would otherwise each maintain
their own copy of.

## Error pages

`GET /errors/<status_code>` renders a branded HTML page for a supported HTTP status code
(400, 401, 403, 404, 500, 502, 503, 504; anything else gets a generic fallback), with the
response's own status code set to match. Accepts two optional query parameters:

- `service` - the name of the frontend the visitor was trying to reach, shown on the page
- `request_id` - a correlation ID, shown on the page

Renders from static template content only - no database, cache, or `admin-api` call, so a
degraded dependency never breaks the error page itself.

Every other frontend reaches this via a Traefik `errors` Middleware in its own
`kubernetes/overlays/{dev,local}/middlewares.yaml`, not a direct link:

```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: errors-shared-web
spec:
  errors:
    status: ["400", "401", "403", "404", "500", "502", "503", "504"]
    query: /errors/{status}?service=<your-service-name>
    service:
      name: web-v1
      namespace: sweetrpg-shared
      port: 8081
```

wired into the frontend's `Ingress` via the `traefik.ingress.kubernetes.io/router.middlewares`
annotation. `assets-web` is the reference implementation. See `openspec/changes/shared-error-pages`
in `sweetrpg/platform` for the full design.

**Note**: `spec.errors.service.port` must be a bare integer/string - the named-port object form
(`{name: http}`) that regular Service selectors accept elsewhere in Traefik's CRDs fails CRD
validation for this specific field.

## Maintenance-mode banner

`_check_maintenance` in `application/blueprints/__init__.py` renders `maintenance.html` when an
active maintenance-mode record exists for the `platform`/`service:shared` scopes (via
`admin-api`). This is `shared-web`'s own maintenance display, gating access to `shared-web`
itself - distinct from the generic error pages above.

## Documentation

Documentation for this package can be found [here](https://sweetrpg.github.io/shared-web).
