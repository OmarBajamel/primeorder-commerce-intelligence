# Operations Runbook

## Purpose

Run, verify, diagnose and clean up the deterministic `public-demo` locally. Live-private connector use is optional, read-only and restricted to ignored local data paths; it is never required for tests, public builds or publication.

## Prerequisites

- Git
- Node.js compatible with Next.js 16 (Node 20.9+; Node 22 is the project development baseline)
- Corepack/pnpm `11.15.1`
- Python 3.11+ (Python 3.12 is the CI/development baseline)
- Optional: Docker Compose and a Chromium installation for Playwright

Commands below run from the repository root. The cross-platform Python wrapper checks `PYTHON_EXECUTABLE`, a bundled Codex runtime when present, the Windows launcher, `python3`, then `python`. It fails with a clear message if no usable interpreter exists.

## First run

### Native Windows

```powershell
pnpm bootstrap
pnpm data:generate
pnpm test:api
pnpm test:analytics
pnpm dev:web
```

Open the local URL printed by Next.js. In another terminal, start the API if local API exploration is needed:

```powershell
pnpm dev:api
```

### Native Bash

```bash
./scripts/bootstrap.sh
./scripts/build_public_demo.sh
./scripts/test.sh
./scripts/dev.sh
```

### Docker Compose

```bash
docker compose up --build
```

Docker maps the web to port `3000` and API to port `8000`. The API image builds from `services/api/Dockerfile`, installs pinned requirements, generates public-demo data and starts Uvicorn. The file-level gap found in the initial review is resolved; a Compose build/health/web smoke test is still required before claiming this path verified. Compose remains optional; the native path is the reproducibility reference if Docker itself is unavailable.

## Data generation

```powershell
pnpm data:generate
```

Expected contract:

- seed `20250301`;
- dates `2025-01-01` through `2025-12-31` (365 days);
- mode `public-demo`;
- independent synthetic provenance;
- six documented synthetic anomalies;
- generated CSV/JSON under `data/public-demo/` and dbt seeds under `analytics/seeds/`;
- file hashes and row counts in `data/public-demo/metadata.json` / `manifest.json`.

Do not treat those expected invariants as a pass until the command and deterministic regeneration tests succeed. Generated values demonstrate the product; they are not PrimeOrder metrics.

## Analytics warehouse

```powershell
pnpm analytics:build
```

This runs dbt with `analytics/` as project and profile directory. The implemented graph contains 11 seeds, 11 staging models, 5 intermediate models and 12 marts; test counts are recorded from the final manifest/run in the test report because semantic tests can change during review. dbt builds an embedded DuckDB target and validates schema/business tests. Generated `analytics/target/`, `analytics/logs/` and local database output are build artifacts, not public source inputs.

Important marts:

- `mart_executive_daily`
- `mart_funnel_daily`
- `mart_product_performance`
- `mart_category_performance`
- `mart_acquisition_performance`
- `mart_campaign_performance`
- `mart_search_performance`
- `mart_customer_mix`
- `mart_payment_performance`
- `mart_data_quality`
- `mart_source_reconciliation`
- `mart_prioritized_insights`

Warnings representing the six intentional demo defects are expected analytical output; dbt structural/invariant tests must still pass.

## API operations

Start:

```powershell
pnpm dev:api
```

The documented default binds Uvicorn to `127.0.0.1:8000`. Key routes are available both at root and under `/api/v1`:

| Route | Purpose |
|---|---|
| `/health` | Process liveness |
| `/readiness` | Public fixture availability and data mode |
| `/status` | Connector modes/statuses |
| `/summary` | Executive summary; optional `date_from`, `date_to` |
| `/funnel` | Funnel steps |
| `/products` | Product/category filter and bounded limit |
| `/acquisition` | Channel/source filters |
| `/seo` | Branded filter and bounded limit |
| `/customers` | New/returning filter |
| `/quality` | Quality results by optional severity |
| `/insights` | Prioritized insights by area/limit |
| `/docs` | FastAPI OpenAPI UI |

Smoke check without printing large payloads:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/readiness
```

Readiness returns HTTP 503 until all required generated JSON artifacts exist. Run data generation, then restart or retry.

## Web operations

Development:

```powershell
pnpm dev:web
```

Static production build:

```powershell
pnpm build
```

The Next.js configuration uses static export, trailing slashes, unoptimized static images and a repository-aware base path. In GitHub Actions, `GITHUB_REPOSITORY` determines the Pages base path unless `NEXT_PUBLIC_BASE_PATH` is explicitly set. The deployed browser must read only bundled/precomputed public data—never localhost, MCP or vendor APIs.

## Verification commands

Run narrow checks during development and the full gate before publication:

```powershell
pnpm lint
pnpm typecheck
pnpm test:unit
pnpm test:api
pnpm test:analytics
pnpm build
pnpm test:e2e
pnpm test:a11y
pnpm screenshots
pnpm release:check
pnpm test
```

`pnpm release:check` is intentionally fail-closed and requires tracked-file context plus a valid screenshot manifest. Running it before screenshots/final Git state can correctly fail. Never weaken the check; resolve the condition or document a genuine external limitation.

Evidence belongs in `artifacts/evidence/` and `docs/testing/`. A status/count is publishable only when it identifies the command, final commit/mode and result.

## Connector operations

The public API/status artifact selects all six connectors in `FIXTURE_MODE`; live status is `READY_NOT_AUTHENTICATED` in a fresh clone. Fixture and file imports are read-only. Live credentials are optional and must remain outside the repository.

PrimeOrder/Salla live reads use `SallaMCPConnector` with an environment-injected executor and an allowlist of aggregate read operations. The connector projects only approved aggregate fields and does not serialize raw MCP payloads. GitHub Pages cannot call MCP.

Do not test live connectors merely to make the status green. Do not use mutation tools, separate Salla API keys, customer/admin actions, cart/checkout/order activity, or wider OAuth scopes. Store any approved private export only under ignored `data/private/` or `.private/` paths.

## Evidence and publication sequence

1. Regenerate public data and inspect metadata/mode/provenance.
2. Run unit/API/connector/dbt/frontend/e2e/accessibility tests and production build.
3. Capture screenshots from the deterministic public app; inspect manifest/hash/privacy result.
4. Run secret/PII/private-path/bundle/release checks.
5. Resolve critical/high review findings; verify documentation claims.
6. Build/review release archives and hashes.
7. Publish only the reviewed commit/artifacts; verify CI/Pages.
8. Fresh-clone the public repository and repeat documented critical commands.

The complete manual gate is in [PUBLIC_RELEASE_CHECKLIST.md](../security/PUBLIC_RELEASE_CHECKLIST.md).

## Cleanup

Stop foreground servers with `Ctrl+C`, then:

```powershell
pnpm clean
```

The cleanup script removes only validated project build/report paths: web `.next`/`out`, dbt `target`/`logs`, Playwright report and test results. It does not delete source fixtures or private imports.

If Docker was used:

```powershell
docker compose down
```

Confirm ports are released on Windows:

```powershell
Get-NetTCPConnection -LocalPort 3000,8000 -State Listen -ErrorAction SilentlyContinue
```

No output means no matching listener. Do not kill an unrelated process solely by port number; identify its command/path first.

## Backup/recovery

Public-demo data and the warehouse are reproducible from Git and the fixed-seed generator; regenerate instead of backing up build outputs. Live-private exports are outside Git. If they must be retained, follow the controller-approved encrypted backup, access and expiry policy—this repository does not provide a private-data backup service.
