"""Pydantic response models shared by the API and generated fixtures."""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


DISCLOSURE = "Synthetic portfolio demo data — no real customer or revenue information"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HealthResponse(StrictModel):
    status: Literal["ok"] = "ok"
    service: str = "primeorder-api"
    version: str = "1.0.0"


class ReadinessResponse(StrictModel):
    status: Literal["ready", "not_ready"]
    data_mode: Literal["public-demo", "live-private"]
    dataset_available: bool
    generated_fixture_available: bool


class Period(StrictModel):
    start: date
    end: date
    days: int = Field(ge=1)


class TimeSeriesPoint(StrictModel):
    date: date
    sessions: float = Field(ge=0)
    tracked_purchases: float = Field(ge=0)
    completed_orders: float = Field(ge=0)
    net_revenue_sar: float


class SummaryTotals(StrictModel):
    sessions: float; active_user_days: float; product_views: float; add_to_carts: float
    begin_checkouts: float; tracked_purchases: float; completed_orders: float; units_sold: float
    gross_revenue_sar: float; discount_sar: float; refund_sar: float
    net_revenue_sar: float; cost_sar: float; ad_spend_sar: float
    average_order_value_sar: float; purchase_conversion_rate: float
    refund_rate: float; gross_margin_sar: float


class SummaryResponse(StrictModel):
    disclosure: str
    currency: Literal["SAR"]
    period: Period
    totals: SummaryTotals
    timeseries: List[TimeSeriesPoint]


class FunnelStep(StrictModel):
    step: str; count: int; step_conversion_rate: float
    overall_conversion_rate: float; abandonment_rate: float


class FunnelResponse(StrictModel):
    disclosure: str
    steps: List[FunnelStep]


class ProductPerformance(StrictModel):
    product_id: str; product_name_en: str; product_name_ar: str
    category: str; brand: str; units_sold: int
    revenue_sar: float; gross_margin_sar: float


class ProductsResponse(StrictModel):
    disclosure: str
    items: List[ProductPerformance]


class AcquisitionPerformance(StrictModel):
    channel: str; source: str; medium: str; campaign: str
    sessions: int; active_user_days: int; tracked_purchases: int; purchase_revenue_sar: float
    ad_spend_sar: float; conversion_rate: float; roas: Optional[float]


class AcquisitionResponse(StrictModel):
    disclosure: str
    items: List[AcquisitionPerformance]


class SearchPerformance(StrictModel):
    query: str; page: str; is_branded: bool; clicks: int
    impressions: int; ctr: float; average_position: float


class SEOResponse(StrictModel):
    disclosure: str
    source_fresh_through: date
    items: List[SearchPerformance]


class CustomerSegment(StrictModel):
    customer_type: Literal["new", "returning"]
    customers: int; completed_orders: int; net_revenue_sar: float; revenue_share: float


class CustomersResponse(StrictModel):
    disclosure: str
    segments: List[CustomerSegment]


class DocumentedAnomaly(StrictModel):
    id: str; kind: str; date: date; severity: str
    expected_detection: str; description: str


class QualityCheck(StrictModel):
    check_id: str
    status: Literal["pass", "warning", "fail"]
    severity: str; metric_value: float; threshold: float; affected_rows: int


class QualityResponse(StrictModel):
    disclosure: str
    checks: List[QualityCheck]
    documented_anomalies: List[DocumentedAnomaly]


class Insight(StrictModel):
    insight_id: str; priority: int; area: str; title: str
    evidence: str; confidence: str; recommended_action: str


class InsightsResponse(StrictModel):
    disclosure: str
    items: List[Insight]


ConnectorState = Literal["CONNECTED", "READY_NOT_AUTHENTICATED", "FIXTURE_MODE", "FILE_MODE", "UNAVAILABLE", "FAILED_WITH_EVIDENCE"]


class ConnectorReportRange(StrictModel):
    start: date
    end: date


class RetryPolicy(StrictModel):
    on: List[Literal["timeout", "connection", "transient_os_error"]]
    backoff_seconds: List[float]


class ConnectorSummary(StrictModel):
    id: str; display_name: str; status: ConnectorState; live_status: ConnectorState
    read_only: bool
    fallback_formats: List[Literal["csv", "json"]]
    fixture_fresh_through: date
    source_timezone: Literal["Asia/Riyadh"]
    report_range: ConnectorReportRange
    currency: Literal["SAR"]
    evidence_ref: str
    schema_validation: Literal["enabled"]
    max_retries: int = Field(ge=0)
    retry_policy: RetryPolicy
    payloads_persisted: bool


class StatusResponse(StrictModel):
    disclosure: str
    items: List[ConnectorSummary]


class ErrorDetail(StrictModel):
    code: str
    message: str
    request_id: str


class ErrorResponse(StrictModel):
    error: ErrorDetail
