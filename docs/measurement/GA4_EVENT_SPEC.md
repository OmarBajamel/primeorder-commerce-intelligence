# GA4 E-commerce Event Specification

- Specification version: `1.0.0`
- Scope: web commerce measurement for digital products
- Implementation state: target contract; no live-store deployment is claimed

Google classifies ecommerce data into event and item scopes. The official references are the [recommended events reference](https://developers.google.com/analytics/devguides/collection/ga4/reference/events), [ecommerce implementation guide](https://developers.google.com/analytics/devguides/collection/ga4/ecommerce), and [ecommerce validation guide](https://developers.google.com/analytics/devguides/collection/ga4/validate-ecommerce). This project deliberately applies several stricter requirements so reconciliation and auditing remain reliable.

## Common event envelope

| Field | Scope | Project rule | Validation |
|---|---|---|---|
| `event` | data layer | Exact lowercase recommended event name | Accepted-value check |
| `currency` | event | ISO 4217 uppercase; required whenever `value` is present and always on `purchase`/valued `refund` | `^[A-Z]{3}$`; one currency per event |
| `value` | event | Numeric event merchandise value; required for project purchase and valued refund | Within tolerance of item total; no tax/shipping unless event definition says so |
| `items` | event | Non-empty array for every applicable commerce event in this specification | Array bounds/type; no stale prior-event items |
| `transaction_id` | event | Required, non-empty, stable and unique for `purchase`; original transaction reference for `refund` | Duplicate/missing/orphan checks |
| `coupon` | event/item | Optional; event and item scope have independent meaning | Length/allowed-character policy; no PII/private public codes |
| `shipping`, `tax` | event | Purchase/refund only where applicable | Numeric, non-negative; excluded from merchandise `value` convention |
| `payment_type` | event | Optional on `add_payment_info`; category only | Accepted safe categories; never card/account data |
| `shipping_tier` | event | Optional on `add_shipping_info` | Governed non-sensitive label |

## Common item contract

| Field | Required | Rule |
|---|---:|---|
| `item_id` | project: yes | Stable catalog identifier. Google requires at least `item_id` or `item_name`; this project expects both when safely available. |
| `item_name` | project: yes | Public product name in demo; live use must pass data classification. |
| `item_category` | project: yes | First governed category level; `item_category2`–`item_category5` optional. |
| `price` | project: yes | Numeric per-unit merchandise price after item discount according to the documented convention. |
| `quantity` | project: yes | Positive number for additions/purchases; removed quantity for `remove_from_cart`; refunded quantity for item-level `refund`. |
| `discount` | optional | Per-unit discount; do not also subtract it from `price` under a contradictory convention. |
| `item_brand` | recommended | Publisher/brand label when governed. |
| `index` | recommended for lists | Zero-based or one-based convention must be consistent and documented. |
| `item_list_id`, `item_list_name` | contextual | Carry list attribution from list view/selection where possible. Item-scope values take precedence for the affected item in GA4. |
| `item_variant` | optional | Governed product variant; do not place free text or personal data here. |
| `affiliation` | optional | Store/fulfilment affiliation, not customer or supplier-confidential detail. |
| `promotion_id`, `promotion_name` | optional | Used only when a real promotion context exists; keep through subsequent events when attribution is intended. |
| `creative_name`, `creative_slot` | optional | Governed promotion creative metadata. |

## Event matrix

`R` = project-required, `C` = conditionally required, `O` = optional/recommended, `—` = not applicable.

| Event | Trigger | `items` | `currency` | `value` | Event-specific fields | Main audit assertions |
|---|---|:---:|:---:|:---:|---|---|
| `view_item_list` | Meaningful product list becomes visible | R | C | O | `item_list_id` or `item_list_name` O; item `index` O | List not empty; IDs/names present; no duplicate render storm |
| `select_item` | User selects an item from a list | R | C | O | list context O | Exactly selected item(s); list attribution consistent with preceding view when observable |
| `view_item` | Product detail becomes active | R | C | O | — | Active product matches item payload; one per routed view |
| `add_to_cart` | Confirmed cart-state addition | R | C | O | event/item `coupon` O | Quantity is delta added; not fired on rejected click; value matches included items |
| `remove_from_cart` | Confirmed cart-state removal | R | C | O | — | Quantity is delta removed; item existed in cart where observable |
| `view_cart` | Cart view becomes active | R | C | O | event `coupon` O | Payload reflects current cart once, not stale previous event |
| `begin_checkout` | Actual checkout flow starts | R | C | O | event `coupon` O | Cart snapshot is current; not fired merely on cart view |
| `add_shipping_info` | Delivery/shipping selection accepted | R when applicable | C | O | `shipping_tier` O | Explicit `NOT_APPLICABLE` allowed for a no-shipping digital flow |
| `add_payment_info` | Non-sensitive payment category accepted | R | C | O | `payment_type` O | No card/account/PII; accepted cart snapshot |
| `purchase` | Completed order confirmation | R | R | R | `transaction_id` R; `tax`, `shipping`, `coupon` O | Unique non-empty transaction ID; one firing; valid currency; item/value reconciliation |
| `refund` | Confirmed full/partial refund | Project R for item analysis | C for valued refund | C | `transaction_id` R; `tax`, `shipping`, `coupon` O | Original transaction exists when dataset supports it; partial quantities/values do not exceed purchased amount |

## Value convention

For item-based events:

```text
expected_value = sum(item.price * item.quantity)
```

Project tolerance is a small currency-rounding tolerance configured by the audit, never a percentage large enough to hide allocation errors. `purchase.value` represents the item merchandise total under this convention. `tax` and `shipping` are separate parameters and are not included in `value`. If the commerce source uses a different revenue definition, reconciliation maps the components explicitly rather than changing the GA4 payload silently.

## Event-specific notes

### List discovery: `view_item_list` and `select_item`

- Use a stable `item_list_id`/`item_list_name` for category, search, recommended, and campaign lists.
- Send only items actually rendered/observed under the chosen visibility rule; document pagination and infinite scroll.
- Preserve item `index` and list context from impression to selection where feasible.
- If promotion attribution is used, at least one governed promotion identifier/name must propagate according to the implementation design.

### Product and cart: `view_item`, `add_to_cart`, `remove_from_cart`, `view_cart`

- A click is not an addition/removal until the commerce state confirms success.
- For quantity changes, send the changed quantity, not necessarily the full cart quantity, on add/remove.
- `view_cart` contains the current cart snapshot. Clear the previous ecommerce object before each GTM ecommerce push to prevent stale arrays.

### Checkout: `begin_checkout`, `add_shipping_info`, `add_payment_info`

- `begin_checkout` marks entry to the actual checkout, not merely selecting “cart.”
- A pure digital-goods experience can mark `add_shipping_info` not applicable. If delivery method, locale, or fulfilment selection genuinely exists, use a non-sensitive governed `shipping_tier`.
- `payment_type` is a safe category such as a governed wallet/card/bank-transfer label. Never send card number, bank data, token, holder name, failure message, or processor payload.

### `purchase`

- Fire on confirmed completed-order state, once per transaction, after the result is known.
- Do not fire on checkout submit, payment initiation, page reload, or merely reaching a thank-you URL without server state.
- `transaction_id` must be stable across reloads/retries and unique across purchases. The live identifier handling requires privacy review; the public demo uses invented identifiers.
- Browser/client deduplication is only a guard. Source-side validation and downstream duplicate detection remain necessary.
- A transaction ID sent twice may be deduplicated by GA4, but the audit still flags repeated sends because they indicate implementation risk.

### `refund`

- Trigger only after the commerce system confirms the refund.
- Reference the original `transaction_id`.
- Include `items` with `item_id` and refunded `quantity` for item-level full/partial refund measurement.
- A server-side or governed offline implementation must keep Measurement Protocol secrets off the browser and must not duplicate a vendor-native refund event.

## Data-layer example

This is a **synthetic contract example**, not code deployed to PrimeOrder:

```js
window.dataLayer = window.dataLayer || [];

window.dataLayer.push({ ecommerce: null });
window.dataLayer.push({
  event: "purchase",
  ecommerce: {
    transaction_id: "DEMO-TXN-000123",
    currency: "SAR",
    value: 149.00,
    tax: 0,
    shipping: 0,
    items: [
      {
        item_id: "DEMO-SKU-AI-01",
        item_name: "Synthetic AI Toolkit License",
        item_brand: "Demo Publisher",
        item_category: "AI",
        price: 149.00,
        quantity: 1
      }
    ]
  }
});
```

No email, phone number, customer name, address, account ID, payment detail, free-form checkout text, or other personal data belongs in this object.

## Validation rules

| Rule ID | Assertion | Default severity |
|---|---|---|
| `EVT-001` | Event name is applicable and in the specification | Medium |
| `EVT-002` | Required event/item parameters exist and have valid types | High |
| `EVT-003` | `currency` is valid and present when required | High |
| `EVT-004` | `value` matches item total within configured rounding tolerance | High |
| `EVT-005` | Purchase transaction ID is non-empty and not duplicated | Critical |
| `EVT-006` | Item ID maps to the governed product dimension | Medium/High by value share |
| `EVT-007` | Quantity/price/value are within valid numeric domains | High |
| `EVT-008` | Event order is plausible within observable session/path | Medium |
| `EVT-009` | Event/report freshness meets source expectation | Medium |
| `EVT-010` | Consent default/update and tag behavior are consistent where observable | High |
| `EVT-011` | No prohibited personal/payment data is present | Critical |
| `EVT-012` | Refund references a purchase and does not exceed it where comparable | High |

## Versioning

A trigger, parameter meaning, value convention, category taxonomy, transaction-ID policy, or consent behavior change requires a new specification version and coordinated updates to storefront data layer, GTM, GA4 reporting, dbt models, tests, and documentation.

