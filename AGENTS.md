# PrimeOrder Commerce Intelligence - Repository Guide

## Commands

- Bootstrap: `pnpm bootstrap` or `./scripts/bootstrap.ps1`
- Generate deterministic demo data: `pnpm data:generate`
- Run dashboard: `pnpm dev:web`
- Run API: `pnpm dev:api`
- Full verification: `pnpm test`
- Capture evidence: `pnpm screenshots`
- Public release gate: `pnpm release:check`
- Cleanup: `pnpm clean`

## Privacy and data rules

- `public-demo` is the default and the only mode allowed in builds, tests, screenshots, Pages, releases, CV assets, and social assets.
- Never commit or quote live merchant metrics, customer identifiers, order references, credentials, raw MCP responses, or authorization metadata.
- All live extracts belong under ignored `data/private/` or `.private/`; aggregate them and pseudonymize identifiers before local analysis.
- PrimeOrder/Salla MCP operations are read-only. Never call mutation tools.

## Screenshot and release rules

- Screenshots must show the synthetic-data disclosure and contain no private data.
- Generate screenshot hashes and a privacy-review result in the manifest.
- A release must pass frontend, API, analytics, e2e, accessibility, secret, PII, tracked-private-path, and public-mode checks.
- Do not weaken tests to make a release pass. Document genuine external connector limitations.

## Definition of done

The documented public demo builds from a fresh clone; EN and AR/RTL routes are verified; analytics, API, browser, accessibility, and privacy checks pass; screenshots and career artifacts are based on the real public-demo app; GitHub Actions and Pages are green; release `v1.0.0` exists; and all local servers are stopped.
