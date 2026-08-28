# Connector Status

- Snapshot date: 2026-08-28
- Status sources: [`docs/execution/EXECUTION_STATE.md`](../execution/EXECUTION_STATE.md) and [`artifacts/evidence/connector-status.json`](../../artifacts/evidence/connector-status.json)
- Public artifact mode: `public-demo` only

## How to interpret this page

There are two independent facts:

1. **Active-environment observation** says what the executing Codex environment could safely reach during inspection.
2. **Repository adapter evidence** says whether the cloned project's fixture/import/live adapter and tests have been completed.

A reachable account-discovery call is not proof of report extraction. A working fixture is not proof of authentication. No status on this page implies that live data is safe for publication.

Supported runtime status values:

| Status | Meaning |
|---|---|
| `CONNECTED` | The specifically named read-only operation was observed to succeed in the active environment. Scope still matters. |
| `READY_NOT_AUTHENTICATED` | Interface/configuration path exists, but usable authentication was not available. |
| `FIXTURE_MODE` | Deterministic public fixture path is selected. This does not indicate live connectivity. |
| `UNAVAILABLE` | Required tool/interface was not available in the active environment. |
| `FAILED_WITH_EVIDENCE` | A read was attempted and failed; a safe evidence reference explains the failure. |

## Application status artifact

The generated public artifact selects the deterministic fixture for all six adapters. A fresh clone has no live credentials/executor, so every application live status is `READY_NOT_AUTHENTICATED`. This is the status the dashboard may present publicly.

| Connector | Public status | Fresh-clone live status | Implemented fallback | Read-only | Fixture through |
|---|---|---|---|:---:|---|
| PrimeOrder/Salla MCP | `FIXTURE_MODE` | `READY_NOT_AUTHENTICATED` | JSON record import plus generated fixture | Yes | 2025-12-31 |
| GA4 | `FIXTURE_MODE` | `READY_NOT_AUTHENTICATED` | CSV/JSON plus generated fixture | Yes | 2025-12-31 |
| Google Search Console | `FIXTURE_MODE` | `READY_NOT_AUTHENTICATED` | CSV/JSON plus generated fixture | Yes | 2025-12-20 (intentionally stale anomaly) |
| Google Merchant Center | `FIXTURE_MODE` | `READY_NOT_AUTHENTICATED` | CSV/JSON plus generated fixture | Yes | 2025-12-31 |
| Microsoft Clarity | `FIXTURE_MODE` | `READY_NOT_AUTHENTICATED` | CSV/JSON plus generated fixture | Yes | 2025-12-31 |
| Google Ads | `FIXTURE_MODE` | `READY_NOT_AUTHENTICATED` | CSV/JSON plus generated commerce/campaign fixture | Yes | 2025-12-31 |

The adapter registry, generated fixture paths and status evidence are implemented. Source-specific Pydantic models validate types, enum domains, non-negative measures and bounded rates before projecting onto an allow-listed normalized record. Unknown fields are discarded at the source boundary, while the normalized model forbids extras.

## Active Codex environment observations

These point-in-time execution observations do not flow into a cloned application and do not replace the status artifact:

| Connector | Observed state | Exact scope/caveat |
|---|---|---|
| PrimeOrder/Salla MCP | `CONNECTED` | Read-only aggregate report reachability; no live values or raw response persisted publicly |
| GA4 | `CONNECTED` | Account discovery only; no claim of Data API reporting/event-parameter extraction |
| Search Console | `READY_NOT_AUTHENTICATED` | Credential path absent |
| Merchant Center | `UNAVAILABLE` | No supported Merchant tool was exposed in that active tool set |
| Clarity | `CONNECTED` | Aggregate query reachability; no live values persisted publicly |
| Google Ads | `UNAVAILABLE` | GA4 link discovery only, not direct Ads reporting authentication |

This difference is expected: the active Codex environment may provide tool-managed sessions, while the repository/application intentionally ships none. Future status changes require capability-specific evidence, not inference.

## Capability matrix

The fixture and file adapter paths below are implemented; live execution remains environment-owned and unauthenticated in the public artifact.

| Connector | Read-only live target | Fixture target | CSV/JSON import target | Core normalized reporting |
|---|:---:|:---:|:---:|---|
| Salla MCP | Yes, via injected MCP aggregate bridge only | Yes | JSON | orders, revenue/refunds, items/products/categories, payment, coupon, device, privacy-safe geography, abandoned-cart aggregate where source supports it |
| GA4 | Yes | Yes | Yes | users/sessions, acquisition, device/landing page, ecommerce events/items/transactions/revenue/refunds |
| Search Console | Yes | Yes | Yes | query/page/country/device/date, clicks, impressions, CTR, position |
| Merchant | Yes when a supported current interface is available | Yes | Yes | product/feed status and diagnostics; no product mutation |
| Clarity | Yes where aggregate export/query is supported | Yes | Yes | sessions, device/country, dead/rage clicks, excessive scroll, JS errors where available |
| Google Ads | Optional | Yes | Yes | campaign spend, clicks, impressions, conversions and conversion value |

## Connector contract

The implemented `ConnectorResult` envelope includes connector ID, schema version, status, mode, read-only flag, fetch time, optional fresh-through date, source timezone, report range, currency, evidence reference, record count, normalized records, warnings and a safe typed error.

Target adapter responses include:

