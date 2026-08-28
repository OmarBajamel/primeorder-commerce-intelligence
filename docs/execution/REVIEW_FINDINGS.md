# Independent Review Findings

## Review policy

This register records architecture, analytics, security/privacy, frontend/UX and documentation/career review. It is an evidence ledger, not a substitute for fixing defects. Critical/high findings block public release unless the condition is removed; an external limitation may remain only when it does not create an unsafe or misleading artifact and is explicitly documented.

### Severity

| Severity | Meaning | Release rule |
|---|---|---|
| Critical | Secret/private-data exposure, mutation risk, public/live boundary break, exploitable code path or materially false release evidence | Block immediately |
| High | Material KPI/privacy/security/accessibility/functional error likely to mislead or harm | Block until resolved and verified |
| Medium | Significant limitation or inconsistency with bounded impact/workaround | Fix when feasible; owner/rationale required if deferred |
| Low | Minor maintainability/copy/polish issue | May defer with owner |

### Status

`OPEN`, `IN_PROGRESS`, `RESOLVED_AWAITING_VERIFICATION`, `VERIFIED`, or `ACCEPTED_LIMITATION`. Only identified rerun/review evidence can set `VERIFIED`.

## Current findings

| ID | Track | Severity | Status | Finding and evidence | Required resolution | Owner |
|---|---|---|---|---|---|---|
| `AN-001` | Analytics | High | `RESOLVED_AWAITING_VERIFICATION` | Initial generator used ambiguous post-discount gross semantics. The generator/marts/API now define gross pre-discount/pre-refund and net as gross minus discount and refund. | Re-run deterministic, semantic reconciliation, API and dbt tests on the final commit; inspect UI/tooltips/catalog alignment. | Analytics |
| `AN-002` | Analytics | High | `RESOLVED_AWAITING_VERIFICATION` | Initial AOV used gross/purchases. The generator, API and executive mart now use net revenue/completed purchases. | Re-run formula regression/API/dbt tests on the final commit and inspect presentation. | Analytics |
| `AN-003` | Analytics | Medium | `RESOLVED_AWAITING_VERIFICATION` | Initial product/category margin omitted refunds. `int_orders_enriched` now allocates refund proportionally to after-discount item value; product/category margin uses net revenue minus cost. | Re-run order/item/category reconciliation and margin tests on the final commit. | Analytics |
| `ME-001` | Measurement | Medium | `RESOLVED_AWAITING_VERIFICATION` | Initial fixture covered five events. It now contains all eleven target event names and coverage fields for transaction ID, currency, value, items, item ID/name/category, price, quantity, promotion and consent. | Re-run event coverage/accepted-value/parameter tests on the final commit; retain clear fixture-versus-live wording. | Measurement/Analytics |
| `ME-002` | Measurement/privacy | Medium | `ACCEPTED_LIMITATION` | Passive audit observed GTM references but no inline data layer/consent default/update or visible consent text on two pages. Evidence explicitly cannot prove absence or compliance. | Keep conclusion `NOT_OBSERVABLE`; an authorized privacy-approved runtime/staging audit and controller/legal review are required for a live conclusion. | Measurement/Privacy |
| `CO-001` | Connectors/docs | Medium | `RESOLVED_AWAITING_VERIFICATION` | Execution-state active tools and cloned-application statuses describe different environments/capabilities. | Connector documentation now presents both axes and exact capability scope. Verify dashboard wording against the final artifact. | Connectors/Docs |
| `CO-002` | Connectors | Medium | `VERIFIED` | Source-specific Pydantic models validate dates, enums, non-negative measures and bounded rates before allow-listed projection; the normalized model forbids extras. | Malformed metric and unknown-field projection tests pass in the 22-test Python suite. | Connectors |
| `CO-003` | Connectors | Medium | `VERIFIED` | `ConnectorResult` now carries schema version, timezone, report range, currency and evidence reference; injected live reads implement bounded exponential retry for transient errors only. | Metadata and deterministic three-attempt/0.25–0.5 second retry tests pass. | Connectors |
| `SEC-001` | Security | Medium | `VERIFIED` | FastAPI unexpected-error logging now records only request ID and route, without exception text or traceback. | Log-capture privacy regression proves an injected upstream marker is absent from response and logs. | API/Security |
| `AR-001` | Architecture/operations | High | `RESOLVED_AWAITING_VERIFICATION` | Initial Compose referenced a missing API Dockerfile. `services/api/Dockerfile` and `.dockerignore` are now present. | Run Compose build, API health/readiness, web smoke check and cleanup on the release candidate. | Architecture/API |

