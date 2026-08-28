import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "generate_demo_data.py"


def directory_hash(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(path.rglob("*")):
        if file.is_file():
            digest.update(str(file.relative_to(path)).replace("\\", "/").encode())
            digest.update(file.read_bytes())
    return digest.hexdigest()


def run_generator(output: Path, seeds: Path) -> None:
    subprocess.run(
        [sys.executable, str(SCRIPT), "--output", str(output), "--seed-output", str(seeds), "--dashboard-output", str(output / "dashboard.json")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.fixture(scope="module")
def generated(tmp_path_factory):
    root = tmp_path_factory.mktemp("generated-public-demo")
    output = root / "public"
    run_generator(output, root / "seeds")
    return output


def test_generator_is_byte_deterministic(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    run_generator(first, tmp_path / "seeds-1")
    run_generator(second, tmp_path / "seeds-2")
    assert directory_hash(first) == directory_hash(second)
    before = directory_hash(first)
    run_generator(first, tmp_path / "seeds-1")
    assert directory_hash(first) == before


def test_metadata_documents_365_days_and_all_anomalies(generated):
    metadata = json.loads((generated / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["day_count"] == 365
    assert metadata["seed"] == 20250301
    assert metadata["derived_from_real_merchant_data"] is False
    assert {item["kind"] for item in metadata["anomalies"]} == {
        "duplicate_transaction_id", "missing_event_parameters", "stale_source",
        "unmapped_product", "tracking_variance", "consent_coverage",
    }


def test_synthetic_identifiers_and_saudi_dimensions_are_present(generated):
    with (generated / "orders.csv").open(encoding="utf-8", newline="") as handle:
        orders = list(csv.DictReader(handle))
    assert len(orders) > 5000
    assert all(row["anonymous_customer_id"].startswith("CUST-") for row in orders)
    assert {row["city"] for row in orders} >= {"Riyadh", "Jeddah", "Dammam"}
    assert {row["payment_method"] for row in orders} >= {"mada", "apple_pay", "stc_pay"}
    serialized = json.dumps(orders[:100])
    assert "@" not in serialized
    assert "+966" not in serialized


def test_api_artifacts_match_public_contract(generated):
    summary = json.loads((generated / "api" / "summary.json").read_text(encoding="utf-8"))
    assert summary["currency"] == "SAR"
    assert len(summary["timeseries"]) == 365
    assert summary["totals"]["completed_orders"] > 0
    assert summary["totals"]["tracked_purchases"] > 0
    assert "no real customer or revenue information" in summary["disclosure"]


def test_revenue_definitions_and_full_ga4_event_spec(generated):
    with (generated / "commerce_daily.csv").open(encoding="utf-8", newline="") as handle:
        commerce = list(csv.DictReader(handle))
    assert all(
        abs(float(row["gross_revenue_sar"]) - float(row["discount_sar"]) - float(row["refund_sar"]) - float(row["net_revenue_sar"])) < 0.01
        for row in commerce
    )
    with (generated / "events.csv").open(encoding="utf-8", newline="") as handle:
        events = list(csv.DictReader(handle))
    assert {row["event_name"] for row in events} == {
        "view_item_list", "select_item", "view_item", "add_to_cart", "remove_from_cart",
        "view_cart", "begin_checkout", "add_shipping_info", "add_payment_info", "purchase", "refund",
    }


def test_frontend_dashboard_contract_is_generated_from_full_period(generated):
    dashboard = json.loads((generated / "dashboard.json").read_text(encoding="utf-8"))
    assert dashboard["schemaVersion"] == "1.0"
    assert dashboard["meta"]["dataMode"] == "public-demo"
    assert dashboard["meta"]["periodStart"] == "2025-01-01"
    assert dashboard["meta"]["periodEnd"] == "2025-12-31"
    dates = {row["date"] for row in dashboard["records"]}
    assert len(dates) == 365
    assert min(dates) == "2025-01-01"
    assert max(dates) == "2025-12-31"
    summary = json.loads((generated / "api" / "summary.json").read_text(encoding="utf-8"))
    dashboard_net = round(sum(row["revenue"] - row["refunds"] for row in dashboard["records"]), 2)
    assert dashboard_net == summary["totals"]["net_revenue_sar"]


def test_product_behavior_is_ga4_scoped_and_customer_segments_are_stable(generated):
    with (generated / "ga4_product_daily.csv").open(encoding="utf-8", newline="") as handle:
        product_behavior = list(csv.DictReader(handle))
    with (generated / "ga4_daily.csv").open(encoding="utf-8", newline="") as handle:
        ga4 = list(csv.DictReader(handle))
    assert len(product_behavior) == 365 * 3 * 12
    assert sum(int(row["sessions"]) for row in product_behavior) == sum(int(row["sessions"]) for row in ga4)
    with (generated / "orders.csv").open(encoding="utf-8", newline="") as handle:
        orders = list(csv.DictReader(handle))
    by_customer = {}
    for order in orders:
        signature = (order["customer_first_purchase_date"], order["customer_type"])
        assert by_customer.setdefault(order["anonymous_customer_id"], signature) == signature
        assert (order["customer_type"] == "returning") == (order["customer_first_purchase_date"] < "2025-01-01")


def test_manifest_hashes_every_payload_without_recursive_self_hash(generated):
    manifest = json.loads((generated / "manifest.json").read_text(encoding="utf-8"))["files"]
    assert "manifest.json" not in manifest
    assert manifest["metadata.json"] == hashlib.sha256((generated / "metadata.json").read_bytes()).hexdigest()
    for relative, expected in manifest.items():
        assert hashlib.sha256((generated / relative).read_bytes()).hexdigest() == expected
