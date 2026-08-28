# Architecture Decision Records

Status terms: **Accepted** is the current design; **Superseded** points to its replacement; **Proposed** is not yet binding. Verification claims are deliberately excluded from ADRs.

## ADR-001 — Separate public static delivery from private local analysis

- Status: Accepted
- Date: 2026-08-28

### Context

The portfolio must be publicly reviewable while optional source integrations can contain confidential merchant aggregates and credentials. A public browser must never be able to reach private MCP tools or local data services.

### Decision

Deploy a static Next.js export backed only by deterministic public JSON. Keep optional live-private ingestion, DuckDB, and FastAPI on the analyst's machine. Maintain compatible response contracts so the same UI concepts can work in both modes without sharing storage or credentials.

### Consequences

- GitHub Pages has no runtime API dependency and exposes no connector credentials.
- Public filtering is limited to data shipped in the static artifact.
- Live-private exploration requires local setup.
- Release tooling must reject private mode, private paths, and private endpoint references.

## ADR-002 — Use deterministic synthetic data for all public evidence

- Status: Accepted
- Date: 2026-08-28

### Context

Public screenshots and recruiter evidence need realistic commerce behavior, but neither exact private values nor transformed approximations are safe.

### Decision

Generate the public dataset from a fixed seed, invented product/channel assumptions, and an explicit generator version. Do not scale, perturb, or statistically fit it to PrimeOrder private data. Include documented synthetic defects to exercise audit logic.

### Consequences

- Public numbers demonstrate product behavior, not actual business performance.
- No commercial uplift claim may be derived from the demo.
- Reproducibility tests can detect generator drift.

## ADR-003 — Use DuckDB and dbt for the analytical core

- Status: Accepted
- Date: 2026-08-28

### Context

The project requires SQL modeling, lineage, tests, and a fresh-clone experience without operating a shared database service.

### Decision

Use DuckDB as the embedded warehouse and dbt for staging, intermediate, mart, test, and documentation workflows.

### Consequences

- The warehouse is portable and inexpensive for a reviewer to run.
- Model grains and business tests are version-controlled.
- It is not a multi-user production warehouse and does not model production orchestration, access control, or high concurrency.

## ADR-004 — Reconcile sources; do not blend away disagreement

- Status: Accepted
- Date: 2026-08-28

### Context

Merchant commerce reports and GA4 differ in collection, attribution, consent, timezone, refunds, blockers, and transaction semantics. Combining them into one undocumented number would hide measurement risk.

### Decision

Use the authoritative commerce source for financial/order KPIs and GA4 for behavioral and acquisition metrics. Publish source-specific values and explicit absolute/percentage variance in reconciliation marts. Treat missing denominators and zero-source cases as unavailable, not zero variance.

### Consequences

- Stakeholders can see disagreement and investigate it.
- Cross-source trend comparison requires aligned date windows, timezone, currency, transaction rules, and freshness.
- The dashboard must label each measure's source.

## ADR-005 — Provide fixture, import, and optional live-read paths behind one connector contract

- Status: Accepted
- Date: 2026-08-28

### Context

Most reviewers lack vendor credentials, while authenticated source availability differs by environment.

### Decision

Every connector exposes a deterministic fixture implementation and a validated CSV/JSON import path. A live implementation is enabled only when safe authentication and a read-only source are available. Connector status and freshness accompany the payload.

### Consequences

- A fresh clone remains evaluable without credentials.
- `FIXTURE_MODE` proves the local adapter path, not live integration.
- Authentication, quota, thresholding, sampling, and source limitations remain visible.

## ADR-006 — Make data quality first-class output

- Status: Accepted
- Date: 2026-08-28

### Context

Decision support is unsafe when unknown products, duplicate transactions, missing event parameters, stale sources, or cross-source variance are silently normalized.

### Decision

Persist quality rule outcomes and reconciliation results as marts. Expose severity, affected source, row count, affected KPI, recommended action, owner, and evidence rather than hiding failed records.

### Consequences

- Quality defects can drive the insight backlog.
- Users must distinguish detected defects from remediated defects.
- Quality rules need stable identifiers and versioned thresholds.

## ADR-007 — Preserve privacy-safe analytical grain

- Status: Accepted
- Date: 2026-08-28

### Context

Customer-level identifiers are unnecessary for most portfolio questions and increase re-identification risk, especially when combined with city, coupon, timestamp, or product details.

### Decision

Use daily and privacy-safe aggregate grains for public outputs. In live-private mode, minimize fields, pseudonymize identifiers only where repeat behavior genuinely requires them, suppress small groups when needed, and do not persist direct identifiers or order references.

### Consequences

- Some cohorts and exact repeat-purchase calculations may be unavailable.
- Operational order investigation is outside scope.
- Geographic, coupon, and customer breakdowns require disclosure-risk review.

## ADR-008 — Fail closed at the public release boundary

- Status: Accepted
- Date: 2026-08-28

### Context

An ignored source file can still leak through a copied artifact, screenshot, generated bundle, Git history, or release archive.

### Decision

Require the release gate to prove public-demo mode, absence of tracked private paths and likely secrets/PII, safe screenshot metadata/content, no private endpoints, and a reviewed artifact manifest. A failed or inconclusive high-risk check blocks publication.

### Consequences

- Release preparation can stop on false positives that need human review.
- `.gitignore` is necessary but not sufficient.
- Evidence must identify the commit and artifact hashes checked.

## ADR-009 — Specify measurement before changing tracking

- Status: Accepted
- Date: 2026-08-28

### Context

The project can audit public behavior and imported reports but is not authorized to change live GTM, GA4, consent, storefront, or checkout settings.

### Decision

Document the target GA4 event contract, GTM implementation approach, consent considerations, and validation queries. Keep audit observations separate from recommendations. Any future live deployment requires merchant approval, consent/legal review, preview validation, and rollback planning.

### Consequences

- The repository demonstrates measurement engineering without claiming live instrumentation was deployed.
- Passive observations may be incomplete because checkout and consent states cannot be exercised invasively.

## ADR-010 — Treat cost-dependent metrics as conditional

- Status: Accepted
- Date: 2026-08-28

### Context

Digital-product cost attribution and ad spend may be absent or unreliable. Showing gross margin, CPA, or ROAS from partial inputs would create false precision.

### Decision

Publish gross margin/margin rate only with reliable allocated cost, CPA only with reliable spend and conversion scope, and ROAS only with comparable spend and attributed revenue. Otherwise return unavailable with a reason.

### Consequences

- Some desired KPIs intentionally remain blank in live-private mode.
- Synthetic fixtures may demonstrate the calculations only when their cost and spend fields are explicitly marked reliable.

