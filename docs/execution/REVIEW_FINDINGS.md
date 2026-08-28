# Independent Review Findings

## Review policy

This register records architecture, analytics, connector/security, frontend and documentation review. It distinguishes implemented evidence from recommendations and external limitations. Critical/high findings block public release until verified; accepted limitations must remain visible and must not be presented as passed behavior.

| Severity | Meaning | Release rule |
|---|---|---|
| Critical | Public/private boundary break, secret/PII exposure, mutation risk or materially false release evidence | Block immediately |
| High | Material KPI, privacy, security, accessibility or functional error likely to mislead | Block until resolved and verified |
| Medium | Significant bounded limitation or inconsistency | Fix or document owner/rationale |
| Low | Minor maintainability or presentation issue | May defer |

Statuses are `OPEN`, `IN_PROGRESS`, `RESOLVED_AWAITING_VERIFICATION`, `VERIFIED` and `ACCEPTED_LIMITATION`.

## Findings register

| ID | Track | Severity | Status | Finding and evidence | Resolution / remaining action |
|---|---|---|---|---|---|
| `AN-001` | KPI semantics | High | `VERIFIED` | Earlier gross/net/AOV/margin definitions diverged. | Gross is pre-discount/pre-refund; net subtracts discount/refund; AOV uses net/completed orders; margin uses net minus synthetic cost. Revenue and reconciliation tests pass. |
| `AN-002` | Grain/source | High | `VERIFIED` | Independent review found GA4-defined funnel/acquisition measures sourced from commerce aggregates and users summed as if period-distinct. | Funnel/acquisition now source GA4 models; spend sources a separate Ads seed; UI/API label the additive measure `active_user_days`. Source/grain tests pass. |
| `AN-003` | Product behavior | High | `VERIFIED` | Product sessions/funnel measures were allocated from commerce order groups, creating unsupported product conversion denominators. | A separate `ga4_product_daily` fixture and staging model now provide declared product-behavior grain; totals reconcile to GA4, and generator/dbt regression tests pass. |
| `AN-004` | Customer lifecycle | High | `VERIFIED` | Recurrent synthetic customers could appear in both `new` and `returning`, while UI copy claimed first-purchase classification. | Generator now assigns immutable first-purchase date/type per customer and fails on drift. Customer stability tests pass. |
| `AN-005` | Payment KPI | Medium | `VERIFIED` | Payment refund-rate denominator differed from the canonical gross-revenue formula. | Mart denominator is now gross item revenue and semantic regression coverage passes. |
| `AN-006` | Quality/reconciliation | Medium | `VERIFIED` | API/dbt check IDs, completeness grains and consent presentation diverged; global tolerance was 15% while daily policy was 10%. | Quality computation and IDs are aligned; UI consumes generated consent evidence; global tolerance is 10%; exact anomaly-count and cross-runtime tests pass. |
| `DT-001` | Determinism | High | `VERIFIED` | The manifest previously captured a stale recursive `metadata.json` hash. | Metadata is excluded from the first payload scan, written once, then hashed into the manifest. Current manifest has zero mismatches and a dedicated regression test. |
| `CO-001` | Salla connector | High | `VERIFIED` | Live Salla aggregate rows could return `CONNECTED` without operation-specific required fields. | Each allow-listed operation now has required aggregate-field groups; malformed live projection is rejected and tested. |
| `CO-002` | Connector status | Medium | `VERIFIED` | File imports were conflated with `FIXTURE_MODE`, and Salla fallback evidence did not fully match implementation. | `FILE_MODE` is distinct and tested; generated connector evidence matches current fixture/import behavior. |
| `CO-003` | Connector controls | Medium | `VERIFIED` | Typed metadata, bounded retries and safe projection required proof. | Six source-specific models, typed result metadata, transient-only retries and unknown-field stripping pass the 26-test Python suite. Public statuses remain `FIXTURE_MODE`; fresh-clone live statuses remain unauthenticated. |
| `ME-001` | Measurement | Medium | `VERIFIED` | Initial fixture/event tests did not fully cover the requested commerce sequence and exact anomaly behavior. | All eleven requested event names and parameter/consent coverage fields are present; exact expected anomaly counts are asserted in dbt/generator tests. Live storefront coverage remains unobserved. |
| `SEC-001` | Security/privacy | High | `VERIFIED` | Public artifacts required evidence against secrets, PII, private paths and error-payload leakage. | Release evidence reports no findings; API log regression excludes injected private markers; screenshot manifest records eight privacy-review passes. |
| `AR-001` | Containers | Medium | `ACCEPTED_LIMITATION` | Compose files validate, but the local Docker Desktop Linux engine is unavailable, so image build/runtime health were not executed locally. | Keep runtime status unverified. CI is designed for build/up/health/web/down smoke; record success only after an observed workflow run. |
| `PERF-001` | Performance | Medium | `ACCEPTED_LIMITATION` | Lighthouse mobile performance is 46 despite 100 accessibility/best-practices/SEO; audit reports about 428 KiB transfer, 4.46 s TBT and CLS 0.353. | Reduce payload/client work/layout shift and rerun the same mobile profile. Do not summarize current performance as uniformly green. |
| `PRIV-001` | Consent audit | Medium | `ACCEPTED_LIMITATION` | Passive storefront evidence could not observe a complete consent default/update journey or prove legal compliance. | Preserve `NOT_OBSERVABLE`; require authorized runtime/staging validation and controller/legal review. Portfolio implementation is not legal advice. |

