import json
from pathlib import Path

import pytest

from connectors.base import ConnectorMode, ConnectorStatus
from connectors.registry import connector_registry
from connectors.salla_mcp import SallaMCPConnector


def ga4_row(day="2025-01-01"):
    return {
        "date": day, "channel": "Organic Search", "source": "google", "medium": "organic",
        "campaign": "Always-on SEO", "device": "mobile", "sessions": 10, "users": 8,
        "product_views": 6, "add_to_carts": 3, "begin_checkouts": 2, "purchases": 1,
        "purchase_revenue_sar": 99, "consent_state_coverage": 0.98,
    }


def test_all_connectors_extract_deterministic_fixtures():
    connectors = connector_registry()
    assert len(connectors) == 6
    for connector in connectors:
        result = connector.extract()
        assert result.connector_id == connector.connector_id
        assert result.status == ConnectorStatus.FIXTURE_MODE
        assert result.mode == ConnectorMode.FIXTURE
        assert result.read_only is True
        assert result.record_count > 0
        assert result.fresh_through is not None
        assert result.schema_version == "1.0.0"
        assert result.source_timezone == "Asia/Riyadh"
        assert result.currency == "SAR"
        assert result.report_range.start <= result.report_range.end
        assert result.evidence_ref.endswith(f"#{connector.connector_id}")


def test_live_connectors_report_ready_not_authenticated(monkeypatch):
    for connector in connector_registry():
        if connector.connector_id == "salla_mcp":
            result = connector.extract(mode=ConnectorMode.LIVE_PRIVATE)
        else:
            for name in connector.credential_env:
                monkeypatch.delenv(name, raising=False)
            result = connector.extract(mode=ConnectorMode.LIVE_PRIVATE)
        assert result.status == ConnectorStatus.READY_NOT_AUTHENTICATED
        assert result.record_count == 0
        assert result.records == []


def test_csv_and_json_import_paths_validate_schema(tmp_path):
    connector = connector_registry()[1]
    csv_path = tmp_path / "ga4.csv"
    row = ga4_row()
    csv_path.write_text(",".join(row) + "\n" + ",".join(str(value) for value in row.values()) + "\n", encoding="utf-8")
    assert connector.extract(ConnectorMode.FILE, csv_path).record_count == 1
    json_path = tmp_path / "ga4.json"
    json_path.write_text(json.dumps({"records": [ga4_row("2025-01-02")]}), encoding="utf-8")
    assert connector.extract(ConnectorMode.FILE, json_path).fresh_through.isoformat() == "2025-01-02"


def test_import_rejects_missing_required_fields(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text('[{"date":"2025-01-01"}]', encoding="utf-8")
    with pytest.raises(ValueError, match="missing required fields"):
        connector_registry()[1].extract(ConnectorMode.FILE, path)


def test_safe_import_returns_typed_failure_without_path(tmp_path):
    missing = tmp_path / "private-name.csv"
    result = connector_registry()[1].safe_extract(ConnectorMode.FILE, missing)
    assert result.status == ConnectorStatus.FAILED_WITH_EVIDENCE
    assert result.error.code == "FILENOTFOUNDERROR"
    assert str(missing) not in result.model_dump_json()


def test_source_specific_types_reject_invalid_metrics_and_drop_unknown_fields(tmp_path):
    connector = connector_registry()[1]
    invalid = ga4_row()
    invalid["sessions"] = -1
    with pytest.raises(ValueError):
        connector.validate_records([invalid])
    valid = ga4_row()
    valid["authorization"] = "must-not-survive-projection"
    result = connector.validate_records([valid])[0]
    assert "authorization" not in result.model_dump_json()


def test_transient_read_retry_uses_bounded_exponential_backoff():
    connector = connector_registry()[1]
    attempts = []
    delays = []

    def operation():
        attempts.append(1)
        if len(attempts) < 3:
            raise TimeoutError("synthetic transient failure")
        return [ga4_row()]

    rows = connector.execute_with_retry(operation, backoff_seconds=0.1, sleeper=delays.append)
    assert len(rows) == 1
    assert len(attempts) == connector.max_retries + 1
    assert delays == [0.1, 0.2]


def test_salla_mcp_allow_list_and_projection_never_expose_identifiers():
    raw = [{
        "date": "2025-01-01", "completed_orders": 5, "net_revenue_sar": 500,
        "customer_email": "SYNTHETIC_EMAIL_TOKEN", "authorization": "SYNTHETIC_AUTH_TOKEN",
    }]
    connector = SallaMCPConnector(executor=lambda operation, params: raw)
    result = connector.extract_live_aggregate("get_order_aggregates")
    assert result.status == ConnectorStatus.CONNECTED
    payload = result.model_dump_json()
    assert "customer_email" not in payload
    assert "authorization" not in payload
    assert "SYNTHETIC_EMAIL_TOKEN" not in payload
    with pytest.raises(ValueError, match="read-only allow-list"):
        connector.extract_live_aggregate("create_order")
