"""Generate the deterministic, privacy-safe PrimeOrder public demo fixtures.

The values are invented from a fixed seed and do not derive from any merchant.
Intentional defects are described in ``metadata.json`` and represented as data;
they are not allowed to break structural warehouse invariants.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import shutil
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


SEED = 20250301
START_DATE = date(2025, 1, 1)
DAY_COUNT = 365
DISCLOSURE = "Synthetic portfolio demo data — no real customer or revenue information"
ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIR = ROOT / "data" / "public-demo"
SEED_DIR = ROOT / "analytics" / "seeds"
API_DIR = PUBLIC_DIR / "api"
DASHBOARD_PATH = ROOT / "apps" / "web" / "public" / "data" / "dashboard.json"

PRODUCTS = [
    ("P001", "Office Pro Annual", "أوفيس برو السنوي", "Productivity", "Nimbus", 299.0, 94.0),
    ("P002", "Focus Notes Plus", "فوكس نوتس بلس", "Productivity", "Nimbus", 89.0, 24.0),
    ("P003", "Arabic Learning Lab", "مختبر التعلم العربي", "Education", "Madar", 179.0, 49.0),
    ("P004", "STEM Academy Pass", "اشتراك أكاديمية ستيم", "Education", "Madar", 249.0, 71.0),
    ("P005", "Canvas Studio", "استوديو كانفس", "Design", "Rimal", 219.0, 67.0),
    ("P006", "Creator Asset Cloud", "سحابة أصول المبدعين", "Design", "Rimal", 139.0, 35.0),
    ("P007", "AI Writing Assistant", "مساعد الكتابة الذكي", "AI", "Sahab", 189.0, 55.0),
    ("P008", "AI Research Workspace", "مساحة البحث الذكية", "AI", "Sahab", 329.0, 121.0),
    ("P009", "Secure Vault Family", "الخزنة الآمنة للعائلة", "Security", "Himaya", 159.0, 43.0),
    ("P010", "Endpoint Guard Pro", "حماية الأجهزة برو", "Security", "Himaya", 279.0, 83.0),
    ("P011", "Cloud Backup 2TB", "نسخ سحابي ٢ تيرابايت", "Cloud", "Afaq", 199.0, 61.0),
    ("P012", "Team Cloud Workspace", "مساحة عمل سحابية", "Cloud", "Afaq", 359.0, 137.0),
]

CHANNELS = [
    ("Organic Search", "google", "organic", "Always-on SEO"),
    ("Paid Search", "google", "cpc", "KSA Growth"),
    ("Direct", "direct", "none", "Unassigned"),
    ("Paid Social", "instagram", "paid_social", "Creator Offers"),
    ("Email", "newsletter", "email", "Lifecycle"),
    ("Affiliates", "partners", "affiliate", "Partner Network"),
]
DEVICES = ["mobile", "desktop", "tablet"]
CITIES = ["Riyadh", "Jeddah", "Dammam", "Makkah", "Madinah", "Khobar"]
PAYMENTS = ["mada", "apple_pay", "visa", "mastercard", "stc_pay"]

ANOMALIES = [
    {
        "id": "DQ-001",
        "kind": "duplicate_transaction_id",
        "date": "2025-06-15",
        "severity": "high",
        "expected_detection": "mart_data_quality duplicate_transaction_rate > 0",
        "description": "Two synthetic orders share a GA4 tracking transaction ID; order IDs remain unique.",
    },
    {
        "id": "DQ-002",
        "kind": "missing_event_parameters",
        "date": "2025-05-08",
        "severity": "medium",
        "expected_detection": "event parameter completeness below 100 percent",
        "description": "A purchase aggregate has missing currency and item_id parameters.",
    },
    {
        "id": "DQ-003",
        "kind": "stale_source",
        "date": "2025-12-21",
        "severity": "medium",
        "expected_detection": "Search Console freshness exceeds seven days at dataset end",
        "description": "Search Console fixtures intentionally stop eleven days before commerce data.",
    },
    {
        "id": "DQ-004",
        "kind": "unmapped_product",
        "date": "2025-07-11",
        "severity": "high",
        "expected_detection": "unknown_product_mapping_rate > 0",
        "description": "One order item uses synthetic product key UNMAPPED-001.",
    },
    {
        "id": "DQ-005",
        "kind": "tracking_variance",
        "date": "2025-09-20",
        "severity": "medium",
        "expected_detection": "Salla versus GA4 purchase variance exceeds tolerance",
        "description": "GA4 purchases are intentionally under-reported during a five-day window.",
    },
    {
        "id": "DQ-006",
        "kind": "consent_coverage",
        "date": "2025-11-03",
        "severity": "low",
        "expected_detection": "consent_state_coverage below 95 percent",
        "description": "Consent state is absent for a small synthetic event cohort.",
    },
]


def iso_day(offset: int) -> date:
    return START_DATE + timedelta(days=offset)


def seasonal_multiplier(day: date) -> float:
    value = 1.0
    if date(2025, 3, 1) <= day <= date(2025, 3, 29):
        value *= 1.32
    if date(2025, 8, 10) <= day <= date(2025, 9, 5):
        value *= 1.17
    if date(2025, 9, 20) <= day <= date(2025, 9, 25):
        value *= 1.41
    if day.weekday() in (3, 4):
        value *= 1.09
    return value


def write_csv(path: Path, rows: Iterable[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def round2(value: float) -> float:
    return round(value + 1e-9, 2)


def generate() -> Dict[str, List[Dict[str, Any]]]:
    rng = random.Random(SEED)
    products = [
        {
            "product_id": p[0], "product_name_en": p[1], "product_name_ar": p[2],
            "category": p[3], "brand": p[4], "list_price_sar": p[5], "unit_cost_sar": p[6],
            "is_active": True,
        }
        for p in PRODUCTS
    ]
    commerce: List[Dict[str, Any]] = []
    orders: List[Dict[str, Any]] = []
    order_items: List[Dict[str, Any]] = []
    ga4_daily: List[Dict[str, Any]] = []
    ga4_product_daily: List[Dict[str, Any]] = []
    google_ads_daily: List[Dict[str, Any]] = []
    events: List[Dict[str, Any]] = []
    search: List[Dict[str, Any]] = []
    merchant: List[Dict[str, Any]] = []
    clarity: List[Dict[str, Any]] = []
    prior_tracking_id = ""

    for day_offset in range(DAY_COUNT):
        day = iso_day(day_offset)
        multiplier = seasonal_multiplier(day)
        for segment in range(3):
            channel, source, medium, campaign = CHANNELS[(day_offset + segment * 2) % len(CHANNELS)]
            device = DEVICES[(day_offset + segment) % len(DEVICES)]
            city = CITIES[(day_offset * 2 + segment) % len(CITIES)]
            payment = PAYMENTS[(day_offset + segment * 3) % len(PAYMENTS)]
            sessions = max(25, int((72 + rng.randint(0, 96)) * multiplier))
            users = int(sessions * rng.uniform(0.72, 0.91))
            product_views = int(sessions * rng.uniform(0.64, 0.83))
            add_to_carts = int(product_views * rng.uniform(0.18, 0.30))
            checkouts = int(add_to_carts * rng.uniform(0.52, 0.72))
            purchases = max(1, int(checkouts * rng.uniform(0.56, 0.78)))
            gross = discount = refunds = cost = 0.0
            for purchase_index in range(purchases):
                product = PRODUCTS[(day_offset * 5 + segment * 3 + purchase_index) % len(PRODUCTS)]
                quantity = 2 if rng.random() < 0.08 else 1
                line_gross = round2(product[5] * quantity)
                line_discount = round2(line_gross * (0.1 if rng.random() < 0.23 else 0.0))
                line_revenue = round2(line_gross - line_discount)
                order_id = f"SYN-{day.strftime('%Y%m%d')}-{segment}-{purchase_index:02d}"
                tracking_id = f"TX-{day.strftime('%y%m%d')}-{segment}-{purchase_index:02d}"
                if day == date(2025, 6, 15) and segment == 0 and purchase_index == 1:
                    tracking_id = prior_tracking_id
                product_id = "UNMAPPED-001" if (
                    day == date(2025, 7, 11) and segment == 1 and purchase_index == 0
                ) else product[0]
                is_refunded = rng.random() < 0.035
                refund_value = line_revenue if is_refunded else 0.0
                anonymous_customer_id = "CUST-{:05d}".format(
                    (day_offset * 11 + segment * 101 + purchase_index * 17) % 2500
                )
                orders.append({
                    "order_id": order_id, "tracking_transaction_id": tracking_id,
                    "order_date": day.isoformat(), "anonymous_customer_id": anonymous_customer_id,
                    "customer_first_purchase_date": "", "customer_type": "", "channel": channel, "source": source,
                    "medium": medium, "campaign": campaign, "device": device, "city": city,
                    "payment_method": payment, "coupon_group": "campaign" if line_discount else "none",
                    "order_status": "refunded" if is_refunded else "completed",
                    "gross_revenue_sar": line_gross, "discount_sar": line_discount,
                    "refund_sar": refund_value, "net_revenue_sar": round2(line_revenue - refund_value),
                })
                order_items.append({
                    "order_id": order_id, "order_date": day.isoformat(), "product_id": product_id,
                    "quantity": quantity, "item_revenue_sar": line_gross,
                    "item_cost_sar": round2(product[6] * quantity), "discount_sar": line_discount,
                })
                gross += line_gross
                discount += line_discount
                refunds += refund_value
                cost += product[6] * quantity
                prior_tracking_id = tracking_id
            ad_spend = round2(sessions * rng.uniform(0.7, 1.45)) if channel in {"Paid Search", "Paid Social"} else 0.0
            commerce_row = {
                "date": day.isoformat(), "channel": channel, "source": source, "medium": medium,
                "campaign": campaign, "device": device, "city": city, "payment_method": payment,
                "purchases": purchases,
                "units_sold": sum(i["quantity"] for i in order_items[-purchases:]),
                "gross_revenue_sar": round2(gross), "discount_sar": round2(discount),
                "refund_sar": round2(refunds), "net_revenue_sar": round2(gross - discount - refunds),
                "cost_sar": round2(cost),
            }
            commerce.append(commerce_row)
            ga4_factor = 0.68 if date(2025, 9, 20) <= day <= date(2025, 9, 24) else 0.96
            ga4_purchases = int(round(purchases * ga4_factor))
            ga4_revenue = round2((gross - discount - refunds) * ga4_factor)
            consent_coverage = 0.82 if day == date(2025, 11, 3) else rng.uniform(0.96, 0.995)
            ga4_sessions = int(sessions * 0.98)
            ga4_users = int(users * 0.98)
            ga4_views = int(product_views * 0.97)
            ga4_carts = int(add_to_carts * 0.96)
            ga4_checkouts = int(checkouts * 0.95)
            ga4_daily.append({
                "date": day.isoformat(), "channel": channel, "source": source, "medium": medium,
                "campaign": campaign, "device": device, "sessions": ga4_sessions,
                "users": ga4_users, "product_views": ga4_views,
                "add_to_carts": ga4_carts, "begin_checkouts": ga4_checkouts,
                "purchases": ga4_purchases, "purchase_revenue_sar": ga4_revenue,
                "consent_state_coverage": round(consent_coverage, 4),
            })
            if channel in {"Paid Search", "Paid Social"}:
                google_ads_daily.append({
                    "date": day.isoformat(), "channel": channel, "source": source,
                    "medium": medium, "campaign": campaign,
                    "clicks": int(ga4_sessions * 0.18), "conversions": ga4_purchases,
                    "conversion_value_sar": ga4_revenue, "ad_spend_sar": ad_spend,
                })
            # Product-scoped GA4 behavior is generated from an exogenous preference
            # profile, never from observed order/item shares. Each measure preserves
            # the parent GA4 row total at a mutually-exclusive primary-product grain.
            weights = [7 + ((index * 5 + day_offset + segment * 3) % 11) for index in range(len(PRODUCTS))]
            allocations = {
                "sessions": _allocate_integer(ga4_sessions, weights),
                "active_user_days": _allocate_integer(ga4_users, weights),
                "product_views": _allocate_integer(ga4_views, weights),
                "add_to_carts": _allocate_integer(ga4_carts, weights),
                "begin_checkouts": _allocate_integer(ga4_checkouts, weights),
                "tracked_purchases": _allocate_integer(ga4_purchases, weights),
            }
            for product_index, product in enumerate(PRODUCTS):
                ga4_product_daily.append({
                    "date": day.isoformat(), "channel": channel, "source": source,
                    "medium": medium, "campaign": campaign, "device": device,
                    "product_id": product[0],
                    **{name: values[product_index] for name, values in allocations.items()},
                })
            event_counts = {
                "view_item_list": int(product_views * 1.18),
                "select_item": int(product_views * 1.04),
                "view_item": int(product_views * 0.97),
                "add_to_cart": int(add_to_carts * 0.96),
                "remove_from_cart": int(add_to_carts * 0.07),
                "view_cart": int(add_to_carts * 0.84),
                "begin_checkout": int(checkouts * 0.95),
                "add_shipping_info": int(checkouts * 0.88),
                "add_payment_info": int(checkouts * 0.79),
                "purchase": ga4_purchases,
                "refund": int(refunds > 0),
            }
            for event_name, event_count in event_counts.items():
                missing = day == date(2025, 5, 8) and segment == 0 and event_name == "purchase"
                events.append({
                    "date": day.isoformat(), "source": source, "device": device,
                    "event_name": event_name, "event_count": event_count,
                    "transaction_id_parameter_coverage": 0.8 if missing else 1.0,
                    "currency_parameter_coverage": 0.0 if missing else 1.0,
                    "value_parameter_coverage": 0.8 if missing else 1.0,
                    "items_parameter_coverage": 0.5 if missing else 1.0,
                    "item_id_parameter_coverage": 0.5 if missing else 1.0,
                    "item_name_parameter_coverage": 0.5 if missing else 1.0,
                    "item_category_parameter_coverage": 0.5 if missing else 1.0,
                    "price_parameter_coverage": 0.5 if missing else 1.0,
                    "quantity_parameter_coverage": 0.5 if missing else 1.0,
                    "promotion_parameter_coverage": 1.0,
                    "consent_state_coverage": round(consent_coverage, 4),
                })

        if day <= date(2025, 12, 20):
            for query_index in range(2):
                branded = query_index == 0 and day_offset % 3 == 0
                impressions = int((95 + rng.randint(0, 390)) * multiplier)
                clicks = int(impressions * rng.uniform(0.025, 0.115))
                search.append({
                    "date": day.isoformat(),
                    "query": "primeorder software" if branded else ["digital subscriptions saudi", "office software ksa", "ai tools arabic"][day_offset % 3],
                    "page": ["/", "/collections/productivity", "/collections/ai"][query_index],
                    "country": "SA", "device": DEVICES[(day_offset + query_index) % 3],
                    "clicks": clicks, "impressions": impressions,
                    "ctr": round(clicks / impressions, 6), "average_position": round(rng.uniform(3.2, 18.5), 2),
                    "is_branded": branded,
                })
        clarity.append({
            "date": day.isoformat(), "device": DEVICES[day_offset % 3], "country": "SA",
            "sessions": int(sum(row["sessions"] for row in ga4_daily[-3:]) * 0.93),
            "dead_clicks": rng.randint(0, 8), "rage_clicks": rng.randint(0, 4),
            "excessive_scrolls": rng.randint(1, 13), "javascript_errors": rng.randint(0, 3),
        })
        if day_offset % 7 == 0:
            for product_index, product in enumerate(PRODUCTS):
                status = "disapproved" if (day_offset == 210 and product_index == 7) else "approved"
                merchant.append({
                    "date": day.isoformat(), "product_id": product[0], "destination": "Shopping ads",
                    "status": status, "issue_code": "landing_page_unavailable" if status == "disapproved" else "none",
                    "affected_items": 1 if status == "disapproved" else 0,
                })

    observed_first_purchase: Dict[str, str] = {}
    for order in orders:
        customer = order["anonymous_customer_id"]
        observed_first_purchase[customer] = min(observed_first_purchase.get(customer, order["order_date"]), order["order_date"])
    for order in orders:
        customer_number = int(order["anonymous_customer_id"].split("-")[-1])
        if customer_number % 4 == 0:
            first_purchase = date(2024, 1 + customer_number % 12, 1 + customer_number % 27).isoformat()
        else:
            first_purchase = observed_first_purchase[order["anonymous_customer_id"]]
        order["customer_first_purchase_date"] = first_purchase
        order["customer_type"] = "returning" if first_purchase < START_DATE.isoformat() else "new"

    return {
        "products": products, "commerce_daily": commerce, "orders": orders,
        "order_items": order_items, "ga4_daily": ga4_daily, "ga4_product_daily": ga4_product_daily,
        "google_ads_daily": google_ads_daily, "events": events,
        "search_console": search, "merchant_diagnostics": merchant, "clarity_daily": clarity,
    }


def build_api(data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    commerce = data["commerce_daily"]
    ga4 = data["ga4_daily"]
    commerce_totals = {key: sum(float(r[key]) for r in commerce) for key in [
        "purchases", "units_sold", "gross_revenue_sar", "discount_sar", "refund_sar",
        "net_revenue_sar", "cost_sar",
    ]}
    ga4_totals = {key: sum(float(r[key]) for r in ga4) for key in [
        "sessions", "users", "product_views", "add_to_carts", "begin_checkouts", "purchases",
    ]}
    totals = {
        "sessions": ga4_totals["sessions"],
        "active_user_days": ga4_totals["users"],
        "product_views": ga4_totals["product_views"],
        "add_to_carts": ga4_totals["add_to_carts"],
        "begin_checkouts": ga4_totals["begin_checkouts"],
        "tracked_purchases": ga4_totals["purchases"],
        "completed_orders": commerce_totals["purchases"],
        **{key: commerce_totals[key] for key in [
            "units_sold", "gross_revenue_sar", "discount_sar", "refund_sar",
            "net_revenue_sar", "cost_sar",
        ]},
        "ad_spend_sar": sum(float(row["ad_spend_sar"]) for row in data["google_ads_daily"]),
    }
    totals.update({
        "average_order_value_sar": round2(totals["net_revenue_sar"] / totals["completed_orders"]),
        "purchase_conversion_rate": round(totals["tracked_purchases"] / totals["sessions"], 6),
        "refund_rate": round(totals["refund_sar"] / totals["gross_revenue_sar"], 6),
        "gross_margin_sar": round2(totals["net_revenue_sar"] - totals["cost_sar"]),
    })
    by_day: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in commerce:
        by_day[row["date"]]["completed_orders"] += float(row["purchases"])
        by_day[row["date"]]["net_revenue_sar"] += float(row["net_revenue_sar"])
    for row in ga4:
        by_day[row["date"]]["sessions"] += float(row["sessions"])
        by_day[row["date"]]["tracked_purchases"] += float(row["purchases"])
    timeseries = [{"date": day, **{k: round2(v) for k, v in values.items()}} for day, values in sorted(by_day.items())]
    summary = {
        "disclosure": DISCLOSURE, "currency": "SAR",
        "period": {"start": START_DATE.isoformat(), "end": iso_day(DAY_COUNT - 1).isoformat(), "days": DAY_COUNT},
        "totals": totals, "timeseries": timeseries,
    }
    funnel_counts = [
        ("sessions", totals["sessions"]), ("product_views", totals["product_views"]),
        ("add_to_carts", totals["add_to_carts"]), ("begin_checkouts", totals["begin_checkouts"]),
        ("tracked_purchases", totals["tracked_purchases"]),
    ]
    funnel_steps = []
    for index, (name, count) in enumerate(funnel_counts):
        prior = funnel_counts[index - 1][1] if index else count
        funnel_steps.append({
            "step": name, "count": int(count), "step_conversion_rate": round(count / prior, 6),
            "overall_conversion_rate": round(count / totals["sessions"], 6),
            "abandonment_rate": round(1 - count / prior, 6) if index else 0.0,
        })
    product_map = {r["product_id"]: r for r in data["products"]}
    order_refunds = {r["order_id"]: float(r["refund_sar"]) for r in data["orders"]}
    product_rollup: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for item in data["order_items"]:
        bucket = product_rollup[item["product_id"]]
        bucket["units_sold"] += float(item["quantity"])
        bucket["gross_revenue_sar"] += float(item["item_revenue_sar"])
        bucket["discount_sar"] += float(item["discount_sar"])
        bucket["refund_sar"] += order_refunds[item["order_id"]]
        bucket["cost_sar"] += float(item["item_cost_sar"])
    product_items = []
    for product_id, values in sorted(product_rollup.items(), key=lambda pair: pair[1]["gross_revenue_sar"] - pair[1]["discount_sar"] - pair[1]["refund_sar"], reverse=True):
        product = product_map.get(product_id, {"product_name_en": "Unmapped product", "product_name_ar": "منتج غير مطابق", "category": "Unmapped", "brand": "Unknown"})
        product_items.append({
            "product_id": product_id, "product_name_en": product["product_name_en"],
            "product_name_ar": product["product_name_ar"], "category": product["category"], "brand": product["brand"],
            "units_sold": int(values["units_sold"]),
            "revenue_sar": round2(values["gross_revenue_sar"] - values["discount_sar"] - values["refund_sar"]),
            "gross_margin_sar": round2(values["gross_revenue_sar"] - values["discount_sar"] - values["refund_sar"] - values["cost_sar"]),
        })
    acquisition_rollup: Dict[tuple, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in ga4:
        bucket = acquisition_rollup[(row["channel"], row["source"], row["medium"], row["campaign"])]
        bucket["sessions"] += float(row["sessions"])
        bucket["active_user_days"] += float(row["users"])
        bucket["tracked_purchases"] += float(row["purchases"])
        bucket["purchase_revenue_sar"] += float(row["purchase_revenue_sar"])
    for row in data["google_ads_daily"]:
        bucket = acquisition_rollup[(row["channel"], row["source"], row["medium"], row["campaign"])]
        bucket["ad_spend_sar"] += float(row["ad_spend_sar"])
    acquisition_items = []
    for keys, values in sorted(acquisition_rollup.items()):
        acquisition_items.append({
            "channel": keys[0], "source": keys[1], "medium": keys[2], "campaign": keys[3],
            "sessions": int(values["sessions"]), "active_user_days": int(values["active_user_days"]),
            "tracked_purchases": int(values["tracked_purchases"]),
            "purchase_revenue_sar": round2(values["purchase_revenue_sar"]),
            "ad_spend_sar": round2(values["ad_spend_sar"]),
            "conversion_rate": round(values["tracked_purchases"] / values["sessions"], 6),
            "roas": round(values["purchase_revenue_sar"] / values["ad_spend_sar"], 4) if values["ad_spend_sar"] else None,
        })
    seo_rollup: Dict[tuple, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in data["search_console"]:
        bucket = seo_rollup[(row["query"], row["page"], bool(row["is_branded"]))]
        bucket["clicks"] += float(row["clicks"]); bucket["impressions"] += float(row["impressions"])
        bucket["weighted_position"] += float(row["average_position"]) * float(row["impressions"])
    seo_items = [{
        "query": keys[0], "page": keys[1], "is_branded": keys[2], "clicks": int(values["clicks"]),
        "impressions": int(values["impressions"]), "ctr": round(values["clicks"] / values["impressions"], 6),
        "average_position": round(values["weighted_position"] / values["impressions"], 2),
    } for keys, values in sorted(seo_rollup.items(), key=lambda pair: pair[1]["clicks"], reverse=True)]
    customer_rollup: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"customers": set(), "completed_orders": 0, "net_revenue_sar": 0.0})
    for row in data["orders"]:
        bucket = customer_rollup[row["customer_type"]]
        bucket["customers"].add(row["anonymous_customer_id"])
        bucket["completed_orders"] += 1
        bucket["net_revenue_sar"] += float(row["net_revenue_sar"])
    customers = [{
        "customer_type": kind, "customers": len(values["customers"]), "completed_orders": int(values["completed_orders"]),
        "net_revenue_sar": round2(values["net_revenue_sar"]),
        "revenue_share": round(values["net_revenue_sar"] / totals["net_revenue_sar"], 6),
    } for kind, values in sorted(customer_rollup.items())]
    tracking_counts: Dict[str, int] = defaultdict(int)
    for order in data["orders"]:
        tracking_counts[order["tracking_transaction_id"]] += 1
    duplicate_rows = sum(count - 1 for count in tracking_counts.values() if count > 1)
    unknown_rows = sum(item["product_id"] not in product_map for item in data["order_items"])
    parameter_names = [
        "transaction_id_parameter_coverage", "currency_parameter_coverage",
        "value_parameter_coverage", "items_parameter_coverage", "item_id_parameter_coverage",
        "item_name_parameter_coverage", "item_category_parameter_coverage",
        "price_parameter_coverage", "quantity_parameter_coverage",
    ]
    event_groups: Dict[tuple, List[Dict[str, Any]]] = defaultdict(list)
    for event in data["events"]:
        event_groups[(event["date"], event["event_name"])].append(event)
    group_quality = []
    for rows in event_groups.values():
        count = sum(int(row["event_count"]) for row in rows)
        parameter_value = min(
            sum(float(row[name]) * int(row["event_count"]) for row in rows) / count
            for name in parameter_names
        ) if count else 1.0
        consent_value = sum(float(row["consent_state_coverage"]) * int(row["event_count"]) for row in rows) / count if count else 1.0
        group_quality.append((parameter_value, consent_value))
    parameter_completeness = min(value[0] for value in group_quality)
    parameter_affected_groups = sum(value[0] < 1.0 for value in group_quality)
    consent_coverage = min(value[1] for value in group_quality)
    consent_affected_groups = sum(value[1] < 0.95 for value in group_quality)
    salla_by_day: Dict[str, int] = defaultdict(int)
    ga4_by_day: Dict[str, int] = defaultdict(int)
    for row in commerce:
        salla_by_day[row["date"]] += int(row["purchases"])
    for row in data["ga4_daily"]:
        ga4_by_day[row["date"]] += int(row["purchases"])
    daily_variances = {
        day: abs(count - ga4_by_day[day]) / count
        for day, count in salla_by_day.items() if count
    }
    reconciliation_affected_days = sum(value > 0.10 for value in daily_variances.values())
    freshness_days = (iso_day(DAY_COUNT - 1) - max(date.fromisoformat(row["date"]) for row in data["search_console"])).days
    quality_specs = [
        ("duplicate_transactions", "high", round(duplicate_rows / len(data["orders"]), 6), 0.0, duplicate_rows, duplicate_rows == 0),
        ("unknown_products", "high", round(unknown_rows / len(data["order_items"]), 6), 0.0, unknown_rows, unknown_rows == 0),
        ("event_parameter_completeness", "medium", round(parameter_completeness, 6), 1.0, parameter_affected_groups, parameter_affected_groups == 0),
        ("search_freshness_days", "medium", float(freshness_days), 7.0, freshness_days, freshness_days <= 7),
        ("daily_reconciliation", "medium", round(max(daily_variances.values()), 6), 0.10, reconciliation_affected_days, reconciliation_affected_days == 0),
        ("consent_state_coverage", "low", round(consent_coverage, 6), 0.95, consent_affected_groups, consent_affected_groups == 0),
    ]
    quality_checks = [
        {"check_id": check_id, "status": "pass" if passed else "warning", "severity": severity,
         "metric_value": metric_value, "threshold": threshold, "affected_rows": affected_rows}
        for check_id, severity, metric_value, threshold, affected_rows, passed in quality_specs
    ]
    insights = [
        {"insight_id": "INS-001", "priority": 1, "area": "measurement", "title": "Resolve duplicate transaction tracking", "evidence": f"{duplicate_rows} duplicate synthetic tracking record detected", "confidence": "high", "recommended_action": "Deduplicate purchase events by transaction_id before attribution."},
        {"insight_id": "INS-002", "priority": 2, "area": "funnel", "title": "Investigate checkout abandonment", "evidence": f"{1 - totals['tracked_purchases'] / totals['begin_checkouts']:.1%} synthetic GA4 checkout-to-purchase abandonment", "confidence": "medium", "recommended_action": "Segment checkout friction by device and payment method, then test one change."},
        {"insight_id": "INS-003", "priority": 3, "area": "seo", "title": "Refresh Search Console ingestion", "evidence": "Synthetic Search Console source is 11 days stale", "confidence": "high", "recommended_action": "Restore daily extraction and alert when freshness exceeds seven days."},
    ]
    connector_items = connector_evidence()["connectors"]
    return {
        "summary": summary, "funnel": {"disclosure": DISCLOSURE, "steps": funnel_steps},
        "products": {"disclosure": DISCLOSURE, "items": product_items},
        "acquisition": {"disclosure": DISCLOSURE, "items": acquisition_items},
        "seo": {"disclosure": DISCLOSURE, "source_fresh_through": "2025-12-20", "items": seo_items},
        "customers": {"disclosure": DISCLOSURE, "segments": customers},
        "quality": {"disclosure": DISCLOSURE, "checks": quality_checks, "documented_anomalies": ANOMALIES},
        "insights": {"disclosure": DISCLOSURE, "items": insights},
        "connectors": {"disclosure": DISCLOSURE, "items": connector_items},
    }


def connector_evidence() -> Dict[str, Any]:
    freshness = {
        "salla_mcp": "2025-12-31", "ga4": "2025-12-31", "search_console": "2025-12-20",
        "merchant": "2025-12-31", "clarity": "2025-12-31", "google_ads": "2025-12-31",
    }
    return {
        "schema_version": "1.0.0",
        "generated_at": "2025-12-31T23:59:59Z",
        "data_mode": "public-demo",
        "contains_payloads": False,
        "connectors": [
            {
                "id": name,
                "display_name": display,
                "status": "FIXTURE_MODE",
                "live_status": "READY_NOT_AUTHENTICATED",
                "read_only": True,
                "fallback_formats": formats,
                "fixture_fresh_through": freshness[name],
                "source_timezone": "Asia/Riyadh",
                "report_range": {"start": "2025-01-01", "end": freshness[name]},
                "currency": "SAR",
                "evidence_ref": f"artifacts/evidence/connector-status.json#{name}",
                "schema_validation": "enabled",
                "max_retries": 2,
                "retry_policy": {"on": ["timeout", "connection", "transient_os_error"], "backoff_seconds": [0.25, 0.5]},
                "payloads_persisted": False,
            }
            for name, display, formats in [
                ("salla_mcp", "PrimeOrder / Salla MCP", ["csv", "json"]),
                ("ga4", "Google Analytics 4", ["csv", "json"]),
                ("search_console", "Google Search Console", ["csv", "json"]),
                ("merchant", "Google Merchant Center", ["csv", "json"]),
                ("clarity", "Microsoft Clarity", ["csv", "json"]),
                ("google_ads", "Google Ads", ["csv", "json"]),
            ]
        ],
    }


def _allocate_integer(total: int, weights: List[int]) -> List[int]:
    """Allocate an integer total proportionally while preserving the exact sum."""
    weight_total = sum(weights)
    if weight_total <= 0:
        return [0 for _ in weights]
    exact = [total * weight / weight_total for weight in weights]
    allocated = [math.floor(value) for value in exact]
    for index in sorted(range(len(weights)), key=lambda item: (-(exact[item] - allocated[item]), item))[: total - sum(allocated)]:
        allocated[index] += 1
    return allocated


def build_dashboard(data: Dict[str, List[Dict[str, Any]]], api: Dict[str, Any]) -> Dict[str, Any]:
    """Adapt the canonical fixture into the frontend's static DashboardData v1.0."""
    product_map = {row["product_id"]: row for row in data["products"]}
    order_map = {row["order_id"]: row for row in data["orders"]}
    category_ar = {
        "Productivity": "الإنتاجية", "Education": "التعليم", "Design": "التصميم",
        "AI": "الذكاء الاصطناعي", "Security": "الأمان", "Cloud": "السحابة",
        "Unmapped": "غير مطابق",
    }
    record_groups: Dict[tuple, Dict[str, Any]] = {}
    for item in data["order_items"]:
        order = order_map[item["order_id"]]
        product = product_map.get(item["product_id"], {
            "product_id": item["product_id"], "category": "Unmapped",
            "product_name_en": "Unmapped product", "product_name_ar": "منتج غير مطابق",
        })
        key = (order["order_date"], order["device"].title(), order["channel"], product["product_id"])
        group = record_groups.setdefault(key, {
            "date": order["order_date"], "device": order["device"].title(),
            "channel": order["channel"], "category": product["category"].lower().replace(" ", "-"),
            "product": product["product_id"], "sessions": 0, "activeUserDays": 0, "viewItem": 0,
            "addToCart": 0, "beginCheckout": 0, "trackedPurchases": 0, "orders": 0, "units": 0,
            "revenue": 0.0, "refunds": 0.0,
        })
        group["orders"] += 1
        group["units"] += int(item["quantity"])
        # DashboardData treats revenue as completed-order value after discounts but
        # before refunds; the UI subtracts the separate refunds field for net KPI.
        group["revenue"] += float(item["item_revenue_sar"]) - float(item["discount_sar"])
        group["refunds"] += float(order["refund_sar"])
    for behavior in data["ga4_product_daily"]:
        product = product_map[behavior["product_id"]]
        key = (behavior["date"], behavior["device"].title(), behavior["channel"], behavior["product_id"])
        group = record_groups.setdefault(key, {
            "date": behavior["date"], "device": behavior["device"].title(),
            "channel": behavior["channel"], "category": product["category"].lower().replace(" ", "-"),
            "product": behavior["product_id"], "sessions": 0, "activeUserDays": 0, "viewItem": 0,
            "addToCart": 0, "beginCheckout": 0, "trackedPurchases": 0, "orders": 0, "units": 0,
            "revenue": 0.0, "refunds": 0.0,
        })
        for source, target in [
            ("sessions", "sessions"), ("active_user_days", "activeUserDays"),
            ("product_views", "viewItem"), ("add_to_carts", "addToCart"),
            ("begin_checkouts", "beginCheckout"), ("tracked_purchases", "trackedPurchases"),
        ]:
            group[target] += int(behavior[source])
    records = sorted(record_groups.values(), key=lambda row: (row["date"], row["product"], row["device"], row["channel"]))
    for row in records:
        row["revenue"] = round2(row["revenue"])
        row["refunds"] = round2(row["refunds"])

    query_ar = {
        "primeorder software": "برامج برايم أوردر",
        "digital subscriptions saudi": "اشتراكات رقمية السعودية",
        "office software ksa": "برامج مكتبية السعودية",
        "ai tools arabic": "أدوات ذكاء اصطناعي عربية",
    }
    query_rollup: Dict[tuple, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    page_rollup: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in data["search_console"]:
        bucket = query_rollup[(row["query"], bool(row["is_branded"]))]
        bucket["clicks"] += int(row["clicks"]); bucket["impressions"] += int(row["impressions"])
        bucket["weighted_position"] += float(row["average_position"]) * int(row["impressions"])
        page_rollup[row["page"]]["clicks"] += int(row["clicks"])
        page_rollup[row["page"]]["impressions"] += int(row["impressions"])
    queries = [{
        "query": {"en": key[0], "ar": query_ar.get(key[0], key[0])},
        "type": "Branded" if key[1] else "Non-branded",
        "clicks": int(values["clicks"]), "impressions": int(values["impressions"]),
        "ctr": round(values["clicks"] / values["impressions"] * 100, 2),
        "position": round(values["weighted_position"] / values["impressions"], 2),
    } for key, values in sorted(query_rollup.items(), key=lambda pair: pair[1]["clicks"], reverse=True)]
    landing_pages = [{
        "page": page, "clicks": int(values["clicks"]), "impressions": int(values["impressions"]),
        "ctr": round(values["clicks"] / values["impressions"] * 100, 2) if values["impressions"] else 0.0,
    } for page, values in sorted(page_rollup.items(), key=lambda pair: pair[1]["clicks"], reverse=True)]
    issue_names = {
        "landing_page_unavailable": {"en": "Landing page unavailable", "ar": "الصفحة المقصودة غير متاحة"},
        "none": {"en": "No active product issue", "ar": "لا توجد مشكلة نشطة في المنتج"},
    }
    merchant_issues: Dict[str, int] = defaultdict(int)
    for row in data["merchant_diagnostics"]:
        merchant_issues[row["issue_code"]] += int(row["affected_items"])
    merchant_diagnostics = [{
        "issue": issue_names[issue], "affectedItemSnapshots": affected,
        "severity": "High" if issue != "none" else "Low",
        "status": "Open" if affected else "Clear",
    } for issue, affected in sorted(merchant_issues.items())]

    customer_values: Dict[str, float] = defaultdict(float)
    customer_types: Dict[str, str] = {}
    customer_orders: Dict[str, int] = defaultdict(int)
    customer_months: Dict[str, set] = defaultdict(set)
    first_month: Dict[str, str] = {}
    for order in data["orders"]:
        customer = order["anonymous_customer_id"]
        customer_values[customer] += float(order["net_revenue_sar"])
        customer_orders[customer] += 1
        prior_type = customer_types.setdefault(customer, order["customer_type"])
        if prior_type != order["customer_type"]:
            raise ValueError(f"Customer lifecycle classification changed for {customer}")
        month = order["order_date"][:7]
        customer_months[customer].add(month)
        first_month[customer] = min(first_month.get(customer, month), month)
    segments = []
    total_customer_revenue = sum(customer_values.values())
    for kind, label in [("new", {"en": "New customers", "ar": "عملاء جدد"}), ("returning", {"en": "Returning customers", "ar": "عملاء عائدون"})]:
        selected = [customer for customer, value in customer_types.items() if value == kind]
        revenue = sum(customer_values[customer] for customer in selected)
        segments.append({
            "segment": label, "customers": len(selected), "orders": sum(customer_orders[customer] for customer in selected),
            "revenue": round2(revenue), "share": round(revenue / total_customer_revenue * 100, 2),
        })
    cohorts = []
    for cohort in ["2025-09", "2025-10", "2025-11", "2025-12"]:
        members = [customer for customer, month in first_month.items() if month == cohort]
        year, month_number = map(int, cohort.split("-"))
        values = []
        for offset in range(4):
            absolute = year * 12 + month_number - 1 + offset
            target = f"{absolute // 12:04d}-{absolute % 12 + 1:02d}"
            retained = sum(target in customer_months[customer] for customer in members)
            values.append(round(retained / len(members) * 100, 1) if members and target <= "2025-12" else 0.0)
        cohorts.append({"cohort": cohort, "month0": values[0], "month1": values[1], "month2": values[2], "month3": values[3]})
    bands = [
        ("< 150 SAR", lambda value: value < 150),
        ("150–299 SAR", lambda value: 150 <= value < 300),
        ("300–599 SAR", lambda value: 300 <= value < 600),
        ("600+ SAR", lambda value: value >= 600),
    ]
    value_distribution = [{"band": name, "customers": sum(predicate(value) for value in customer_values.values())} for name, predicate in bands]

    connector_counts = {
        "salla_mcp": len(data["orders"]), "ga4": len(data["ga4_daily"]),
        "search_console": len(data["search_console"]), "merchant": len(data["merchant_diagnostics"]),
        "clarity": len(data["clarity_daily"]),
        "google_ads": len(data["google_ads_daily"]),
    }
    connectors = [{
        "id": item["id"], "name": item["display_name"], "status": item["status"],
        "freshness": f"{item['fixture_fresh_through']}T23:59:59Z", "records": connector_counts[item["id"]],
    } for item in api["connectors"]["items"]]
    quality_copy = {
        "duplicate_transactions": ({"en": "Unique transaction IDs", "ar": "معرّفات معاملات فريدة"}, {"en": "Deduplicate purchase events by transaction_id.", "ar": "إزالة تكرار أحداث الشراء حسب معرّف المعاملة."}),
        "unknown_products": ({"en": "Known product references", "ar": "مراجع المنتجات المعروفة"}, {"en": "Quarantine unknown IDs and repair catalog mappings.", "ar": "عزل المعرّفات غير المعروفة وإصلاح ربط الكتالوج."}),
        "event_parameter_completeness": ({"en": "Event parameter completeness", "ar": "اكتمال معلمات الأحداث"}, {"en": "Validate required GA4 item and transaction fields.", "ar": "التحقق من حقول GA4 المطلوبة للمنتج والمعاملة."}),
        "search_freshness_days": ({"en": "Search data freshness", "ar": "حداثة بيانات البحث"}, {"en": "Alert when Search Console freshness exceeds seven days.", "ar": "التنبيه عند تجاوز حداثة بيانات البحث سبعة أيام."}),
        "daily_reconciliation": ({"en": "Salla versus GA4 daily reconciliation", "ar": "المطابقة اليومية بين سلة وGA4"}, {"en": "Investigate daily variance above ten percent.", "ar": "فحص التباين اليومي الذي يتجاوز عشرة بالمئة."}),
        "consent_state_coverage": ({"en": "Consent-state coverage", "ar": "تغطية حالة الموافقة"}, {"en": "Validate consent defaults and updates in EEA test journeys.", "ar": "التحقق من إعدادات الموافقة الافتراضية وتحديثاتها في اختبارات المنطقة الاقتصادية الأوروبية."}),
    }
    rules = []
    for check in api["quality"]["checks"]:
        name, remediation = quality_copy[check["check_id"]]
        rules.append({
            "id": check["check_id"], "name": name, "status": check["status"], "severity": check["severity"],
            "evidence": {
                "en": f"Synthetic check value {check['metric_value']}; threshold {check['threshold']}; affected rows/days {check['affected_rows']}.",
                "ar": f"قيمة الفحص الاصطناعي {check['metric_value']}؛ الحد {check['threshold']}؛ الصفوف أو الأيام المتأثرة {check['affected_rows']}.",
            },
            "remediation": remediation,
        })
    severity_penalty = {"high": 8, "medium": 4, "low": 2}
    health_score = max(0, 100 - sum(severity_penalty[check["severity"]] for check in api["quality"]["checks"] if check["status"] != "pass"))
    salla_orders = sum(int(row["purchases"]) for row in data["commerce_daily"])
    ga4_orders = sum(int(row["purchases"]) for row in data["ga4_daily"])
    salla_revenue = sum(float(row["net_revenue_sar"]) for row in data["commerce_daily"])
    ga4_revenue = sum(float(row["purchase_revenue_sar"]) for row in data["ga4_daily"])
    reconciliation = {
        "sallaOrders": salla_orders, "ga4Orders": ga4_orders,
        "orderVariance": round((ga4_orders - salla_orders) / salla_orders * 100, 2),
        "sallaRevenue": round2(salla_revenue), "ga4Revenue": round2(ga4_revenue),
        "revenueVariance": round((ga4_revenue - salla_revenue) / salla_revenue * 100, 2),
    }
    insight_ar = {
        "INS-001": ("إصلاح تتبع المعاملات المكررة", "إزالة التكرار حسب معرّف المعاملة قبل الإسناد."),
        "INS-002": ("فحص تسرب إتمام الدفع", "تقسيم احتكاك الدفع حسب الجهاز وطريقة الدفع ثم اختبار تغيير واحد."),
        "INS-003": ("تحديث استيراد بيانات البحث", "استعادة الاستيراد اليومي والتنبيه عند تجاوز سبعة أيام."),
    }
    insight_meta = {
        "INS-001": ("Measurement repair", "Orders and revenue", "Analytics engineer", "Replay a synthetic purchase in debug mode and verify one event per transaction.", "S", 94),
        "INS-002": ("Checkout friction", "Checkout completion", "CRO lead", "Run a device and payment usability study before any A/B test.", "M", 84),
        "INS-003": ("SEO", "Organic reporting freshness", "SEO analyst", "Restore the fixture-equivalent daily job and observe freshness for 14 days.", "S", 78),
    }
    insights = []
    for item in api["insights"]["items"]:
        ar_finding, ar_action = insight_ar[item["insight_id"]]
        category, kpi, owner, experiment, effort, priority = insight_meta[item["insight_id"]]
        insights.append({
            "id": item["insight_id"], "category": category,
            "finding": {"en": item["title"], "ar": ar_finding},
            "evidence": {"en": item["evidence"], "ar": f"دليل اصطناعي: {item['evidence']}"},
            "kpi": {"en": kpi, "ar": "مؤشر قرار موثق"},
            "action": {"en": item["recommended_action"], "ar": ar_action},
            "direction": {"en": "Improve decision reliability", "ar": "تحسين موثوقية القرار"},
            "confidence": item["confidence"].title(), "effort": effort, "priority": priority,
            "owner": {"en": owner, "ar": "مسؤول التحليلات"},
            "experiment": {"en": experiment, "ar": "تنفيذ تجربة تحقق محددة قبل أي ادعاء بالأثر."},
            "status": "Ready" if item["priority"] <= 2 else "Monitoring",
        })
    catalog_products = [{
        "id": row["product_id"],
        "name": {"en": row["product_name_en"], "ar": row["product_name_ar"]},
        "category": row["category"].lower().replace(" ", "-"),
        "categoryName": {"en": row["category"], "ar": category_ar[row["category"]]},
    } for row in data["products"]]
    catalog_products.append({
        "id": "UNMAPPED-001", "name": {"en": "Unmapped product", "ar": "منتج غير مطابق"},
        "category": "unmapped", "categoryName": {"en": "Unmapped", "ar": category_ar["Unmapped"]},
    })
    return {
        "schemaVersion": "1.0",
        "meta": {
            "dataMode": "public-demo", "generatedAt": "2025-12-31T23:59:59Z",
            "periodStart": START_DATE.isoformat(), "periodEnd": iso_day(DAY_COUNT - 1).isoformat(),
            "currency": "SAR", "locale": "en-SA", "seed": SEED,
        },
        "catalog": {
            "products": catalog_products,
            "channels": sorted({row["channel"] for row in records}),
            "devices": ["Mobile", "Desktop", "Tablet"],
        },
        "records": records,
        "seo": {"queries": queries, "landingPages": landing_pages, "merchantDiagnostics": merchant_diagnostics},
        "customers": {"segments": segments, "cohorts": cohorts, "valueDistribution": value_distribution},
        "quality": {
            "healthScore": health_score, "connectors": connectors, "rules": rules,
            "reconciliation": reconciliation,
            "consentStateCoverage": round(next(check["metric_value"] for check in api["quality"]["checks"] if check["check_id"] == "consent_state_coverage") * 100, 2),
        },
        "insights": insights,
    }
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PUBLIC_DIR)
    parser.add_argument("--seed-output", type=Path, default=SEED_DIR)
    parser.add_argument("--dashboard-output", type=Path, default=DASHBOARD_PATH)
    args = parser.parse_args()
    output = args.output.resolve()
    seed_output = args.seed_output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    seed_output.mkdir(parents=True, exist_ok=True)
    data = generate()
    fields = {
        "products": ["product_id", "product_name_en", "product_name_ar", "category", "brand", "list_price_sar", "unit_cost_sar", "is_active"],
        "commerce_daily": ["date", "channel", "source", "medium", "campaign", "device", "city", "payment_method", "purchases", "units_sold", "gross_revenue_sar", "discount_sar", "refund_sar", "net_revenue_sar", "cost_sar"],
        "orders": ["order_id", "tracking_transaction_id", "order_date", "anonymous_customer_id", "customer_first_purchase_date", "customer_type", "channel", "source", "medium", "campaign", "device", "city", "payment_method", "coupon_group", "order_status", "gross_revenue_sar", "discount_sar", "refund_sar", "net_revenue_sar"],
        "order_items": ["order_id", "order_date", "product_id", "quantity", "item_revenue_sar", "item_cost_sar", "discount_sar"],
        "ga4_daily": ["date", "channel", "source", "medium", "campaign", "device", "sessions", "users", "product_views", "add_to_carts", "begin_checkouts", "purchases", "purchase_revenue_sar", "consent_state_coverage"],
        "ga4_product_daily": ["date", "channel", "source", "medium", "campaign", "device", "product_id", "sessions", "active_user_days", "product_views", "add_to_carts", "begin_checkouts", "tracked_purchases"],
        "google_ads_daily": ["date", "channel", "source", "medium", "campaign", "clicks", "conversions", "conversion_value_sar", "ad_spend_sar"],
        "events": ["date", "source", "device", "event_name", "event_count", "transaction_id_parameter_coverage", "currency_parameter_coverage", "value_parameter_coverage", "items_parameter_coverage", "item_id_parameter_coverage", "item_name_parameter_coverage", "item_category_parameter_coverage", "price_parameter_coverage", "quantity_parameter_coverage", "promotion_parameter_coverage", "consent_state_coverage"],
        "search_console": ["date", "query", "page", "country", "device", "clicks", "impressions", "ctr", "average_position", "is_branded"],
        "merchant_diagnostics": ["date", "product_id", "destination", "status", "issue_code", "affected_items"],
        "clarity_daily": ["date", "device", "country", "sessions", "dead_clicks", "rage_clicks", "excessive_scrolls", "javascript_errors"],
    }
    for name, rows in data.items():
        write_csv(output / f"{name}.csv", rows, fields[name])
        write_csv(seed_output / f"{name}.csv", rows, fields[name])
    api = build_api(data)
    for name, payload in api.items():
        write_json(output / "api" / f"{name}.json", payload)
    write_json(args.dashboard_output.resolve(), build_dashboard(data, api))
    evidence = connector_evidence()
    write_json(ROOT / "artifacts" / "evidence" / "connector-status.json", evidence)
    payload_hashes = {}
    for path in sorted(output.rglob("*")):
        if path.is_file() and path.name not in {"manifest.json", "metadata.json"}:
            payload_hashes[str(path.relative_to(output)).replace("\\", "/")] = hashlib.sha256(path.read_bytes()).hexdigest()
    metadata = {
        "schema_version": "1.0.0", "seed": SEED, "start_date": START_DATE.isoformat(),
        "end_date": iso_day(DAY_COUNT - 1).isoformat(), "day_count": DAY_COUNT,
        "data_mode": "public-demo", "disclosure": DISCLOSURE,
        "derived_from_real_merchant_data": False, "anomalies": ANOMALIES,
        "parameter_coverage_semantics": "1 means present and valid when applicable, or explicitly not applicable for that event; values below 1 mean applicable records are incomplete.",
        "row_counts": {name: len(rows) for name, rows in data.items()}, "sha256": payload_hashes,
    }
    write_json(output / "metadata.json", metadata)
    manifest_files = {**payload_hashes, "metadata.json": hashlib.sha256((output / "metadata.json").read_bytes()).hexdigest()}
    write_json(output / "manifest.json", {"schema_version": "1.0.0", "files": manifest_files})
    print(json.dumps({"output": str(output), "seed": SEED, "days": DAY_COUNT, "rows": metadata["row_counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
