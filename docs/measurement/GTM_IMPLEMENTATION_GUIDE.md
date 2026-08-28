# Google Tag Manager Implementation Guide

## Status and safety boundary

This is a proposed implementation guide. The project has not published or changed a live GTM container, GA4 property, consent platform, storefront, or checkout. Perform future work in an authorized GTM workspace and test environment; use read-only inspection for the current portfolio audit.

## Recommended container design

Use one governed data layer and thin GTM configuration. Business logic—what happened, which items changed, and the confirmed transaction state—belongs in the storefront/commerce integration, not in brittle DOM scraping or Custom JavaScript variables.

Suggested naming:

| Asset | Pattern | Example |
|---|---|---|
| Tag | `GA4 - Event - <event_name>` | `GA4 - Event - purchase` |
| Trigger | `CE - <event_name>` | `CE - begin_checkout` |
| Data-layer variable | `DLV - ecommerce.<path>` | `DLV - ecommerce.currency` |
| Consent tag | `CMP - Consent defaults/update` | implementation-specific |
| Lookup/config | `LUT - <purpose>` | `LUT - environment measurement ID` |

Avoid putting secrets in GTM variables. Measurement IDs are identifiers, not secrets, but environment mappings still require controlled review.

## Data-layer contract

Initialize once before the container and never overwrite it:

```js
window.dataLayer = window.dataLayer || [];
```

For each ecommerce event, clear stale ecommerce state and then push one complete event object:

```js
window.dataLayer.push({ ecommerce: null });
window.dataLayer.push({
  event: "add_to_cart",
  ecommerce: {
    currency: "SAR",
    value: 49.00,
    items: [
      {
        item_id: "DEMO-SKU-001",
        item_name: "Synthetic Productivity License",
        item_category: "Productivity",
        price: 49.00,
        quantity: 1
      }
    ]
  }
});
```

The example is synthetic. Do not reuse demo identifiers in live reporting. Do not push PII, payment data, credentials, raw errors, or private coupon/customer attributes.

## Build sequence

1. **Inventory first:** export the current container version, GA4 web stream settings, cross-domain configuration, custom dimensions, consent platform behavior, and existing vendor/native ecommerce tags. Do not create a second purchase tag until duplicate risk is resolved.
2. **Define environments:** isolate development/preview from production measurement IDs or use governed GTM Environments. Exclude internal/test traffic through documented GA4 filters where appropriate.
3. **Implement consent initialization:** the CMP/consent template establishes defaults before dependent tags and sends updates on the same page where the choice occurs.
4. **Create variables:** data-layer variables for common event and item fields; avoid DOM variables for transaction value/ID.
5. **Create custom-event triggers:** exact match on the eleven event names in the event specification.
6. **Create GA4 event tags:** map event name and ecommerce object/parameters according to the current GTM Google tag interface. Use one firing route per business event.
7. **Set consent requirements:** use built-in consent checks for Google tags and explicit Additional Consent Checks for other tags. Review every custom/community template.
8. **Prevent duplicates:** remove or suppress overlapping platform-native, hard-coded `gtag`, plugin, and GTM collection paths only after evidence identifies the authoritative route.
9. **Validate:** Preview/Tag Assistant, browser network inspection, GA4 DebugView, processed reporting, and commerce reconciliation.
10. **Publish safely:** peer review the workspace diff, name/version it, record tests and rollback, publish only after approval.

## Tag mapping

| Data-layer event | GTM trigger | GA4 event name | Essential mapped data |
|---|---|---|---|
| `view_item_list` | exact custom event | `view_item_list` | `items`, list context, optional `currency/value` |
| `select_item` | exact custom event | `select_item` | selected `items`, list context |
| `view_item` | exact custom event | `view_item` | `items`, optional `currency/value` |
| `add_to_cart` | exact custom event | `add_to_cart` | `items`, `currency/value` when used |
| `remove_from_cart` | exact custom event | `remove_from_cart` | removed delta `items`, `currency/value` when used |
| `view_cart` | exact custom event | `view_cart` | current cart `items`, `currency/value` |
| `begin_checkout` | exact custom event | `begin_checkout` | current cart `items`, `currency/value`, optional coupon |
| `add_shipping_info` | exact custom event when applicable | `add_shipping_info` | `items`, optional safe `shipping_tier` |
| `add_payment_info` | exact custom event | `add_payment_info` | `items`, optional safe `payment_type` |
| `purchase` | exact confirmed-order event | `purchase` | `transaction_id`, `currency`, `value`, `items`, optional tax/shipping/coupon |
| `refund` | governed server/offline or trusted event route | `refund` | original `transaction_id`, refunded `items`, optional `currency/value` |

