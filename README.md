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

## Feedback form widget

A shared "Report a problem / request a feature" widget, embeddable by any `*-web` frontend
regardless of its own templating stack (Flask, Rust+Askama, etc.) - see
`openspec/changes/add-anonymous-feedback-reporting` in `sweetrpg/platform`. The widget mounts
its own markup via plain JS (`static/js/feedback-widget.js` + `static/css/feedback-widget.css`),
so the host frontend only needs to include two tags:

```html
<link rel="stylesheet" href="https://shared.dev.sweetrpg.com/static/css/feedback-widget.css">
<script
  src="https://shared.dev.sweetrpg.com/static/js/feedback-widget.js"
  data-api-url="https://api.admin.dev.sweetrpg.com/api/0/feedback"
  defer
></script>
```

With nothing else, the widget injects a floating "Report a problem / request a feature" button
in the bottom-right corner that opens the form in a modal. Live preview: `GET
/widgets/feedback-preview` on this service (also the page these docs are verified against).

### Config (script tag `data-*` attributes)

| Attribute | Required | Description |
| --- | --- | --- |
| `data-api-url` | yes | Full URL of `admin-api`'s `POST /feedback` endpoint |
| `data-trigger-selector` | no | CSS selector for a host-provided trigger element; when set, the widget wires clicks on matching elements instead of injecting its own floating button |
| `data-trigger-label` | no | Label for the auto-injected trigger button (default: "Report a problem / request a feature") |
| `data-source` | no | Value sent as the submission's `source` field (default: `location.hostname + location.pathname`) |

A host can also open the dialog programmatically (e.g. from a nav menu item) via
`window.SweetRPGFeedbackWidget.open()`.

### Request contract

On submit, the widget `POST`s this JSON body to `data-api-url`:

```json
{
  "type": "bug",
  "title": "...",
  "body": "...",
  "reporter_email": "optional",
  "source": "catalog-web/volumes/123",
  "website": "",
  "rendered_at": "2026-10-06T22:00:00.000Z"
}
```

- `type` is `"bug"` or `"feature"`.
- `website` is a honeypot field - always empty for a real user; a non-empty value indicates a
  bot that filled every field.
- `rendered_at` is when the dialog was opened (ISO 8601) - the backend computes elapsed time
  against the request's arrival to reject submissions completed faster than a human plausibly
  could.
- `title` is capped at 200 characters, `body` at 5000, enforced client-side via `maxlength` and
  expected to be enforced again server-side (never trust client-side limits alone).

### States

- **Success**: shows a `banner-success` confirmation inside the dialog and clears the title,
  body, email, and honeypot fields for a fresh submission.
- **Error**: shows a `banner-error` message inside the dialog (validation, rate limit, or
  backend failure) and preserves whatever the user typed.

### Accessibility and theming

- Every control (type selector, title, body, email, submit, cancel) is reachable and operable
  via keyboard alone; `Tab`/`Shift+Tab` is trapped within the open dialog, `Escape` closes it,
  and focus returns to whatever triggered it on close.
- Colors come entirely from `main.css`'s `--color-*` custom properties and existing
  `.input`/`.btn`/`.banner-*` classes, so the widget inherits the host's light/dark theme and
  the same contrast guarantees as the rest of the design system rather than carrying its own
  palette.

## Documentation

Documentation for this package can be found [here](https://sweetrpg.github.io/shared-web).
