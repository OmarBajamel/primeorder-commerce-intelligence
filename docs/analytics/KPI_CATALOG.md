# KPI Catalog

- Catalog version: `1.0.0`
- Effective date: 2026-08-28
- Semantic owner: Commerce Analytics
- Technical owner: Data Engineering
- Machine-readable companion: [`kpi_definitions.yml`](kpi_definitions.yml)

## Reading this catalog

Availability values are deliberately strict:

- `AVAILABLE_PUBLIC_DEMO`: implemented from deterministic fixtures and safe for public presentation.
- `CONDITIONAL`: available only when the named input is present, reliable, aligned, and privacy-safe.
- `NOT_AVAILABLE`: unsupported in the selected mode/source.
- `NOT_VERIFIED`: specified here, but implementation/test evidence has not yet been recorded.

The current public implementation exposes the commerce, funnel, acquisition, SEO, margin and quality measures marked `AVAILABLE_PUBLIC_DEMO` below. Track verification reported the associated semantic/dbt tests passing; the release owner must re-run them on the final commit. Live availability remains conditional on authenticated source capability, scope alignment and privacy review.

All dashboard KPIs must link to or reproduce the applicable definition, source, scope, and caveat. Ratios return `NULL` when the denominator is zero or unavailable. Dashboard filters apply to numerator and denominator unless stated otherwise.

## Source precedence

| Code | Precedence rule |
|---|---|
| `COMMERCE` | Official PrimeOrder/Salla commerce report for completed orders, revenue, discounts, refunds, payment and product/category performance; validated import next; fixture in public-demo. |
| `GA4` | GA4 reporting for users, sessions, behavioral funnel, and GA4-attributed acquisition; validated import next; fixture in public-demo. |
| `GSC` | Search Console for organic search queries/pages/clicks/impressions/position; validated import next; fixture in public-demo. |
| `ADS` | Google Ads for spend, clicks, impressions, Ads conversions/value; validated import next; fixture in public-demo. |
| `MERCHANT` | Merchant reporting for product/feed diagnostic status; validated import next; fixture in public-demo. |
| `CLARITY` | Clarity for aggregate UX indicators; validated import next; fixture in public-demo. |
| `RECONCILED` | Keep source values side by side after aligning date, timezone, currency, status, and metric scope. Never average sources. |

### Commerce KPIs

