# Data Classification

## Classification levels

Classification follows the most sensitive field in a file, row, screenshot, log, database, archive, or derived output. Aggregation does not automatically lower classification; document the transformation and disclosure review.

| Level | Definition | Examples | Allowed location | Public release |
|---|---|---|---|---|
| **P0 — Public synthetic** | Independently invented/generated information approved for publication | Fixed-seed demo orders/events/products, public docs, reviewed screenshot, public artifact hash | Tracked repository and public artifacts | Yes after release review |
| **P1 — Internal operational** | Non-secret project operations with low disclosure impact | Local build timing, non-sensitive test logs, draft review notes, dependency inventory | Repository only when publication-safe; otherwise local work | Case-by-case |
| **P2 — Confidential business** | Live aggregate or strategy information that could harm the merchant if disclosed | Exact revenue/orders/refunds, campaign performance, product diagnostics, live catalog/coupon/cost details | Ignored encrypted/restricted local storage | No |
| **P3 — Restricted personal/security** | Personal data, credentials, tokens, auth metadata or highly linkable records | Name, email, phone, address, customer/order reference, session/user ID, IP, OAuth token, cookie, service-account JSON, raw MCP response | Do not ingest when avoidable; approved secret store or restricted transient processing only | Never |
| **P4 — Prohibited project data** | Data the project must not process/store for its purpose | Passwords, recovery/one-time codes, full card/bank data, raw authorization payloads, customer messages, supplier secrets unrelated to KPI need | Nowhere in project storage/logs/chat | Never |

## Field-level decision table

| Field/data | Public demo | Live-private | Classification | Transformation/control |
|---|---|---|---|---|
| Product ID/name/category | Invented | Local only unless approved aggregate | P0 demo / P2 live | Conformed key; public values independent |
| Order/transaction ID | Invented opaque | Avoid retention; local pseudonym if needed | P0 demo / P3 live | Never publish; no reversible mapping in repo |
| Customer identity | Invented type only | Direct identifiers excluded | P3/P4 | Use aggregate new/returning; keyed pseudonym only after review |
| Order timestamp | Invented | Reduce to date when possible | P0 demo / P2–P3 live | Date aggregation and small-group control |
| Revenue/discount/refund | Invented | Exact values local only | P0 demo / P2 live | Aggregate; never quote in public docs |
| Cost/margin | Invented reliable fixture where marked | Restricted, only if reliable/necessary | P0 demo / P2 live | Access limitation; conditional KPI |
| City/region | Invented | Coarse aggregate/suppressed | P0 demo / P2–P3 combined | Minimum-group/differencing review |
| Payment method | Invented category | Safe category only | P0 demo / P2 live | No account/card/token/auth outcome |
| Coupon/promotion | Invented code | Aggregate/pseudonym/category | P0 demo / P2–P3 live | Never publish targeted/private codes |
| GA4 Client/User ID | Invented session key | Exclude by default | P3 | Aggregate reporting; separate privacy review for User-ID |
| Source/medium/campaign | Invented | Aggregate; suppress rare/targeted values | P0 demo / P2 live | Mapping and small-group review |
| Search query/page URL | Invented/sanitized | Validate for PII/query strings | P0 demo / P2–P3 live | Strip identifiers; classify free text conservatively |
| Clarity behavior metric | Invented aggregate | Aggregate only | P0 demo / P2 live | No recording/session identifier/public private values |
| Merchant diagnostic | Invented | Aggregate local | P0 demo / P2 live | Remove product/account identifiers as needed |
| Connector credential | Never | Secret manager/session only | P3/P4 | Never file/log/chat/screenshot |
| Raw API/MCP response | Never | Do not persist | P3 until proven otherwise | Minimize into validated schema in memory/local restricted path |
| Error/stack trace | Synthetic/sanitized | Treat as potentially restricted | P1–P3 | Structured safe code; no payload/header/query values |

## Location and handling matrix

| Location | P0 | P1 | P2 | P3/P4 |
|---|:---:|:---:|:---:|:---:|
| Tracked Git files | Yes | Only if publication-safe | No | No |
| GitHub issue/Actions log | Yes | Only if publication-safe | No | No |
| `data/public-demo/` | Yes | No | No | No |
| Ignored `data/private/` or `.private/` | No need | Yes | Yes with local access controls | P3 transient/minimized only; P4 no |
| Local DuckDB/cache | Public build: P0 only | Yes | Live-private local only | Avoid; minimize and expire |
| Public browser/static bundle | Yes | Only reviewed public operational metadata | No | No |
| Screenshot/CV/social/release ZIP | Reviewed P0 only | No | No | No |
| Chat/prompt/command output | Public-safe facts only | Cautious | Never exact values | Never |

## Classification workflow

1. Identify the business purpose and minimum fields.
2. Classify each source field before import; unknown/free-text fields default to P3.
3. Reject P4 and unnecessary P3 fields.
4. Minimize/aggregate/pseudonymize permitted inputs in the trusted local zone.
5. Reclassify derived outputs based on linkage, group size, rare dimensions and differencing—not only removed column names.
6. Enforce allowed storage, access, retention and logging.
7. Re-review any output moving to a lower-trust zone.

## Declassification to public

Only independent synthetic data can normally be classified P0 for this project. Do not “anonymize” live metrics by multiplying, adding noise, rounding, changing labels, screenshot cropping, or removing a merchant name; those outputs remain private and can leak scale/distribution.

A public artifact requires:

- independent synthetic provenance;
- visible synthetic disclosure where numbers appear;
- no P2/P3/P4 field or exact private metric;
- no secret/private endpoint in metadata, source map, link or bundled code;
- privacy scan and human review tied to the commit/hash;
- allowed-license/provenance review.

## Test fixtures and anomalies

Test data is P0 only when independently synthetic. Seeded defects such as duplicate transaction IDs, missing parameters, stale timestamps, unknown products and source variance must be documented as synthetic. Never copy a real malformed row into fixtures, even after changing a single identifier.

## Incident rule

When classification is uncertain, stop the data movement, treat it as P3, keep it out of Git/public tools, and ask the project privacy/security owner through an approved private channel. See the incident procedure in [PRIVACY_DESIGN.md](PRIVACY_DESIGN.md).

