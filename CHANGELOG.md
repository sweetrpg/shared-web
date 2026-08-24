## [0.15.0] - 2026-08-24

### 🚀 Features

- *(css)* Add volume tab strip and panel styles for catalog detail page

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.14.1
## [0.14.1] - 2026-08-24

### 🐛 Bug Fixes

- *(ci)* Use uv install/test commands in the release workflow
- *(ci)* Scope release test command to the tests directory
- *(deps)* Restore uwsgi runtime dependency lost in the uv migration

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.14.0
## [0.14.0] - 2026-08-24

### 🚀 Features

- *(css)* Add .form-hint helper style (sweetrpg/admin-web#22)
- *(i18n)* Extract user-facing strings into Flask-Babel catalogs
- *(maintenance)* Redirect to shared maintenance page instead of rendering 503 in-place

### 🐛 Bug Fixes

- *(ci)* Generate coverage data for the report steps
- *(css)* Horizontal layout for volume detail association blocks

### 💼 Other

- *(deps)* Migrate to uv for dependency management and task running
- Resolve conflicts with develop (i18n); port flask-babel dep to pyproject

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.13.2
- Clean up a bunch of old static files
## [0.13.2] - 2026-08-21

### 🐛 Bug Fixes

- Move CSS from catalog into here
- *(ci)* Potential fix for code scanning alert no. 1: Workflow does not contain permissions

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.13.1
## [0.13.1] - 2026-08-21

### 🐛 Bug Fixes

- *(css)* Recolor destructive icon-btn icons with the danger palette, brighten background

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.13.0
## [0.13.0] - 2026-08-21

### 🚀 Features

- *(static)* Add cover placeholder images for catalog-web
- *(css)* Add pagination footer styles for browse pages

### 🐛 Bug Fixes

- *(tests)* Update error-page tests for the 3-tuple STATUS_COPY

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.12.0
## [0.12.0] - 2026-08-21

### 🚀 Features

- *(assets)* Add sweetrpg error SVG images
- *(errors)* Add themed error icons to error pages
- *(css)* Add .icon-btn-danger for destructive icon-button actions

### 🐛 Bug Fixes

- *(tests)* Match STATUS_COPY's 3-tuple shape and the actual error-page icon asset

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.11.0
- *(static)* Remove build-info.json file
## [0.11.0] - 2026-08-21

### 🚀 Features

- *(catalog)* Use capsule button shape app-wide, not just volume edit

### 🐛 Bug Fixes

- *(css)* Add missing .page-header-toolbar layout rule
- *(catalog)* Use a round rect for buttons, not a full capsule
- *(catalog)* Remove the top nav's divider line
- *(tracing)* Use bare "shared-web" for the OTel service.name

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.10.0
## [0.10.0] - 2026-08-20

### 🚀 Features

- *(catalog)* Color page titles with catalog's accent

### 🐛 Bug Fixes

- *(css)* Center icon-btn contents horizontally, not just vertically
- *(kubernetes)* Fix cpu resource limit quantity that never matched ArgoCD's applied manifest
- *(css)* Center icon-btn contents, add page-header-toolbar layout

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.9.0
## [0.9.0] - 2026-08-19

### 🚀 Features

- Add shared app-switcher grid JS/CSS

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.8.1
## [0.8.1] - 2026-08-19

### 🐛 Bug Fixes

- *(css)* Use secondary text opacity for volume detail description

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.8.0
## [0.8.0] - 2026-08-19

### 🚀 Features

- *(icons)* Add history icon, matching edit.svg's style

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.7.0
## [0.7.0] - 2026-08-19

### 🚀 Features

- *(errors)* Add branded copy for 409 Conflict and 413 Payload Too Large

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.6.3
## [0.6.3] - 2026-08-18

### 🐛 Bug Fixes

- *(deps)* Add opentelemetry packages to deploy requirements

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.6.0
- *(release)* Merge master into develop after v0.6.1
- *(release)* Merge master into develop after v0.6.2
## [0.6.2] - 2026-08-18

### 🐛 Bug Fixes

- *(deps)* Add python-json-logger to deploy requirements
## [0.6.1] - 2026-08-18

### 🐛 Bug Fixes

- *(deps)* Add opentelemetry packages to deploy requirements
## [0.6.0] - 2026-08-18

### 🚀 Features

- *(observability)* Add structured JSON logging and OTel tracing
- *(theme)* Add theme.css with brand accent color override
- Merge broadsheet.css design tokens into main.css
- *(catalog)* Style the license detail page's two-column layout
- *(config)* Add SHARED_URL to dev configmap
- *(kubernetes)* Add auto-reload annotation to web deployment

### 🐛 Bug Fixes

- *(deployment)* Remove unused secret and config, enable health probes
- *(deployment)* Remove unused secret and config, enable health probes

### 📚 Documentation

- *(readme)* Add ArgoCD deployment status badge

### 🎨 Styling

- Add theme.css files with consistent color-accent override

### ⚙️ Miscellaneous Tasks

- *(release)* 0.5.1
## [0.5.1] - 2026-08-17

### 🎨 Styling

- *(css)* Add hub page layout and dark theme styles

### ⚙️ Miscellaneous Tasks

- Remove unneeded secrets


## [0.5.0] - 2026-08-16

### 🚀 Features

- *(error)* Style error status and meta in error template

### 🐛 Bug Fixes

- *(template)* Replace shared_assets_url with shared_url in error template

### 🎨 Styling

- *(error)* Increase error status font size to 120px

### ⚙️ Miscellaneous Tasks

- *(release)* Merge master into develop after v0.4.1
- *(workflow)* Install pip-tools in update-reqs workflow


## [0.4.1] - 2026-08-15

### 🧪 Testing

- Remove unused test file
- Add SHARED_URL env var to conftest.py
- Use relative paths in error template assertions

### ⚙️ Miscellaneous Tasks

- Upgrade to Python 3.14, switch to uv, add coverage reporting
- Remove docs CI job and update Sphinx dependencies


## [0.4.0] - 2026-08-15

### 🚀 Features

- *(dev)* Update configmap with shared assets and base path
- *(kubernetes)* Add local overlay for shared-web


## [0.3.0] - 2026-08-14

### 🚀 Features

- *(dev)* Remove unused service URLs from configmap
- Give the error pages medieval/D&D flavor text

### 🐛 Bug Fixes

- Remove logo size

### 🎨 Styling

- *(error)* Increase error status font size for visibility

## [0.2.0] - 2026-08-14

### 🚀 Features

- Brand the error pages with the platform's real design system

### 📚 Documentation

- Describe the error-pages route contract

### ⚙️ Miscellaneous Tasks

- Remove "secrets"
- *(kubernetes)* Remove destination-rules.yaml and update kustomization labels
- Divide secrets

## [0.1.5] - 2026-08-14

### 🐛 Bug Fixes

- Use Python 3.13, not 3.14 - uwsgi/msgspec fail to build wheels on 3.14
- Bump msgspec 0.18.6 -> 0.21.1 - no cp313 wheel at the old pin

### ⚙️ Miscellaneous Tasks

- Rename
- Update Python version

## [0.1.4] - 2026-08-14

### 🐛 Bug Fixes

- Bump base image to Python 3.14, matching assets-web

## [0.1.3] - 2026-08-14

### 🐛 Bug Fixes

- Bump base image to Python 3.11 - 3.9 crashes on boot

## [0.1.2] - 2026-08-14

### 🐛 Bug Fixes

- *(kubernetes)* Run 1 replica in dev, not 2
- *(kubernetes)* Don't pin replicas at all - let it default to 1
- *(kubernetes)* Align resource naming with platform convention

## [0.1.1] - 2026-08-14

### 🐛 Bug Fixes

- Remove crash-on-boot unconditional Sentry init

## [0.1.0] - 2026-08-14

### 🚀 Features

- *(admin-api)* Add maintenance-mode banner via admin-api-client.py
- Add shared branded error pages

### 🐛 Bug Fixes

- Secret version
- *(k8s)* Remove HPA and PDB from dev overlay
- *(ci)* Install Python 3.11 to match the py311 tox environment
- Unblock CI - templates outside sdist, no redis service
- Support Redis auth and fix always-true DEBUG parsing
- *(ci)* Scope Docker Build's concurrency group by ref
- *(ci)* Trigger CI/PR checks on workflow-file changes
- *(kubernetes)* Wire deployment to shared-web's own cache, make image pinnable

### 🚜 Refactor

- Rename unused LIBRARY_API_BASE_URL constant to SHELF_API_BASE_URL

### ⚙️ Miscellaneous Tasks

- Build arm64 image alongside amd64
- Fix memory spec
- *(kubernetes)* Move out of retired sweetrpg-support into sweetrpg-shared
- Add repo-setup-standard scaffolding
- Bootstrap real release pipeline