| ID / KPI | Formula | Source priority | Filters and grain | Caveats | Availability |
|---|---|---|---|---|---|
| `commerce.gross_revenue` Gross revenue | `SUM(quantity × unit_list_price)` for completed merchandise lines before discounts and refunds | `COMMERCE` | Completed orders; date × selected dimensions | Excludes tax/shipping unless the source mapping explicitly says otherwise. Do not compare with a tax-inclusive source. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.discount_value` Discount value | `SUM(allocated_item_discount + allocated_order_discount)` | `COMMERCE` | Completed orders; date × product/category/promotion | Allocation must reconcile to order totals; private coupon codes are not exposed. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.refund_value` Refund value | `SUM(refund_value)` by refund-effective date | `COMMERCE` | Valid refunds; date × selected dimensions | Partial refunds and late refunds can make purchase-period and refund-period views differ. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.net_revenue` Net revenue | `gross_revenue - discount_value - refund_value` | `COMMERCE` | Completed commerce scope; date × selected dimensions | Defined as net merchandise revenue, not accounting revenue. Taxes, shipping, fees and chargebacks require explicit mapping. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.completed_orders` Completed orders | `COUNT(DISTINCT commerce_transaction_key)` after source-status mapping and deduplication | `COMMERCE` | Completion date × selected dimensions | One transaction counted once; cancelled, failed, test and duplicate orders excluded. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.units_sold` Units sold | `SUM(quantity)` on completed order items | `COMMERCE` | Completion date × product/category | Refund quantities are not subtracted unless labelled `net_units`; bundles need item mapping. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.aov` Average order value | `net_revenue / completed_orders` | `COMMERCE` | Same filters/date scope for both inputs | This is net-merchandise AOV; sources using gross or tax-inclusive AOV are not directly comparable. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.refund_rate_value` Refund rate | `refund_value / gross_revenue` | `COMMERCE` | Aligned currency and selected reporting window | Refund-effective-date reporting may exceed 100% in a short period when older purchases are refunded; purchase-cohort rate is a separate analysis. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.revenue_per_session` Revenue per session | `GA4 purchase_revenue / GA4 sessions` | `GA4` | Date × acquisition/device in the GA4 measurement plane | Commerce revenue is not silently divided by GA4 sessions; any cross-source variant must be explicitly reconciled. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.revenue_per_user` Revenue per user | `GA4 purchase_revenue / GA4 users` | `GA4` | Selected period and same GA4 reporting identity/scope | GA4 users are not additive across rows; thresholding and identity settings apply. | `NOT_VERIFIED` |
| `commerce.product_revenue_share` Product revenue share | `product net_revenue / total net_revenue in the same filter context` | `COMMERCE` | Period × product | The denominator changes with filters; unknown product remains visible. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.category_revenue_share` Category revenue share | `category net_revenue / total net_revenue in the same filter context` | `COMMERCE` | Period × category | Category mapping changes can affect history; unknown category remains visible. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.gross_margin` Gross margin | `net_revenue - attributable_cost` | `COMMERCE` + governed cost input | Period × product/category | Public-demo cost is explicitly reliable synthetic input; live publication remains conditional. Excludes unallocated operating costs. | `AVAILABLE_PUBLIC_DEMO` |
| `commerce.margin_rate` Margin rate | `gross_margin / net_revenue` | `COMMERCE` + governed cost input | Same filters for both inputs | Undefined at zero net revenue; public-demo is available, live availability inherits cost/revenue reliability. | `AVAILABLE_PUBLIC_DEMO` |

### Funnel KPIs

Funnel steps use distinct sessions reaching the event, not raw event counts. A session may reach later steps without an observable earlier event; such event-order defects remain flagged rather than being rewritten.

| ID / KPI | Formula | Source priority | Filters and grain | Caveats | Availability |
|---|---|---|---|---|---|
| `funnel.product_view_rate` Product-view rate | `sessions_with_view_item / sessions` | `GA4` | Date × device × acquisition | Consent and blockers can reduce observed sessions/events; event coverage must be shown. | `AVAILABLE_PUBLIC_DEMO` |
| `funnel.add_to_cart_rate` Add-to-cart rate | `sessions_with_add_to_cart / sessions_with_view_item` | `GA4` | Date × device × acquisition | Does not prove the same item was viewed and added unless item/session pathing is validated. | `AVAILABLE_PUBLIC_DEMO` |
| `funnel.checkout_start_rate` Checkout-start rate | `sessions_with_begin_checkout / sessions_with_add_to_cart` | `GA4` | Date × device × acquisition | Cross-domain/checkout tracking gaps can undercount checkout starts. | `AVAILABLE_PUBLIC_DEMO` |
| `funnel.purchase_conversion_rate` Purchase conversion rate | `sessions_with_valid_purchase / sessions` | `GA4` | Date × device × acquisition | Not the commerce order rate; duplicates must be removed by transaction ID and valid purchase rules. | `AVAILABLE_PUBLIC_DEMO` |
| `funnel.step_abandonment_rate` Step abandonment | `1 - next_step_sessions / current_step_sessions` | `GA4` | Consecutive named steps, date × device × acquisition | Can be negative if event-order/coverage anomalies exist; flag rather than clamp. | `AVAILABLE_PUBLIC_DEMO` |

### Acquisition KPIs

| ID / KPI | Formula | Source priority | Filters and grain | Caveats | Availability |
|---|---|---|---|---|---|
| `acquisition.users` Distinct users | Source-reported distinct users | `GA4` | Selected period × channel/source/medium/campaign/device | Not derived by summing daily rows; requires a period-scoped source report with identity/thresholding metadata. | `NOT_VERIFIED` |
| `acquisition.active_user_days` Active user-days | `SUM(source_reported_daily_active_users)` | `GA4` | Date × acquisition dimensions, then additive across dates | This is activity volume, not a distinct period-user count. | `AVAILABLE_PUBLIC_DEMO` |
| `acquisition.sessions` Sessions | `SUM(source-reported sessions)` only at additive export grain | `GA4` | Date × acquisition dimensions | Attribution is session-scoped; channel-group rule version must be known. | `AVAILABLE_PUBLIC_DEMO` |
| `acquisition.campaign_revenue` Campaign revenue | `SUM(attributed purchase/net revenue)` under the named public fixture attribution; live default is GA4 purchase revenue | `GA4`; commerce only in a separate governed model | Date × campaign | Attribution model, lookback, consent, and `(not set)` affect interpretation. | `AVAILABLE_PUBLIC_DEMO` |
| `acquisition.cpa` Cost per acquisition | `reliable ad_spend / comparable attributed acquisitions` | `ADS` with aligned conversion definition | Date × campaign | Public-demo inputs are reliable synthetic fixtures; live spend/conversion scope must align. | `AVAILABLE_PUBLIC_DEMO` |
| `acquisition.roas` Return on ad spend | `comparable attributed_revenue / reliable ad_spend` | `ADS`, or explicitly reconciled GA4 revenue | Date × campaign | Public-demo inputs are reliable synthetic fixtures. ROAS is not profit; live attribution/currency must align. | `AVAILABLE_PUBLIC_DEMO` |

### Customer KPIs

| ID / KPI | Formula | Source priority | Filters and grain | Caveats | Availability |
|---|---|---|---|---|---|
| `customer.new_share` New-customer share | `new customers / customers with known type` | `COMMERCE`; GA4 user type only as separate metric | Period | Available from invented public identities; live use requires documented lookback/safe identity. Unknown is reported separately. | `AVAILABLE_PUBLIC_DEMO` |
| `customer.returning_share` Returning-customer share | `returning customers / customers with known type` | `COMMERCE` | Period | Available from invented public identities; live use has identity/window caveats. | `AVAILABLE_PUBLIC_DEMO` |
| `customer.repeat_purchase_rate` Repeat-purchase rate | `customers with >=2 completed orders / customers with >=1 completed order` | `COMMERCE` | Customer cohort and stated observation window | Requires privacy-reviewed pseudonymous identity; right-censoring affects recent cohorts. | `CONDITIONAL` |
| `customer.retention_rate` Cohort retention | `cohort customers purchasing again in period N / original cohort customers` | `COMMERCE` | Acquisition cohort × period N | Only available with safe identity, sufficient observation window, and minimum group size. | `CONDITIONAL` |

### SEO KPIs

| ID / KPI | Formula | Source priority | Filters and grain | Caveats | Availability |
|---|---|---|---|---|---|
| `seo.clicks` Clicks | `SUM(clicks)` | `GSC` | Date × chosen query/page/country/device grain | API row limits and anonymized queries can make detailed sums differ from property totals. | `AVAILABLE_PUBLIC_DEMO` |
| `seo.impressions` Impressions | `SUM(impressions)` | `GSC` | Same as clicks | Same dimensional/top-row caveats. | `AVAILABLE_PUBLIC_DEMO` |
| `seo.ctr` CTR | `SUM(clicks) / SUM(impressions)` | `GSC` | Selected aggregation | Recalculate from sums; do not average row CTRs. | `AVAILABLE_PUBLIC_DEMO` |
| `seo.average_position` Average position | `SUM(position × impressions) / SUM(impressions)` | `GSC` | Selected aggregation | Impression-weighted; not a simple rank and not comparable when query mix changes materially. | `AVAILABLE_PUBLIC_DEMO` |
| `seo.branded_share` Branded query share | `branded clicks or impressions / classified clicks or impressions` | `GSC` + versioned classifier | Period | Public rule/queries are synthetic; live query omissions and classifier variants apply. | `AVAILABLE_PUBLIC_DEMO` |

### Data-quality and reconciliation KPIs

| ID / KPI | Formula | Source priority | Filters and grain | Caveats | Availability |
|---|---|---|---|---|---|
| `quality.event_coverage` Event coverage | `observed required event types / applicable required event types` | Measurement audit | Audit run × platform/scope | Public fixture contains all eleven target types; presence is not correctness or live coverage. | `AVAILABLE_PUBLIC_DEMO` |
| `quality.parameter_completeness` Required-parameter completeness | `valid applicable event rows / applicable event rows` for each event/parameter rule | Measurement audit | Audit run × event × parameter | Conditional parameters are included only when applicable; aggregated live reports may not expose all parameters. | `AVAILABLE_PUBLIC_DEMO` |
| `quality.duplicate_transaction_rate` Duplicate transaction rate | `duplicate valid purchase rows beyond first / valid purchase rows` | `GA4`, and commerce separately | Audit period × source | Same transaction ID in purchase and refund is not a duplicate purchase; empty IDs fail completeness. | `AVAILABLE_PUBLIC_DEMO` |
| `quality.unknown_product_rate` Unknown-product mapping rate | `rows or value with unmatched item_id / applicable rows or value` | Conformed product mapping | Period × source | Current public implementation is row-weighted; do not mix with unit/value variants. | `AVAILABLE_PUBLIC_DEMO` |
| `quality.data_freshness_hours` Data freshness | `observation_time - report_through_at` in hours | Connector metadata | Observation × connector | Public quality mart exposes Search Console staleness in days; source latency/timezone expectations differ. | `AVAILABLE_PUBLIC_DEMO` |
| `quality.transaction_variance` Salla–GA4 transaction variance | `(ga4_transactions - commerce_orders) / commerce_orders`; public SQL stores absolute magnitude for tolerance | `RECONCILED` | Aligned date/currency/status scope | Undefined when commerce orders are zero. Public mart does not preserve sign; live analysis should retain signed and absolute forms. | `AVAILABLE_PUBLIC_DEMO` |
| `quality.revenue_variance` Salla–GA4 revenue variance | `(ga4_purchase_revenue - commerce_net_revenue) / commerce_net_revenue`; public SQL stores absolute magnitude | `RECONCILED` | Aligned date/currency/net-revenue scope | Requires tax, shipping, discount, refund, timezone and currency alignment. | `AVAILABLE_PUBLIC_DEMO` |
| `quality.consent_state_coverage` Consent-state coverage | `events with observable valid consent state / events where consent state should be observable` | Measurement audit | Audit period × event/context | Public fixture includes a synthetic coverage defect. Live absence may mean not observable; this is not a compliance verdict. | `AVAILABLE_PUBLIC_DEMO` |

## Filter and presentation rules

1. Default date ranges are inclusive and shown with timezone.
2. The same filter context applies to numerator and denominator.
3. Currency conversion is out of scope unless an exchange-rate source and method are explicitly versioned; mixed-currency totals are unavailable.
4. A suppressed, unauthenticated, stale, or unsupported KPI displays a reason—not `0`.
5. The source name and report-through date remain visible near source-sensitive KPIs.
6. Comparisons show absolute and relative change; a relative change is unavailable when the comparison denominator is zero.
7. Synthetic data labels remain visible anywhere a public KPI value appears.

## Change control

Formula, scope, source precedence, or grain changes require a catalog version update, corresponding machine-readable change, dbt/API/frontend contract review, and regression tests. Presentation-only wording changes do not require a semantic version bump unless they alter interpretation.