## Review pass template

Complete each pass against the release candidate SHA. Add findings above, then record the pass result below.

### Architecture

- [ ] Public static and local-private boundaries match built code/network behavior.
- [ ] Contracts are aligned across generator, connectors, dbt, API and frontend.
- [ ] GitHub Pages base-path/direct-navigation behavior is verified.
- [ ] Complexity, failure states and maintainability reviewed.

### Analytics

- [ ] Every mart has one declared/tested grain.
- [ ] KPI formulas match SQL/API/UI and machine-readable catalog.
- [ ] Source precedence, filters, currency/timezone/refund scope are explicit.
- [ ] Fact joins and allocation avoid double counting.
- [ ] Expected anomalies are detected; unexpected failures are not hidden.

### Security and privacy

- [ ] Secrets/PII/private paths/history/bundle/release archives scanned.
- [ ] Connectors are read-only and least-scope; no silent fallback.
- [ ] Logs/errors/screenshots/evidence contain no protected data.
- [ ] Dependency/action/license review complete.
- [ ] Consent conclusions are scoped and evidence-based.

### Frontend and UX

- [ ] All main routes desktop/tablet/mobile in EN and AR.
- [ ] Correct `lang`/RTL, logical layout, readable charts/tables.
- [ ] Keyboard/focus/labels/contrast/axe review.
- [ ] Loading, empty, unsupported, unauthenticated and error states are distinct.
- [ ] Recruiter can understand problem, evidence and synthetic disclaimer quickly.

### Documentation and career

- [ ] Claims and counts match final evidence.
- [ ] Implemented work is separated from recommendations.
- [ ] No unmeasured business impact claim.
- [ ] German wording is natural and role-relevant.
- [ ] Final repository/demo/release/commit/workflow links are exact and verified.

## Pass results

| Pass | Reviewer | Candidate SHA | Result | Critical | High | Medium | Low | Evidence / date |
|---|---|---|---|---:|---:|---:|---:|---|
| Architecture | Technical documentation review | not yet final | `RESOLVED_AWAITING_VERIFICATION` | 0 | 0 | 0 | 0 | Dockerfile/config now present; runtime verification pending, 2026-08-28 |
| Analytics | Technical documentation review | not yet final | `RESOLVED_AWAITING_VERIFICATION` | 0 | 0 | 0 | 0 | Code inspection; track reports passing pytest/dbt runs, final counts/rerun pending, 2026-08-28 |
| Security/privacy/connectors | Technical documentation review | not yet final | `RESOLVED_AWAITING_FINAL_REVIEW` | 0 | 0 | 1 | 0 | Connector schema/metadata/retry and safe logging fixes verified locally; passive-audit limitation accepted, 2026-08-28 |
| Frontend/UX |  |  | `NOT_RUN` |  |  |  |  |  |
| Documentation/career |  |  | `NOT_RUN` |  |  |  |  |  |

## Resolution log

| Finding | Change/decision | Verification command/evidence | Reviewer | Date |
|---|---|---|---|---|
| `AN-001` | Gross/net/discount contract aligned across generator/marts/API | Track-reported pytest/dbt pass; exact final count/rerun pending | Technical documentation review | 2026-08-28 |
| `AN-002` | AOV aligned to net revenue/completed purchases | Track-reported semantic/API/dbt tests; final rerun pending | Technical documentation review | 2026-08-28 |
| `AN-003` | Proportional item refund allocation and margin semantics added | Track-reported reconciliation/dbt tests; final rerun pending | Technical documentation review | 2026-08-28 |
| `ME-001` | Eleven-event fixture and ten parameter/consent coverage fields added | `assert_event_spec_coverage.sql`; track-reported dbt pass; final rerun pending | Technical documentation review | 2026-08-28 |
| `AR-001` | API Dockerfile and Docker build context exclusions added | Static file review passed; Compose runtime verification pending | Technical documentation review | 2026-08-28 |
| `CO-002` | Added connector-specific Pydantic models and safe normalized projection | Python connector malformed-metric/unknown-field tests pass | Main release verification | 2026-08-28 |
| `CO-003` | Added metadata envelope and bounded transient retry/backoff | Python connector metadata and retry tests pass | Main release verification | 2026-08-28 |
| `SEC-001` | Removed exception payload/traceback logging and added privacy regression | `pnpm test:api` (22 passed after final rerun) | Main release verification | 2026-08-28 |

## Release decision

- Candidate SHA: `not yet recorded`
- Decision: **PENDING — no open critical/high finding in this documentation review; final runtime and multi-track verification is not yet recorded**
- Decision owner/date: pending
