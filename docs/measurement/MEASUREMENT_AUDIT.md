# Measurement Audit

- Audit state: **public fixture audit implemented; limited passive storefront observation completed; live measurement validation not completed**
- Initial record date: 2026-08-28
- Scope: repository measurement contract, deterministic event aggregates, observed connector reachability, and a non-transactional passive public-page inspection
- Live storefront changes: none
- Live checkout/order activity: none

## Executive conclusion

The repository defines the required eleven-event GA4 ecommerce contract, parameter rules, source-reconciliation rules, GTM implementation approach, and consent-aware test scenarios. The deterministic fixture includes all eleven event names and ten parameter/consent coverage fields; dbt has a coverage assertion and quality aggregation. That proves the public audit module can represent the contract, not that the live store implements it.

The execution record states that GA4 account discovery was reachable but no values were persisted publicly. A passive DOM inspection covered an Arabic storefront home page and a representative product page without login, cart, checkout, order, form submission or configuration change. It observed two GTM script references per page, but no data-layer object, inline consent default/update, or visible consent text in the captured DOM. This is a point-in-time observation, not proof that analytics/consent behavior is absent; conditional, post-interaction, server-side or otherwise non-DOM behavior remains unobserved.

No evidence proves live event coverage, parameter completeness, duplicate rate, runtime consent behavior, GTM tag configuration, or aligned Salla–GA4 variance. Those live controls remain `NOT_RUN` or `NOT_OBSERVABLE`.

## Evidence scale

| Status | Meaning |
|---|---|
| `PASS` | The named assertion passed against identified evidence and scope. |
| `FAIL` | The assertion failed; finding/evidence is recorded. |
| `NOT_RUN` | Required procedure has not been executed. |
| `NOT_OBSERVABLE` | Available source/evidence cannot expose the assertion. |
| `NOT_APPLICABLE` | The business flow does not contain the step, with supporting evidence. |

`NOT_RUN`, `NOT_OBSERVABLE`, and `NOT_APPLICABLE` are not passes.

## Current control matrix

### Public deterministic fixture

| Control | Evidence | Status | Scope caveat |
|---|---|---|---|
| Eleven event names represented | `data/public-demo/events.csv`; dbt event-coverage assertion | `PASS` (track-reported; final rerun pending) | Synthetic aggregate coverage only |
| Ten parameter/consent coverage fields represented | Event CSV/staging/intermediate quality model | `PASS` (track-reported; final rerun pending) | Ratios, not raw payload validation |
| Intentional missing parameter detected | `DQ-002` and `mart_data_quality` | `PASS` (track-reported; final rerun pending) | Synthetic defect |
| Duplicate transaction detected | `DQ-001` and quality mart/API | `PASS` (track-reported; final rerun pending) | Synthetic defect |
| Source variance detected | `DQ-005` and reconciliation mart | `PASS` (track-reported; final rerun pending) | Synthetic sources and governed tolerance |
| Consent-coverage gap detected | `DQ-006`, event coverage field and `consent_state_coverage` quality check | `PASS` (track-reported; final rerun pending) | Technical observability metric, not compliance score |

### Live/storefront measurement

| Control | Expected evidence | Initial status | Honest gap |
|---|---|---|---|
| Required event coverage | GA4 export/DebugView or privacy-safe data-layer capture for all applicable events | `NOT_RUN` | Account discovery does not prove event presence. |
| Required parameter completeness | Event/item parameter-level evidence | `NOT_RUN` | Aggregate reports may not expose all parameters. |
| Purchase transaction-ID uniqueness | Event-level purchase audit | `NOT_RUN` | No live event records retained. |
| Currency validity/consistency | Event-level and commerce export | `NOT_RUN` | Property/store currency settings not evidenced here. |
| Value-to-item reconciliation | Event/item arrays and tolerance result | `NOT_RUN` | No live payload evidence. |
| Product mapping | Item IDs plus governed product dimension | `NOT_RUN` | No live catalog/event comparison persisted. |
| Event-order anomalies | Session/path-level privacy-safe evidence | `NOT_RUN` | No session event sequence evidence. |
| Data freshness | Extract/report-through metadata | `NOT_RUN` | Reachability is not freshness. |
| Salla–GA4 transaction variance | Aligned source extracts | `NOT_RUN` | Date/timezone/status scope not aligned. |
| Salla–GA4 revenue variance | Aligned source extracts and component mapping | `NOT_RUN` | Revenue scope/currency/refund mapping not evidenced. |
| Consent defaults/updates | Tag Assistant/network/storage evidence for scenarios | `NOT_RUN` | Consent state not inspected. |
| Prohibited data absence in analytics payloads | Privacy-safe request/data-layer inspection | `NOT_OBSERVABLE` | Passive DOM capture had privacy review `PASS`, but no event payload/data layer was observed to inspect. |

## Required event register

