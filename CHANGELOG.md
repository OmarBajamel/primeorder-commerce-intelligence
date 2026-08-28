# Changelog

All notable changes to PrimeOrder Commerce Intelligence are documented here.

## [1.0.0] - 2026-08-28

### Added

- Nine-page English/Arabic commerce intelligence dashboard with verified RTL behavior and GitHub Pages static export.
- Deterministic 365-day Saudi digital-commerce fixture with six documented measurement anomalies.
- Typed Salla MCP, GA4, Search Console, Merchant, Clarity, and Google Ads connector paths with fixture and file modes.
- Read-only FastAPI analytics surface and shared contracts.
- DuckDB/dbt warehouse with 28 models and 78 data tests.
- GA4/GTM ecommerce event specification, consent notes, quality checks, and source reconciliation.
- Public/private trust boundaries, release scanning, screenshot provenance, CI, Pages deployment, Docker Compose, and native scripts.
- English/German career materials and a review-ready LinkedIn media package.

### Verified

- 10 frontend unit tests, 26 Python tests, 117 successful dbt nodes, 17 browser/accessibility checks, and direct-navigation static testing.
- Lighthouse desktop 85/100/100/100 and reviewed public-demo screenshots.
- Secret, PII, Git-history, private-path, bundle, screenshot, and release-archive gates.

### Known limitations

- Live connector authentication is intentionally external to the public repository.
- Local Docker engine was unavailable during final local verification; trusted CI contains the container build and smoke gate.
- Mobile performance is constrained by the complete filterable 365-day public dataset and remains explicitly documented.
