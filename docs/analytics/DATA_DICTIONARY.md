# Data Dictionary

## Contract and conventions

This dictionary defines the analytical contract for both the deterministic `public-demo` and the local-only `live-private` path. The dbt manifest is the authority for the physical schema once generated; this document is the human-readable semantic layer. A field or model must not be presented as implemented merely because it is listed here.

### Global conventions

| Convention | Definition |
|---|---|
| Reporting date | Calendar date in the source reporting timezone. Cross-source comparisons require aligned timezone and inclusive date boundaries. |
| Currency | ISO 4217 uppercase code. Monetary values are decimal, never binary floating point in SQL calculations. SAR is expected for the demo, but currency must remain explicit. |
| Revenue scope | Merchandise revenue only unless a source-specific mapping explicitly includes tax or shipping. Mixing scopes is prohibited. |
| Missing numeric value | `NULL` means unavailable/not observable; zero means observed and equal to zero. They are not interchangeable. |
| Ratios | `NULL` when the denominator is `NULL` or zero. Percentages are stored as fractions from 0 to 1 and formatted at the presentation layer. |
| Source identity | Every row retains `source_system`; multi-source marts keep measures separate. |
| Data mode | `public-demo` or `live-private`. Public builds accept only `public-demo`. |
| Freshness | Derived from `report_through_at` and a connector-specific service-level expectation, not from file modification time. |
| Identifiers | Public identifiers are invented. Live direct customer/order identifiers are neither required nor retained. Pseudonymous keys are permitted locally only when necessary and reviewed. |
| Small groups | Live-private geography, coupon, campaign, or customer cohorts may be suppressed to reduce re-identification risk. |

### Common ingestion metadata

| Field | Type | Nullable | Meaning |
|---|---|---:|---|
| `source_system` | string | no | Stable source name such as `salla`, `ga4`, `gsc`, `merchant`, `clarity`, or `google_ads`. |
| `connector_mode` | enum | no | `fixture`, `import`, or `live_read`. |
| `connector_status` | enum | no | `CONNECTED`, `READY_NOT_AUTHENTICATED`, `FIXTURE_MODE`, `UNAVAILABLE`, or `FAILED_WITH_EVIDENCE`. |
| `data_mode` | enum | no | `public-demo` or `live-private`. |
| `schema_version` | string | no | Version of the normalized input contract. |
| `extracted_at` | timestamp | yes | When extraction/import completed; absent for data that has not been extracted. |
| `report_through_at` | timestamp | yes | Latest source period represented. |
| `source_timezone` | string | yes | IANA timezone or documented source setting. |
| `currency` | string | yes | ISO 4217 code when monetary measures exist. |
| `evidence_ref` | string | yes | Non-secret pointer to a log/report supporting a failed or limited state. |

## Implemented public-demo source schemas

The current fixed-seed implementation materializes these CSV schemas. All monetary fields are SAR. These physical fields are synthetic and must not be assumed to exist in every live connector.

| Seed/source | Physical grain | Key fields/measures |
|---|---|---|
| `products` | one row per invented product (12 rows) | `product_id`, EN/AR names, category, brand, list price, unit cost, active flag |
| `commerce_daily` | date × generated acquisition segment/device/city/payment (1,095 rows) | completed purchases, units, gross revenue, discount, refund, net revenue and reliable synthetic cost; no behavior or ad spend |
| `orders` | one invented order (9,075 rows) | order/tracking/customer demo keys, derived first-purchase date and stable lifecycle type, acquisition/device/city/payment/coupon/status, gross/discount/refund/net revenue |
| `order_items` | one invented order item line (9,075 rows) | order/date/product, quantity, pre-discount item revenue, cost, discount |
| `ga4_daily` | date × acquisition segment/device (1,095 rows) | sessions/users/funnel/purchases, purchase revenue, consent-state coverage |
| `ga4_product_daily` | date × acquisition segment/device × primary product (13,140 rows) | sessions, active user-days, funnel reaches and tracked purchases generated from an exogenous preference profile independent of order shares |
| `google_ads_daily` | date × paid acquisition campaign (364 rows) | clicks, conversions, conversion value and ad spend |
| `events` | date × source × device × eleven event names (12,045 rows) | event count plus coverage for transaction ID, currency, value, items, item ID/name/category, price, quantity, promotion and consent state |
| `search_console` | date × query × page × country × device (708 rows) | clicks, impressions, CTR, average position, branded flag |
| `merchant_diagnostics` | weekly snapshot × product (636 rows) | destination, status, issue code, affected items |
| `clarity_daily` | date × device/country (365 rows) | sessions, dead/rage clicks, excessive scrolls, JavaScript errors |

Dataset metadata records seed `20250301`, dates `2025-01-01`–`2025-12-31`, independent synthetic provenance, row counts, file hashes and the six intentional anomaly definitions.

## Dimensions

