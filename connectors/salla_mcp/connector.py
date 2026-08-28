"""Privacy boundary for read-only PrimeOrder/Salla MCP aggregate exports.

The bridge accepts an injected executor owned by the local environment. It never
serializes raw results. Only an allow-listed aggregate projection is returned to
the caller, which remains responsible for storing live-private data under ignored
paths. Fixture mode is the only public/release mode.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field
from connectors.base import ConnectorMode, ConnectorRecord, ConnectorResult, ConnectorStatus, FileFallbackConnector


class SallaFixtureRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: date
    purchases: int = Field(ge=0)
    gross_revenue_sar: float = Field(ge=0)
    refund_sar: float = Field(ge=0)
    net_revenue_sar: float


class SallaMCPConnector(FileFallbackConnector):
    connector_id = "salla_mcp"
    required_fields = ("date", "purchases", "gross_revenue_sar", "net_revenue_sar")
    fixture_path = Path(__file__).resolve().parents[2] / "analytics" / "seeds" / "commerce_daily.csv"
    record_model = SallaFixtureRecord
    allowed_operations = frozenset({
        "get_order_aggregates", "get_product_performance", "get_payment_aggregates",
        "get_coupon_aggregates", "get_device_aggregates", "get_region_aggregates",
        "get_abandoned_cart_aggregates", "get_catalog_facts",
    })
    safe_aggregate_fields = frozenset({
        "date", "period", "product_id", "category", "payment_method", "coupon_group",
        "device", "city", "region", "order_count", "completed_orders", "purchases",
        "units_sold", "gross_revenue_sar", "refund_sar", "net_revenue_sar",
        "abandoned_carts", "catalog_item_count",
    })

    def __init__(self, executor: Optional[Callable[[str, Dict[str, Any]], List[Dict[str, Any]]]] = None):
        self._executor = executor

    @property
    def authenticated(self) -> bool:
        return self._executor is not None

    def extract_live_aggregate(self, operation: str, parameters: Optional[Dict[str, Any]] = None) -> ConnectorResult:
        if operation not in self.allowed_operations:
            raise ValueError(f"MCP operation is not on the read-only allow-list: {operation}")
        if self._executor is None:
            return ConnectorResult(
                connector_id=self.connector_id,
                status=ConnectorStatus.READY_NOT_AUTHENTICATED,
                mode=ConnectorMode.LIVE_PRIVATE,
                fetched_at=datetime.now(timezone.utc),
                evidence_ref=self.evidence_ref(),
                warnings=["No connected MCP executor; no live call was attempted."],
            )
        raw_rows = self.execute_with_retry(lambda: self._executor(operation, dict(parameters or {})))
        if not isinstance(raw_rows, list) or not all(isinstance(row, dict) for row in raw_rows):
            raise ValueError("MCP bridge expects an aggregate record list")
        projected = [
            ConnectorRecord.model_validate({key: value for key, value in row.items() if key in self.safe_aggregate_fields})
            for row in raw_rows
        ]
        return ConnectorResult(
            connector_id=self.connector_id,
            status=ConnectorStatus.CONNECTED,
            mode=ConnectorMode.LIVE_PRIVATE,
            fetched_at=datetime.now(timezone.utc),
            report_range=self._report_range(projected),
            evidence_ref=self.evidence_ref(),
            record_count=len(projected),
            records=projected,
            warnings=["Ephemeral aggregate projection; raw MCP results were not persisted."],
        )

    def extract(self, mode: ConnectorMode = ConnectorMode.FIXTURE, path: Optional[Path] = None) -> ConnectorResult:
        if mode == ConnectorMode.LIVE_PRIVATE:
            return self.extract_live_aggregate("get_order_aggregates")
        return super().extract(mode=mode, path=path)