| Event | Applicability hypothesis | Validation state | Evidence needed |
|---|---|---|---|
| `view_item_list` | Expected for category/search/recommendation lists | `NOT_RUN` | List impression data-layer/GA4 evidence |
| `select_item` | Expected when an item is opened from a list | `NOT_RUN` | Selection event with list/item context |
| `view_item` | Expected on product detail | `NOT_RUN` | Product detail event/item payload |
| `add_to_cart` | Expected if cart exists | `NOT_RUN` | Confirmed state-change event |
| `remove_from_cart` | Expected if cart item can be removed | `NOT_RUN` | Confirmed state-change event |
| `view_cart` | Expected if cart view exists | `NOT_RUN` | Cart snapshot event |
| `begin_checkout` | Expected | `NOT_RUN` | Actual checkout-entry event; no live checkout initiated for audit |
| `add_shipping_info` | Potentially not applicable for digital goods | `NOT_RUN` | Flow evidence establishing a real delivery step or justified N/A |
| `add_payment_info` | Expected if payment choice exists | `NOT_RUN` | Safe payment-category event; no payment details |
| `purchase` | Expected | `NOT_RUN` | Approved non-live/fixture or existing privacy-safe evidence only |
| `refund` | Expected for reported refunds; usually server/offline | `NOT_RUN` | Governed refund evidence linked to original transaction |

## Passive storefront observation

Evidence: `artifacts/evidence/passive-storefront-audit.json`, captured 2026-08-28 in Europe/Berlin time; privacy review `PASS`.

| Page class | Observed | Not observed in captured DOM |
|---|---|---|
| Arabic storefront home (`lang=ar`, `dir=rtl`) | 2 GTM script references | direct GA script, Clarity script, data layer, inline consent default/update, visible cookie/consent text |
| Representative public product page (`dir=rtl`) | 2 GTM script references, canonical metadata, product price metadata, Organization/WebPage/Product/BreadcrumbList schema types | data layer, inline consent default, visible cookie/consent text |

The inspection did not prove tags fired, requests were sent, consent was valid/invalid, or events were present/absent. A future authorized runtime audit may inspect public rendered pages, data layer, tag/network behavior, cookie/storage changes and consent UI. It must not log into customer/admin areas, add to a live cart, begin live checkout, submit an order, alter consent/tag/store settings, or capture customer/merchant-private data merely to create evidence.

Because a full purchase/refund path cannot be generated safely on the live store for this portfolio, validate those events through an approved test/staging environment, deterministic fixture, existing privacy-safe debug evidence, or historical aggregate reconciliation. Do not claim live end-to-end validation without such evidence.

## Audit procedure for the next authorized run

1. Record URL scope, UTC/local time, browser profile, locale, consent starting state, GTM/GA4 identifiers in redacted form, and evidence owner.
2. Extend the existing passive observation to approved runtime network/storage/interaction-free states only as permitted.
3. Run the consent scenarios in [CONSENT_AND_EEA_NOTES.md](CONSENT_AND_EEA_NOTES.md) without transactional actions.
4. Import approved GA4 aggregates/parameter audit output and Salla aggregate reports to ignored private storage.
5. Validate each event/rule from [GA4_EVENT_SPEC.md](GA4_EVENT_SPEC.md).
6. Align date, timezone, currency, order status, value components, duplicates, and refunds before variance.
7. Record evidence hash/path, result, affected rows/denominator, severity, KPI impact, owner, and remediation recommendation.
8. Redact or aggregate findings before any public publication; never copy exact live metrics.

## Findings

| ID | Severity | Observation | Classification | Effect | Required action |
|---|---|---|---|---|---|
| `MA-001` | High | No event-level or Tag Assistant evidence is recorded for the live implementation. | Evidence gap | Live event/parameter quality cannot be assessed. | Conduct an authorized privacy-safe audit or import approved audit evidence. |
| `MA-002` | High | Consent default/update and tag behavior have not been observed. | Evidence gap | EEA/German consent-aware behavior cannot be assessed. | Execute the consent scenario matrix with privacy/legal-approved expectations. |
| `MA-003` | Medium | Salla and GA4 sources have not been aligned into a comparable private extract. | Evidence gap | Transaction/revenue variance is unavailable. | Align scope in ignored local storage and run reconciliation tests. |

These findings describe missing evidence, not proven defects in the live storefront.

## Implemented contract vs future recommendation

| Implemented/documented in repository | Future/live recommendation |
|---|---|
| Eleven-event specification and validation rules | Deploy only approved event/data-layer changes |
| KPI and source-precedence definitions | Configure/report against authenticated GA4 and commerce sources |
| GTM workspace/tag/trigger design guidance | Change live GTM container after peer/privacy review |
| Consent-aware scenario and engineering checklist | Controller/legal decision on CMP, lawful basis and Consent Mode |
| Public fixture audit plus limited passive DOM evidence with explicit caveats | Capture approved runtime/staging evidence and resolve live findings |

## Sign-off rule

Do not mark the live measurement audit passed until all applicable critical/high controls have identified evidence, failed controls have owned remediation, not-applicable events have flow evidence, and the privacy reviewer approves the evidence set for its intended audience.
