from fastapi.testclient import TestClient

from services.api.app import main
from services.api.app.main import app


client = TestClient(app)


def test_health_and_readiness_are_typed():
    assert client.get("/health").json() == {"status": "ok", "service": "primeorder-api", "version": "1.0.0"}
    readiness = client.get("/api/v1/readiness")
    assert readiness.status_code == 200
    assert readiness.json()["data_mode"] == "public-demo"


def test_connector_status_is_honest_and_payload_free():
    response = client.get("/status")
    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 6
    assert {item["status"] for item in items} == {"FIXTURE_MODE"}
    assert {item["live_status"] for item in items} == {"READY_NOT_AUTHENTICATED"}
    assert "records" not in response.text


def test_summary_period_filter_and_disclosure():
    response = client.get("/api/v1/summary", params={"date_from": "2025-03-01", "date_to": "2025-03-31"})
    assert response.status_code == 200
    body = response.json()
    assert len(body["timeseries"]) == 31
    assert body["currency"] == "SAR"
    assert "Synthetic portfolio demo data" in body["disclosure"]


def test_products_and_acquisition_filters():
    products = client.get("/products", params={"category": "AI", "limit": 2}).json()["items"]
    assert len(products) == 2
    assert all(row["category"] == "AI" for row in products)
    acquisition = client.get("/acquisition", params={"channel": "Paid Search"}).json()["items"]
    assert acquisition and all(row["channel"] == "Paid Search" for row in acquisition)


def test_seo_customer_quality_and_insight_filters():
    assert all(row["is_branded"] for row in client.get("/seo?branded=true").json()["items"])
    assert client.get("/customers?customer_type=returning").json()["segments"][0]["customer_type"] == "returning"
    assert all(row["severity"] == "high" for row in client.get("/quality?severity=high").json()["checks"])
    assert client.get("/insights?area=seo").json()["items"][0]["area"] == "seo"


def test_invalid_query_has_structured_error_without_details():
    response = client.get("/products?limit=0", headers={"x-request-id": "test-request"})
    assert response.status_code == 422
    assert response.json() == {
        "error": {"code": "VALIDATION_ERROR", "message": "One or more request parameters are invalid.", "request_id": "test-request"}
    }


def test_openapi_exposes_all_versioned_analytics_routes():
    paths = client.get("/openapi.json").json()["paths"]
    required = {"health", "readiness", "status", "summary", "funnel", "products", "acquisition", "seo", "customers", "quality", "insights"}
    assert {path.rsplit("/", 1)[-1] for path in paths if path.startswith("/api/v1/")} == required


def test_unexpected_errors_do_not_log_exception_payload(monkeypatch, caplog):
    marker = "PRIVATE_UPSTREAM_PAYLOAD_MUST_NOT_BE_LOGGED"

    def fail(*_args, **_kwargs):
        raise RuntimeError(marker)

    monkeypatch.setattr(main.repository, "validated", fail)
    response = client.get("/summary", headers={"x-request-id": "privacy-log-test"})
    assert response.status_code == 500
    assert marker not in response.text
    assert marker not in caplog.text
    assert "request_failed request_id=privacy-log-test path=/summary" in caplog.text


def test_untrusted_request_id_is_not_reflected_in_logs(caplog):
    marker = "security@example.invalid\nFORGED"
    response = client.get("/health", headers={"x-request-id": marker})
    assert response.status_code == 200
    assert marker not in caplog.text
    assert "security@example.invalid" not in response.headers["x-request-id"]
