# Technical Case Study: PrimeOrder Commerce Intelligence

## Executive technical summary

PrimeOrder Commerce Intelligence is a privacy-separated commerce measurement system for a Saudi digital-products store. It combines deterministic demo generation, six typed read-only connector paths, DuckDB/dbt analytics, a filtered FastAPI API, and an EN/AR static Next.js dashboard that can be deployed to GitHub Pages without private credentials or server-side access.

The project demonstrates implementation and measurement-quality reasoning; it does not claim a measured sales, conversion, SEO, margin or cost-saving improvement. Every public number is synthetic and independently generated.

## Problem

Commerce, behavioral, acquisition, search, merchant and UX data answer different questions and often disagree. The technical risks were not simply “build a dashboard”:

- keep live merchant/customer information out of a public portfolio;
- preserve Salla as the commerce authority while using GA4 for behavior/attribution;
- make missing/duplicated/stale/misaligned data visible;
- support reviewers without vendor credentials;
- publish a static site without private API or MCP access;
- define GA4/GTM/consent recommendations without changing the live store;
- keep EN/AR and RTL, accessibility, testing and release evidence in the engineering scope.

## Constraints

- PrimeOrder/Salla access is read-only through the connected MCP; no separate API-key integration or mutation.
- Live-private files stay ignored and local; raw MCP responses, customer/order identifiers, credentials and exact merchant metrics are not public inputs.
- Public-demo data must be deterministic and not derived from real scale/distribution.
- GitHub Pages is static; it cannot call MCP, vendor reporting APIs or local FastAPI.
- A passive storefront audit cannot log in, add to cart, begin checkout, submit an order or alter tracking/consent settings.
- Cost/ROAS/margin metrics are available only where their inputs are deliberately reliable and comparable.

## Architecture decisions

### Separate delivery paths

The public path generates synthetic CSV/JSON, builds/tests dbt models, exports precomputed API-shaped JSON and statically exports Next.js. The live-private path accepts authorized read-only aggregate reports into ignored local storage and can expose filtered marts through FastAPI on loopback. There is intentionally no live-to-public data path.

### Embedded analytical stack

DuckDB makes the warehouse portable; dbt provides staged contracts, model grains, tests and lineage without requiring a shared database server. The current graph contains:

- 9 generated seeds;
- 9 staging models;
- 4 intermediate models;
- 12 marts.

### Status as data

Connectors return a typed mode/status rather than letting the UI infer connectivity. Public evidence shows `FIXTURE_MODE`; the cloned application's live path shows `READY_NOT_AUTHENTICATED` until a safe local executor/credential path exists. An account-discovery or active-tool observation is kept separate from report extraction capability.

### Reconcile rather than blend

Commerce and GA4 purchase/revenue measures remain side by side with variance and tolerance fields. A source disagreement becomes quality evidence rather than a hidden average. Date, timezone, currency, order status, revenue components, duplicates, refunds and freshness must align before interpreting variance.

Full rationale is in [ADRS.md](../architecture/ADRS.md).

## Implemented system

### Deterministic dataset

The generator uses seed `20250301` for 365 dates from `2025-01-01` through `2025-12-31`. Current metadata records 12 synthetic products, 9,075 synthetic orders, 9,075 order-item rows and independent provenance (`derived_from_real_merchant_data: false`).

Six deliberate defects exercise observability:

1. duplicate GA4 tracking transaction ID;
2. missing purchase currency/item parameter coverage;
3. Search Console fixture stale by eleven days at dataset end;
4. an unmapped product key;
5. a five-day GA4 under-reporting window;
6. reduced synthetic consent-state coverage.

These are expected warnings, not live PrimeOrder findings. Structural/business tests must still pass.

### Connector layer

Six adapters implement a shared read-only contract:

- PrimeOrder/Salla MCP;
- GA4;
- Search Console;
- Merchant Center;
- Microsoft Clarity;
- optional Google Ads.

All support public fixtures; adapters expose CSV/JSON file fallback according to their status artifact. They validate required fields, report freshness and use typed statuses. The Salla bridge accepts an environment-owned executor, restricts calls to an allowlist of aggregate reads, projects approved aggregate fields and does not serialize raw MCP payloads.