## Consent configuration

- Decide basic versus advanced Consent Mode with the controller's privacy/legal stakeholders; Google's modeling benefits do not determine legal permissibility.
- Set region-appropriate defaults before any measurement tag can act. For an EEA-oriented conservative baseline, relevant optional storage/use states start denied until a valid choice is received.
- Map CMP purposes to `analytics_storage`, `ad_storage`, `ad_user_data`, `ad_personalization`, and other applicable states. Do not treat one analytics checkbox as consent to all advertising purposes.
- Fire consent updates on the page where the choice occurs and before navigation.
- Make withdrawal/reopen controls discoverable and test that denial/withdrawal changes tag behavior.
- `security_storage` supports security-related storage and should not be casually tied to marketing consent.

See [CONSENT_AND_EEA_NOTES.md](CONSENT_AND_EEA_NOTES.md) for the governance boundary.

## Duplicate prevention

Common duplicate sources include:

- Salla/platform-native GA4 integration plus GTM purchase tag;
- hard-coded `gtag` plus GTM Google tag;
- thank-you page reload or history navigation;
- client event plus server/Measurement Protocol event;
- multiple GTM containers or repeated container initialization;
- trigger matching both custom event and page view.

Controls:

- document one owner/firing path per event;
- fire `purchase` from a confirmed state with a stable transaction ID;
- inspect Tag Assistant's event timeline and network requests;
- retain downstream duplicate detection even if GA4 deduplicates a repeated transaction ID;
- never rely solely on browser storage for financial-event deduplication.

## Validation checklist

### Consent states

- Before choice: expected default is established before dependent tags.
- Accept selected purposes: only corresponding states become granted.
- Reject: optional tags follow the approved denied behavior.
- Granular selection: analytics and advertising choices remain independent.
- Withdraw: future behavior changes immediately and choice UI remains available.
- Region/language: banner and default behavior are consistent on EN/AR and applicable regional paths.

### Events and parameters

- Each user/business action produces exactly one intended data-layer event.
- Event object is cleared between pushes; no stale items or coupon values.
- No event precedes its actual business confirmation.
- Item array, identifiers, price, quantity, currency, and value pass the specification.
- Purchase ID is stable on reload and absent from unintended events.
- No PII/payment data appears in data layer, Tag Assistant, requests, or GA4 DebugView.

### Reporting

- DebugView shows event- and item-scoped parameters.
- Standard reports/Data API are checked after processing latency.
- Required custom definitions exist only for justified custom parameters.
- Date/timezone/currency/status scope aligns before Salla–GA4 reconciliation.

## Rollout and rollback

Use a small, reviewed GTM workspace. Record the container version, approver, test evidence, intended change, and rollback version. Start with discovery and product/cart events before purchase only if doing so does not create mixed production semantics; the final publication must keep one coherent contract. Monitor purchase completeness, duplicates, parameter errors, consent behavior, and source variance immediately after release.

Rollback means republishing the last known-good GTM version and, where necessary, reverting the storefront data-layer change. It does not mean deleting evidence or rewriting historic analytics.

## Official references

- [Google: The data layer](https://developers.google.com/tag-platform/tag-manager/datalayer)
- [Google: Set up ecommerce events](https://support.google.com/analytics/answer/12200568)
- [Google: Validate ecommerce](https://developers.google.com/analytics/devguides/collection/ga4/validate-ecommerce)
- [Google: Consent Mode overview](https://developers.google.com/tag-platform/security/concepts/consent-mode)
- [Google: Troubleshoot consent with Tag Assistant](https://developers.google.com/tag-platform/security/guides/consent-debugging)

