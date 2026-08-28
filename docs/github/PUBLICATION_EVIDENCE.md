# Publication evidence

PrimeOrder Commerce Intelligence was published as a public, synthetic-data-only portfolio project on 28 August 2026.

## Public endpoints

- Repository: https://github.com/OmarBajamel/primeorder-commerce-intelligence
- GitHub Pages: https://omarbajamel.github.io/primeorder-commerce-intelligence/
- Release: https://github.com/OmarBajamel/primeorder-commerce-intelligence/releases/tag/v1.0.0
- Publication build commit: https://github.com/OmarBajamel/primeorder-commerce-intelligence/commit/98134e2c2ac912961a262a18296de200c0c63ffe
- Successful CI: https://github.com/OmarBajamel/primeorder-commerce-intelligence/actions/runs/33208946030
- Successful Pages deployment: https://github.com/OmarBajamel/primeorder-commerce-intelligence/actions/runs/33209108631

## Verified publication state

- GitHub Pages is configured with `build_type=workflow` and HTTPS enforcement.
- The deployed root returned HTTP 200 with `text/html; charset=utf-8`.
- The Pages workflow rebuilt the static export with the repository base path, ran the static-hosting test, ran the fail-closed release check, uploaded the Pages artifact, and deployed successfully.
- The six-job CI workflow passed frontend quality, Python/API tests, dbt analytics, browser/accessibility/privacy checks, dependency security, and Docker Compose build/smoke validation.
- The live deployment was visually verified in `artifacts/evidence/github-pages-verification.png`.

## Fresh-clone reproduction

A new public clone of commit `98134e2c2ac912961a262a18296de200c0c63ffe` was created outside the working tree's dependency directories and validated from committed lockfiles.

| Check | Result |
| --- | --- |
| `pnpm bootstrap` | PASS |
| Deterministic data generation | PASS: seed `20250301`, 365 days, exact committed row counts |
| ESLint | PASS |
| TypeScript | PASS |
| Frontend unit tests | PASS: 10/10 |
| Python/API/connector/generator tests | PASS: 26/26 |
| dbt build | PASS: 117/117, WARN=0, ERROR=0 |
| Next.js production build | PASS: nine application routes exported |
| Release/privacy check | PASS: no missing inventory, secret/PII, history, archive, or private-path findings |

Browser/accessibility coverage was also independently validated by the successful GitHub Linux CI run: 17/17 Playwright checks, including axe scans, keyboard reachability, workflow behavior, privacy/network assertions, and mobile overflow.

## Scope and limitations

- All published business data is deterministic and synthetic; it is not PrimeOrder production data.
- Connector implementations are typed, read-only fixture paths. No production credentials are included.
- Commerce and GA4 retain separate metric ownership; source differences are surfaced rather than silently blended.
- No measured commercial uplift is claimed.
- Desktop Lighthouse scored 85/100/100/100. Mobile scored 46/100/100/100 and remains a documented optimization opportunity.
- Distinct users are non-additive across arbitrary periods; the public demo uses period-scoped aggregations and documents this limitation.
- Docker was unavailable on the authoring host, but GitHub's Linux Docker Compose build and smoke job passed.