The current public status artifact marks all six `FIXTURE_MODE` and all fresh-clone live paths `READY_NOT_AUTHENTICATED`. This does not contradict active Codex observations that selected external discovery/aggregate tools were reachable: those sessions are not application credentials and are not shipped.

### Analytics layer

The dbt graph normalizes products, commerce aggregates, orders/items, GA4 aggregates/events, Search Console, Merchant diagnostics and Clarity. Intermediate models aggregate commerce, enrich order items, summarize event parameter quality and align Salla-like/GA4 daily values. Twelve marts cover executive, funnel, product/category, acquisition/campaign, search, customer, payment, data quality, reconciliation and prioritized insight use cases.

The quality mart detects six documented anomaly classes: duplicate transactions, unknown products, incomplete parameters, stale search data, daily source variance and consent-state coverage below 95%. The static quality API exposes the corresponding synthetic warnings and remediation descriptions.

### API and contracts

FastAPI exposes health/readiness, connector status, summary, funnel, products, acquisition, SEO, customers, quality and insights at root and `/api/v1`. Pydantic models reject unexpected response fields. Query bounds and typed filters constrain date, category, channel/source, branded state, customer type, severity, area and limits. Errors include a request ID without returning internal stack traces to clients; logs capture route/status/duration.

The API is local-only and reads generated public-demo JSON/CSV in the current implementation. Public GitHub Pages consumes the same precomputed shapes without a server.

### Measurement and consent design

The repository specifies eleven recommended GA4 ecommerce events and parameter/value rules; a GTM implementation guide; consent-aware EEA/German engineering scenarios; and an evidence scale that distinguishes `PASS`, `FAIL`, `NOT_RUN`, `NOT_OBSERVABLE` and `NOT_APPLICABLE`.

A passive public-storefront inspection recorded two RTL page classes. Two GTM script references were observed per inspected page, while no inline data layer, inline consent default/update, or visible consent text was observed in the captured DOM. This point-in-time result is not proof that tags or consent behavior are absent: tags may load conditionally, after interaction, server-side or outside inspected DOM evidence. No cart, checkout, order, login, form submission or configuration change occurred.

## Verification evidence available at this stage

The analytics/API track reported a passing dbt build and Python connector/API suite after the semantic fixes; exact final counts belong in the test report generated from the release-candidate run because review may add tests. Deterministic metadata/file SHA-256 manifests were generated, and the passive storefront evidence records privacy review `PASS`.

These are track-reported implementation results at the time this case study was written. The final release/handoff must re-run, count and bind every result to the final commit. This document does not infer frontend, e2e, accessibility, screenshot, security-scan, deployment, release or fresh-clone results before their evidence exists.

## Requirement-to-evidence traceability

| Requirement | Implementation source | Verification/evidence source | Current interpretation |
|---|---|---|---|
| Independent 365-day synthetic public mode | `scripts/generate_demo_data.py` | `data/public-demo/metadata.json`, manifest and generator tests | Implemented; final deterministic rerun pending |
| Public/private separation | static Next.js config, local API, ignored private paths, release checker | architecture/privacy docs, bundle/private-path release evidence | Implemented controls; final artifact/history review pending |
| Six typed read-only connector paths | `connectors/` registry/base/source adapters | `artifacts/evidence/connector-status.json`, connector tests | Fixture/status paths, typed models, metadata envelopes and bounded transient retry implemented; live fresh-clone unauthenticated |
| Salla MCP read-only boundary | allowlisted operations/fields and injected executor | connector tests/code review | Implemented bridge design; no public live payload |
| Tested analytical warehouse | `analytics/models`, `schema.yml`, singular tests | dbt manifest/run report | Track reports pass; exact final counts pending |
| Consistent KPI/source layer | mart SQL, Pydantic/static contracts | KPI catalog/YAML and semantic reconciliation tests | Core public semantics aligned; final UI/tooltips review pending |
| Local filtered API | FastAPI routes, repository and Pydantic contracts | API tests, health/readiness smoke evidence | Public-demo API implemented; live-private repository is future work |
| Static recruiter dashboard | Next.js static export and precomputed JSON | frontend/e2e/accessibility/build evidence | Implemented in shared tree; final browser/release proof belongs to frontend/release tracks |
| Eleven-event GA4 audit | event fixture/staging/intermediate/quality SQL and event coverage test | measurement spec/audit and dbt evidence | Public fixture represented; live event coverage not observed |
| EEA/German consent-aware representation | consent notes, GTM guide, coverage fields | passive audit evidence and future Tag Assistant scenarios | Engineering design complete; live behavior `NOT_OBSERVABLE`; no compliance claim |
| Release privacy/security gate | `scripts/release_check.py`, screenshot manifest checks, ignored paths | release-check JSON and manual checklist | Mechanism implemented; final release-candidate pass pending |