- connector/source ID and schema version;
- selected `data_mode` and connector mode (`fixture`, `import`, `live_read`);
- supported status value and status scope;
- fetch time, available `fresh_through`, source timezone and report range metadata;
- reporting date range and currency where relevant;
- typed result/status/error envelope and required-field-validated normalized records;
- source caveats such as thresholding, sampling, row limits, missing dimensions, quota state, or unsupported capabilities;
- safe warning/error code and evidence reference without credentials, auth metadata, raw private payloads, or PII.

Mode selection is explicit. A failed live read never silently returns fixtures while retaining `CONNECTED` or a live label. Source-specific models, schema version `1.0.0`, `Asia/Riyadh` source timezone, report range, `SAR` currency and an evidence reference are verified by connector tests.

## Import rules

1. Accept only documented CSV/JSON schemas and declared schema versions.
2. Validate header/field names, types, enums, currency, timezone, dates, and reporting range before ingestion.
3. Reject unexpected sensitive columns in public-demo imports.
4. Store live/private imports only under ignored `data/private/` or `.private/` paths.
5. Preserve source record counts and validation outcomes, but never publicize exact private metrics.
6. Quarantine invalid rows with reason codes locally; do not coerce an invalid ID/date/value to a plausible value.
7. Record a content hash and extraction/report-through metadata in local evidence where safe.

## Retry and failure policy

All operations are idempotent reads. The base class performs at most three attempts (`max_retries = 2`) for transient timeouts, connection errors and operating-system read failures, with deterministic exponential delays of 0.25 and 0.5 seconds. Authentication/schema failures are not retried. Tests inject the sleeper and prove both the attempt count and delay schedule. Vendor-specific `Retry-After` parsing and jitter remain future operational hardening.

| Condition | Behavior |
|---|---|
| Authentication missing/expired (`401`) | Do not loop; return `READY_NOT_AUTHENTICATED` with safe setup guidance. |
| Forbidden/scope error (`403`) | Do not broaden permissions automatically; return `FAILED_WITH_EVIDENCE` or `READY_NOT_AUTHENTICATED` according to evidence. |
| Rate limit (`429`) | Honor `Retry-After`; exponential backoff with jitter; bounded attempts; preserve last safe status. |
| Transient upstream/server error (`5xx`, timeout) | Bounded retry (target maximum three attempts) with backoff and safe evidence. |
| Schema/validation failure | No retry; quarantine/reject input and return `FAILED_WITH_EVIDENCE`. |
| Unsupported capability/tool absent | `UNAVAILABLE`; do not substitute another private integration that violates the architecture. |
| Partial report/page failure | Do not publish partial totals as complete; identify coverage and fail or mark partial according to connector contract. |

Retries must not log request headers, tokens, cookies, authorization metadata, raw private payloads, or customer identifiers.

## Source-specific caveats

### PrimeOrder/Salla MCP

- MCP access is read-only. No product/order/customer/store/tracking mutation is permitted.
- Prefer official report-derived aggregates.
- The deployed site cannot call MCP; an authorized analyst uses a documented local export bridge.
- Minimize/pseudonymize before local persistence. Raw MCP responses and order/customer identifiers are prohibited from tracked/public files.
- A missing MCP function or upstream error is recorded; fixtures remain visibly `FIXTURE_MODE`.

### GA4

- Account discovery and report access are separate capabilities.
- Data API quota, thresholding, sampling (where applicable), cardinality, `(other)` rows, retention, identity settings, reporting timezone, currency, and processing latency can affect results.
- Aggregate reports often cannot expose all event/item parameters or consent state; label such checks `NOT_OBSERVABLE` rather than pass.
- GA4 revenue and transactions are measurement outputs, not the merchant financial authority.

### Search Console

- Query privacy filtering, top-row limits, dimensions, and aggregation type can cause detail rows not to reconcile with property totals.
- CTR must be recalculated from clicks/impressions; rolled-up position is impression-weighted.
- Inspection/indexing mutation is out of scope; the connector is reporting-only.

### Merchant

- Use only the current supported read/report interface available at execution time.
- Diagnostics can be delayed and scoped by destination/country; a diagnostic snapshot is not a real-time feed state.
- No product, feed, destination, account, or policy setting changes are permitted.
- Current primary references: [Merchant API latest updates](https://developers.google.com/merchant/api/latest-updates) and the read-only [reports resource](https://developers.google.com/merchant/api/reference/rest/reports_v1/accounts.reports).

### Clarity

- Behavioral indicators are aggregate diagnostic signals, not proof of user intent or causation.
- Export availability, dimension granularity, quotas, retention, and sampling/aggregation require source evidence.
- No recordings, free-text, or personal/session identifiers belong in public artifacts.
- Product capabilities and limitations should be checked against the current [Microsoft Clarity documentation](https://learn.microsoft.com/en-us/clarity/).

### Google Ads

- Optional live connector. Link discovery in GA4 does not prove Ads authentication.
- Spend, conversions, and value require aligned customer/account, currency, attribution window, and conversion actions before CPA/ROAS.
- Read-only reporting only; no campaign, bid, audience, budget, conversion, or spend changes.

## Authentication and secrets

Use existing official credential flows, environment configuration, OS credential storage, or tool-managed sessions. Never request or store passwords, PATs, OAuth tokens, API secrets, service-account JSON, cookies, or recovery codes in repository files, command logs, screenshots, or chat. `.env.example` contains names only. Local secret files must remain ignored.

## Status update procedure

For each status change, record date/time, connector version, exact capability tested, mode, safe command/test reference, report-through time, limitation, and reviewer. Update both this human-readable page and the machine-readable artifact from the same evidence. Do not copy live totals into either public status record.
