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