This table links code/doc/evidence without turning an unexecuted check into a pass.

## Trade-offs

| Decision | Benefit | Cost/limitation |
|---|---|---|
| Static public app | No public credentials/API/private data path; low hosting cost | No runtime live refresh or server-side filtering |
| Synthetic public dataset | Safe, repeatable portfolio evidence | Cannot demonstrate actual PrimeOrder outcomes |
| DuckDB/dbt | Portable SQL/testing/lineage | Not a multi-user production warehouse |
| Aggregates/minimization | Lower disclosure risk | Some identity/cohort/sequence questions become unavailable |
| Fixture path for every connector | Fresh clone works without credentials | Fixture success does not prove authentication |
| Explicit source reconciliation | Measurement disagreement stays visible | Requires careful scope alignment and stakeholder education |
| Passive live audit | Avoids transaction/customer/configuration impact | Cannot validate checkout, purchase, refund or all consent interactions end to end |

## Implementation versus recommendations

| Implemented/documented now | Recommended future work; not claimed as deployed |
|---|---|
| Fixed-seed synthetic generator and public API fixtures | Scheduled private aggregate refresh with approved credential/governance design |
| Six typed read-only connector adapters and explicit status artifact | Authenticate each live reporting source with least scopes and record capability-specific evidence |
| Allowlisted ephemeral Salla MCP aggregate bridge | Run approved local exports; never expose raw/private payloads publicly |
| 25-model dbt graph, marts and quality/reconciliation logic | Production orchestration, alerting, warehouse access control and retention enforcement |
| FastAPI public-demo repository and typed endpoints | Optional live-private repository implementation with suppression and audit controls |
| Eleven-event target specification and audit rules | Deploy/fix GTM/data layer only after merchant, privacy/legal and peer approval |
| EEA/German consent engineering checklist | Controller decision on CMP, lawful basis, Consent Mode and vendor settings |
| Passive storefront evidence | Approved staging/test validation for checkout, purchase, refund and consent scenarios |
| Synthetic prioritized insights | Controlled experiments with pre-registered success metrics; measure real impact before claims |

## Known technical limitations and open review items

- Live connector report extraction is not authenticated in the cloned application; public fixture mode is intentional.
- The public aggregate fixture now covers all eleven target events and ten parameter/consent coverage fields. This is fixture validation, not evidence that the live storefront implements them.
- A passive DOM/network observation cannot determine legal compliance or complete runtime tag behavior.
- Revenue semantics are now aligned in generator, marts, API and catalog: gross is pre-discount/pre-refund, net subtracts discount and refund, AOV uses net revenue/completed purchases, and product/category refunds are proportionally allocated before margin. Final release verification must rerun the semantic tests on the final commit.
- Final public repository, Pages, release, workflow and commit URLs are intentionally absent until verified; no placeholder is presented as a result.

## Next experiments

After measurement quality and consent governance are approved, candidate work is:

1. complete non-production event coverage for discovery/cart/checkout/refund and measure parameter completeness;
2. reconcile an aligned private Salla/GA4 window and classify explained variance;
3. segment synthetic and then authorized private funnel quality by device/payment/source without small-group disclosure;
4. prioritize one real friction hypothesis using Clarity/commerce evidence, define guardrails and run a controlled experiment;
5. improve Search Console freshness/brand classifier and validate SEO changes using pre/post or controlled evidence;
6. add monitored private refreshes only after access, retention, incident and vendor-limit controls are operational.

None of these imply future uplift. Any business result must be measured after implementation against an explicit baseline and experiment design.

## Recruiter-oriented technical relevance

The case study demonstrates e-commerce KPI semantics, measurement strategy, data-quality/reconciliation reasoning, SQL/dbt/Python/API engineering, privacy/security boundaries, static deployment architecture and multilingual product delivery. The important signal is not a fabricated outcome; it is the ability to build a decision system that explains what is known, what source it came from, and what remains unsafe or unverified.