## Final verification snapshot

| Pass | Result | Evidence |
|---|---|---|
| Architecture and source/grain review | `VERIFIED` with container limitation | Static/public-private boundaries reviewed; independent high findings remediated; Compose syntax passes |
| Analytics | `VERIFIED` | 28 models + 78 data tests + 11 seeds = 117/117 successful dbt nodes |
| Python/API/connectors/generator | `VERIFIED` | 26 tests passed |
| Frontend unit/type safety | `VERIFIED` | 10 unit tests passed; TypeScript check passed |
| Browser behavior | `VERIFIED` | 11 E2E checks passed across nine routes and interaction/mobile workflows |
| Accessibility | `VERIFIED` | 6 checks passed; no serious/critical axe finding in tested routes |
| Static export | `VERIFIED` | 1 scenario passed across all nine direct-navigation routes under base path |
| Public release/privacy scan | `VERIFIED` | Release checker `PASS`; eight screenshot privacy reviews `PASS` |
| Lighthouse | `ACCEPTED_LIMITATION` | Desktop 85/100/100/100; mobile 46/100/100/100 |
| Local Compose runtime | `NOT_RUN` | Docker engine unavailable; CI smoke designed, not yet evidenced here |

## Resolution evidence

- Current dbt `manifest.json` records 28 models and 78 tests; `run_results.json` records 117 passing/successful nodes.
- The current public manifest verifies every declared file hash with zero mismatch.
- Connector status evidence contains six entries, all `FIXTURE_MODE`, with no payloads persisted.
- Browser test definitions expand to eleven E2E and six accessibility checks; the last Playwright result is passed.
- Screenshot evidence contains eight hashed, privacy-reviewed `public-demo` captures.
- Lighthouse artifacts record the desktop/mobile score sets and payload/performance limitations above.
- `docker compose config --quiet` passes; `docker info` fails because the local Docker Desktop Linux engine socket is unavailable.

## Release decision

- Candidate SHA: not final; working tree under review
- Critical findings: 0 open
- High findings: 0 open
- Decision: **CONDITIONAL**
- Conditions: successful final clean-clone/CI run, exact public-link verification, and continued disclosure of the local container and mobile-performance limitations
- Commercial claim status: no measured revenue, conversion, traffic, SEO or cost-saving uplift claimed