The current compact public warehouse keeps most dimension attributes on staging/intermediate/mart rows rather than materializing separate `dim_*` models. The sections below define the semantic dimension contract for joins and a future live-private extension; they must not be counted as implemented dbt models. Surrogate keys are warehouse-internal hashes or sequences. Natural keys from live systems must not be exposed publicly.

### `dim_date`

Grain: one row per calendar date.

| Field | Type | Meaning |
|---|---|---|
| `date_key` | date | Primary date key. |
| `year`, `quarter`, `month` | integer | Calendar components. |
| `iso_week` | integer | ISO-8601 week. |
| `day_of_week` | integer | ISO day, Monday = 1. |
| `is_weekend` | boolean | Saturday/Sunday flag for neutral international reporting; Saudi business-calendar analysis must be separately labelled. |

### `dim_product`

Grain: one row per conformed product key and valid version where history is retained.

| Field | Type | Privacy | Meaning |
|---|---|---|---|
| `product_key` | string | public-safe surrogate | Join key. |
| `source_product_id` | string | invented public; private locally | Vendor/item identifier. Never expose live values publicly. |
| `product_name` | string | public synthetic only | Display name. Live names require classification review. |
| `category_key` | string | aggregate safe | Conformed category. |
| `brand_key` | string | aggregate safe | Conformed brand/publisher. |
| `product_status` | string | aggregate safe | Normalized active/inactive/unknown status. |
| `cost_reliability` | enum | aggregate safe | `reliable`, `partial`, `unavailable`; gates margin metrics. |

### `dim_category` and `dim_brand`

Grain: one row per conformed category or brand. Fields include the surrogate key, public label, normalized grouping, and mapping status. Unknown values map to an explicit `unknown` member rather than disappearing from joins.

### `dim_acquisition`

Grain: one row per normalized channel/source/medium/campaign combination.

| Field | Type | Meaning |
|---|---|---|
| `acquisition_key` | string | Join key. |
| `channel_group` | string | Documented channel grouping. |
| `source`, `medium`, `campaign` | string | Normalized acquisition labels; potentially small live campaigns may be suppressed publicly. |
| `mapping_status` | enum | `mapped`, `unmapped`, or `not_applicable`. |
| `is_branded` | boolean/null | Campaign classification when rules support it. |

### `dim_device`

Grain: one row per normalized device category. Accepted public values are `desktop`, `mobile`, `tablet`, and `unknown`; source-specific device details may remain in staging only.

### `dim_geography`

Grain: one row per privacy-safe region/city grouping. Public-demo cities are invented records. Live-private outputs must not combine precise location with a small customer/product/coupon cohort.

### `dim_payment_method`

Grain: one row per normalized payment-method category. No account, card, wallet, or transaction credentials are stored.

### `dim_promotion`

Grain: one row per public-safe promotion grouping. Exact live private coupon codes are out of scope; use a synthetic code in public-demo or a local aggregate category/pseudonym where justified.

### `dim_customer_type`

Grain: one row per classification (`new`, `returning`, `unknown`). The classification window and source must be present in the consuming mart; `unknown` remains in denominators only where the KPI explicitly says so.

### `dim_connector`

Grain: one row per connector and observation time/version. Contains supported capabilities, current status, mode, freshness expectation, last success, report-through time, and a non-secret limitation summary.

## Facts

Likewise, the names below describe fact concepts. The current public implementation materializes eleven source-shaped staging models, five intermediate models and the twelve named marts rather than separate `fct_*` physical models for every concept.

### `fct_sessions`

Implemented GA4 fixture grain: date × channel/source/medium/campaign × device. Measures include `sessions`, daily active users, funnel counts, tracked purchases, purchase revenue and consent-state coverage. Aggregated marts rename summed daily active users to `active_user_days`; they never claim a distinct period user total. The product-scoped companion fixture uses a mutually exclusive primary-product allocation independent of commerce order shares. GA4 privacy thresholding or sampling metadata must accompany affected live extracts.

### `fct_events`

Implemented public grain: date × source × device × event name with aggregate event count and parameter/consent coverage ratios. All eleven target ecommerce events are present. The fixture intentionally does not expose individual event/session/customer payloads. A richer private import may retain privacy-safe aggregate dimensions, but raw live event payloads are not retained.

### `fct_funnel_daily`

Grain: date × source × device, with distinct session counts reaching `view_item`, `add_to_cart`, `begin_checkout`, and `purchase`. A session is counted once per step. Event count and session-reach count are separate measures.

### `fct_orders`

Public-demo grain: one synthetic order. Live-private target grain: order-level only when necessary locally; otherwise pre-aggregated date × safe dimensions. Core fields include order status, completion date, currency, pre-discount merchandise value, discount, refund, and net merchandise revenue. Test/failed/cancelled orders are excluded from completed-order KPIs according to the source status mapping.

### `fct_order_items`

Grain: one item line per synthetic order and product in public-demo; minimized local line-level records only when product/category analysis requires them. Measures include quantity, unit list price, allocated discount, allocated refund, allocated net revenue, and allocated cost where reliable. Allocation residuals must be deterministically assigned and reconciliation-tested.

### `fct_refunds`

