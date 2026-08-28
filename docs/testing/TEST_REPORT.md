# Test Report

## Release-candidate scope

- Review date: 2026-08-28
- Data mode: `public-demo`
- Dataset: deterministic synthetic data, seed `20250301`, 2025-01-01 through 2025-12-31
- Candidate identifier: working tree under review; final release SHA not recorded here

This report separates executed evidence from configuration or planned verification. Counts from different runners are not added into one headline total because dbt nodes, unit tests and browser scenarios represent different work units.

## Results

| Layer | Command/scope | Result | What it establishes |
|---|---|---:|---|
| Python generator/connectors/API | `pnpm test:api` | **PASS — 26 tests** | Determinism, manifests, connector schema/status/retry/privacy behavior, API contracts/filters and safe logging |
| Analytics | `pnpm test:analytics` | **PASS — 117/117 nodes** | 11 seeds loaded, 28 models built and 78 data tests passed |
| Frontend unit | `pnpm test:unit` | **PASS — 10 tests** | Data normalization/filtering, presentation helpers, provider and localization behavior |
| Browser E2E | dashboard Playwright suite | **PASS — 11 checks** | Nine routes, synthetic disclosure, no private API calls/console errors, filters/export/RTL and mobile overflow |
| Accessibility | axe/keyboard Playwright suite | **PASS — 6 checks** | Five route audits with no serious/critical axe finding plus primary keyboard/skip-link workflow |
| Static hosting | static-export Playwright configuration | **PASS — 1 scenario** | All nine routes load by direct navigation under the repository base path without failed responses |
| Public release scan | `pnpm release:check` | **PASS** | Required files, tracked/private paths, secret/PII patterns, history/archive scope and screenshot-manifest presence |
| Compose syntax | `docker compose config --quiet` | **PASS** | Compose file resolves and validates structurally |
| Compose runtime | local Docker Desktop engine | **NOT RUN** | Linux engine socket unavailable; images and running services were not verified locally |

## dbt detail

The recorded `run_results.json` contains 117 successful results:

- 11 seed loads;
- 28 models;
- 78 data tests.

Coverage includes declared grains and keys, revenue identities, product/category reconciliation, proportional refunds, GA4 product totals, stable customer lifecycle classification, event-name and parameter coverage, exact documented-anomaly counts, search metrics and Commerce-versus-GA4 tolerance.

Known synthetic warnings remain intentional: duplicate tracking transaction, missing event parameters, stale search data, an unmapped product, a five-day reconciliation variance and reduced consent-state coverage. Tests prove the expected warning counts; they are not live-store findings.

## Browser coverage

The 11 E2E checks comprise:

- nine route smoke/privacy/error checks;
- one filter, comparison, CSV export and language-direction workflow;
- one mobile overflow/disclosure workflow.

The six accessibility checks comprise five WCAG A/AA axe scans and one keyboard/skip-link scenario. Automated accessibility checks reduce risk but do not replace manual screen-reader, zoom, contrast-in-context and usability testing.

The static-export scenario iterates all nine routes under the configured repository base path. It is counted as one scenario because the route loop belongs to one Playwright test.

## Screenshot evidence

Eight PNGs are recorded in `artifacts/evidence/screenshot-manifest.json`:

- five English desktop evidence views;
- one Arabic/RTL desktop view;
- two mobile views.

Every manifest entry contains a SHA-256 hash, `public-demo` mode, capture metadata, alt text and privacy review `PASS`. Screenshot review is visual evidence, not an automated assertion count.

## Lighthouse

| Profile | Performance | Accessibility | Best Practices | SEO |
|---|---:|---:|---:|---:|
| Desktop | 85 | 100 | 100 | 100 |
| Mobile | 46 | 100 | 100 | 100 |

The desktop and mobile audits each reported approximately 428 KiB total transfer. The dashboard JSON contributed approximately 125 KiB. The mobile run also reported 4.46 seconds Total Blocking Time, 13 seconds main-thread work, 3.2 seconds LCP and CLS 0.353. Therefore the mobile performance score is a material open limitation. Likely work includes route-level payload splitting, reducing client JavaScript, deferring non-critical charts and stabilizing layout; the same profile must be rerun after changes.

Lighthouse scores are lab measurements from one local run and may vary by machine and throttling. They do not demonstrate field performance.

## Container limitation and CI design

Compose configuration validation passed locally. `docker info` could not reach the Docker Desktop Linux engine, so this report does not mark container build, startup, API readiness or web smoke as locally passed.

The CI workflow is designed to run `docker compose build`, start the services, poll API health and the web endpoint, print logs on failure and tear the stack down. That design is inspectable, but its runtime result must remain unverified until a successful CI job is recorded.

## Release interpretation

The automated application, analytics, accessibility, static-export and public-data checks are green for the recorded working tree. Public release should still require:

1. a final clean-clone rerun against the exact candidate SHA;
2. successful CI, including the container smoke job;
3. rechecking manifest and screenshot hashes after any artifact regeneration;
4. treating mobile performance as an explicit limitation until improved and remeasured;
5. inserting public URLs only after those URLs are independently opened and verified.

