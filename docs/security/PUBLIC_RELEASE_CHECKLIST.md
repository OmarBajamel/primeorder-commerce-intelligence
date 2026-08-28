# Public Release Checklist

Use this checklist for the exact release candidate commit and artifacts. All boxes intentionally start unchecked. A generated/passing command result may be linked, but no item is complete based on intention or a prior commit.

## Release identity

- [ ] Release candidate full commit SHA recorded: `________________`
- [ ] Intended tag/version recorded: `________________`
- [ ] Reviewer and UTC review time recorded: `________________`
- [ ] Working tree and tracked-file inventory reviewed; unrelated/private files absent.
- [ ] Claims, URLs, test counts and connector statuses match evidence for this commit.

## Mode and data boundary

- [ ] Build/test/screenshot environment is exactly `public-demo`.
- [ ] UI visibly says “Synthetic portfolio demo data — no real customer or revenue information” wherever public numbers appear.
- [ ] Synthetic generator provenance is independent; no live distribution/scale/metric was used.
- [ ] `data/private/`, `.private/`, local databases, exports, raw MCP/API responses and credential files are untracked and absent from artifacts.
- [ ] Git history scan finds no secret/private-data introduction.
- [ ] Public bundle contains no live value, private identifier, vendor reporting endpoint, `localhost`, `127.0.0.1`, private API URL or credential.

## Secrets and privacy

- [ ] Secret scan passed for tracked files, Git history, build output and every release archive.
- [ ] Likely PII/auth-metadata/private-metric scan passed or each false positive is safely reviewed.
- [ ] Environment/config examples contain names/placeholders only.
- [ ] Logs/evidence contain no headers, tokens, cookies, auth codes/URLs, payloads, private identifiers or exact private totals.
- [ ] Screenshots/media passed visual and practical OCR/metadata review.
- [ ] Each screenshot manifest row contains path, route, viewport, language, mode, commit, capture time, SHA-256, privacy result, intended use and alt text.
- [ ] CV, social, architecture and release derivatives were re-reviewed after composition.

## Code, analytics and connectors

- [ ] Frontend lint, type check, unit/component tests and production static build passed.
- [ ] API tests, health/readiness, validation/error and safe-logging checks passed.
- [ ] dbt build/tests passed, including grain, relationship, invariant and reconciliation rules.
- [ ] Deterministic data test passed from clean inputs.
- [ ] Browser/e2e, EN/AR routes, RTL, mobile and direct/static navigation passed.
- [ ] Accessibility checks passed or honest non-blocking evidence/ownership is recorded.
- [ ] Public browser network inspection shows static public assets only.
- [ ] Connector fixture/import/live statuses match the exact tested capability; no discovery-only or fixture path is overstated.
- [ ] PrimeOrder/Salla path is read-only MCP/export bridge; no mutation code or separate API-key integration exists.

## Supply chain and assets

- [ ] JavaScript lockfile and pinned Python dependencies are committed and install cleanly.
- [ ] Dependency/security scans have no unresolved release-blocking critical/high shipped vulnerability.
- [ ] GitHub Actions use minimal permissions and trusted/pinned actions; public build requires no live secrets.
- [ ] Every image/font/icon/data fixture/code asset is generated, owned or used under a compatible documented license.
- [ ] Source maps and generated static files were inspected for internal paths/config/data.
- [ ] Release ZIP/PDF/media can be opened and their internal file lists match the reviewed manifest.

## Documentation and evidence

- [ ] README, architecture, data dictionary, KPI catalog, connector status, measurement, privacy, security, operations and case study match implementation.
- [ ] Implemented capability is clearly separated from recommendation/future work.
- [ ] No unmeasured revenue, conversion, SEO, cost-saving or commercial-uplift claim appears.
- [ ] Command/test counts, hashes, deployment state, final URLs and limitations are supported by evidence.
- [ ] Critical/high architecture, analytics, security/privacy, UX and documentation review findings are resolved.
- [ ] License, security policy, contributing guide and code of conduct are present.

## Publication and post-publication proof

- [ ] Public repository target/visibility/description/topics are correct.
- [ ] Required CI workflows passed on the final commit.
- [ ] GitHub Pages deployed from the reviewed static artifact and was opened/verified on desktop/mobile and EN/AR routes.
- [ ] Public page requests no localhost/private/vendor reporting endpoint and shows the synthetic label.
- [ ] Exact repository/demo/release/commit/workflow URLs replaced placeholders in public career/social/release docs.
- [ ] Tag/release points to the reviewed commit; release assets match recorded SHA-256 hashes.
- [ ] Fresh clone followed documented bootstrap and passed critical tests/build without local hidden dependencies.
- [ ] Final deployed/release artifacts received one last privacy/secret/content inspection.

## Sign-off

| Review | Reviewer | Result | Evidence path/URL | Time |
|---|---|---|---|---|
| Architecture |  |  |  |  |
| Analytics |  |  |  |  |
| Security/privacy |  |  |  |  |
| Frontend/UX/accessibility |  |  |  |  |
| Documentation/career claims |  |  |  |  |
| Release owner |  |  |  |  |

Any unchecked release-blocking item means the release is not approved. Document external limitations honestly; do not convert them into passes.