Grain: refund occurrence or source-supported daily aggregate. Fields include effective refund date, related safe transaction key where permitted, refund value, currency, quantity, and full/partial indicator. Refund timing is not silently backdated to purchase date.

### `fct_ad_performance`

Grain: date × account-safe campaign key × device/channel where supported. Measures include spend, impressions, clicks, source-reported conversions, and conversion value. ROAS/CPA require comparable attribution scope and reliable spend.

### `fct_search_performance`

Grain: date × query × page × country × device as exported by Search Console. Measures include clicks, impressions, CTR, and average position. Query rows may be omitted by source privacy controls; aggregates across dimensions may not reconcile because the API can return different top-row sets.

### `fct_merchant_diagnostics`

Grain: snapshot date × safe product key × destination/country × diagnostic code where available. Fields include severity, status, affected state, and non-sensitive message/category. This is read-only reporting, not feed mutation.

### `fct_behavior_daily`

Grain: date × device × country/region where the Clarity export supports it. Measures may include sessions, dead clicks, rage clicks, excessive scrolls, and JavaScript errors. A behavioral signal is diagnostic, not proof of causation.

### `fct_data_quality_results`

Grain: test execution × rule ID × source/model. Fields include severity, status, rows evaluated, affected rows, rate, threshold, affected KPI, evidence reference, and remediation state. A passing test proves only the stated rule at that execution.

### `fct_source_reconciliation`

Grain: reporting date × metric × comparison dimensions. Stores merchant value, GA4 value, absolute variance, percentage variance, aligned scope flags, and explanation codes. A variance is unavailable when source scope or denominators cannot be aligned.

## Analytical marts

| Mart | Declared grain | Primary measures | Join/usage cautions |
|---|---|---|---|
| `mart_executive_daily` | date | completed orders, gross/net revenue, refunds, GA4 sessions, active user-days, tracked purchases and conversion | Cross-source measures stay labelled; do not sum ratios or call user-days distinct users. |
| `mart_funnel_daily` | date × device × channel/source | distinct sessions per funnel step and step rates | Pre-aggregate before joining to orders. |
| `mart_product_performance` | product | units, pre-discount revenue, discount, allocated refund, net revenue, reliable synthetic margin | Unknown product is explicit; current public mart is full-period. |
| `mart_category_performance` | category | units, pre-discount revenue, discount, allocated refund, net revenue/share, reliable synthetic margin | Current public mart is full-period; category share uses the same scope. |
| `mart_acquisition_performance` | channel × source × medium | active user-days, GA4 sessions/tracked purchases/purchase revenue, Ads spend, conversion and ROAS | `active_user_days` is additive and not a distinct-user claim; GA4 and Ads scopes must align. |
| `mart_campaign_performance` | campaign × channel | GA4 sessions/tracked purchases/purchase revenue, Ads spend, CPA/ROAS | Current public mart is full-period synthetic; do not mix incompatible live attribution scopes. |
| `mart_search_performance` | query × page × branded flag | clicks, impressions, CTR, weighted position, fresh-through date | Current public mart rolls up country/device/date; GSC detail may not reconcile to property totals. |
| `mart_customer_mix` | customer type | anonymous synthetic customers, orders, net revenue, orders/customer, revenue share | Public pseudonyms are invented; live identity requires a separate privacy decision. |
| `mart_payment_performance` | payment method | orders, revenue, refunds, refund rate, AOV | Current public mart is full-period; no payment credentials. |
| `mart_data_quality` | check ID | metric, threshold, affected rows, severity, status | Six implemented checks detect the six documented synthetic anomalies; they are demo warnings, not live defects. |
| `mart_source_reconciliation` | date | Salla-like and GA4 purchases/net revenue, absolute variance rates, 10% daily tolerance flag | Public sources are synthetic; only aligned live scopes are comparable. |
| `mart_prioritized_insights` | insight ID | priority, area, title, evidence, confidence, recommended action | Recommendation, not measured impact; current public set contains three insights. |

## Join rules and double-counting controls

1. Aggregate facts to the same declared grain before joining.
2. Never join session/event rows directly to order-item rows; both are many-to-many by user/session/transaction in common implementations.
3. Count orders by the deduplicated commerce transaction key, not by item rows or `purchase` event count.
4. Allocate order discounts/refunds/costs to item lines exactly once and test item sums against order totals.
5. Use effective refund date for refund trends; use purchase cohort date only in explicitly named cohort analyses.
6. Do not sum distinct users across dates, devices, channels, or campaigns and call the result a period user count.
7. Use impression-weighted average position when rolling up GSC rows: `sum(position * impressions) / sum(impressions)`.
8. A source's `unknown` dimension member must remain visible until mapping; inner joins that discard it are prohibited.

## Quality expectations

At minimum, physical models must test uniqueness at the declared grain, required fields, accepted status/currency/device values, dimension relationships, valid dates, non-negative bounded measures, order-to-item reconciliation, duplicate transaction logic, and source-variance thresholds. Exact results belong in the test report, not this dictionary.
