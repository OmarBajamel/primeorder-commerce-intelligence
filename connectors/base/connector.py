"""Shared, typed connector contract with deterministic file fallbacks."""

from __future__ import annotations

import csv
import json
import os
import time
from abc import ABC, abstractmethod
from datetime import date as Date, datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Literal, Optional, Sequence, Type

from pydantic import BaseModel, ConfigDict, Field


class ConnectorStatus(str, Enum):
    CONNECTED = "CONNECTED"
    READY_NOT_AUTHENTICATED = "READY_NOT_AUTHENTICATED"
    FIXTURE_MODE = "FIXTURE_MODE"
    UNAVAILABLE = "UNAVAILABLE"
    FAILED_WITH_EVIDENCE = "FAILED_WITH_EVIDENCE"


class ConnectorMode(str, Enum):
    FIXTURE = "fixture"
    FILE = "file"
    LIVE_PRIVATE = "live-private"


class ConnectorError(BaseModel):
    code: str
    message: str
    retryable: bool = False


class ConnectorRecord(BaseModel):
    """Privacy-safe superset used after source-specific validation/projection."""

    model_config = ConfigDict(extra="forbid")
    date: Optional[Date] = None
    period: Optional[str] = None
    source: Optional[str] = None
    medium: Optional[str] = None
    channel: Optional[str] = None
    campaign: Optional[str] = None
    device: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    query: Optional[str] = None
    page: Optional[str] = None
    product_id: Optional[str] = None
    category: Optional[str] = None
    payment_method: Optional[str] = None
    coupon_group: Optional[str] = None
    destination: Optional[str] = None
    status: Optional[str] = None
    issue_code: Optional[str] = None
    sessions: Optional[int] = Field(default=None, ge=0)
    users: Optional[int] = Field(default=None, ge=0)
    product_views: Optional[int] = Field(default=None, ge=0)
    add_to_carts: Optional[int] = Field(default=None, ge=0)
    begin_checkouts: Optional[int] = Field(default=None, ge=0)
    purchases: Optional[int] = Field(default=None, ge=0)
    order_count: Optional[int] = Field(default=None, ge=0)
    completed_orders: Optional[int] = Field(default=None, ge=0)
    units_sold: Optional[int] = Field(default=None, ge=0)
    clicks: Optional[int] = Field(default=None, ge=0)
    impressions: Optional[int] = Field(default=None, ge=0)
    affected_items: Optional[int] = Field(default=None, ge=0)
    dead_clicks: Optional[int] = Field(default=None, ge=0)
    rage_clicks: Optional[int] = Field(default=None, ge=0)
    excessive_scrolls: Optional[int] = Field(default=None, ge=0)
    javascript_errors: Optional[int] = Field(default=None, ge=0)
    abandoned_carts: Optional[int] = Field(default=None, ge=0)
    catalog_item_count: Optional[int] = Field(default=None, ge=0)
    ctr: Optional[float] = Field(default=None, ge=0, le=1)
    average_position: Optional[float] = Field(default=None, gt=0)
    consent_state_coverage: Optional[float] = Field(default=None, ge=0, le=1)
    gross_revenue_sar: Optional[float] = Field(default=None, ge=0)
    purchase_revenue_sar: Optional[float] = Field(default=None, ge=0)
    refund_sar: Optional[float] = Field(default=None, ge=0)
    net_revenue_sar: Optional[float] = None
    ad_spend_sar: Optional[float] = Field(default=None, ge=0)
    conversion_value_sar: Optional[float] = Field(default=None, ge=0)
    conversions: Optional[float] = Field(default=None, ge=0)
    is_branded: Optional[bool] = None


class ReportRange(BaseModel):
    start: Date
    end: Date


class ConnectorResult(BaseModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    connector_id: str
    status: ConnectorStatus
    mode: ConnectorMode
    read_only: bool = True
    fetched_at: datetime
    fresh_through: Optional[Date] = None
    source_timezone: str = "Asia/Riyadh"
    report_range: Optional[ReportRange] = None
    currency: Literal["SAR"] = "SAR"
    evidence_ref: str
    record_count: int = 0
    records: List[ConnectorRecord] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    error: Optional[ConnectorError] = None


class BaseConnector(ABC):
    connector_id: str
    required_fields: Sequence[str] = ()
    credential_env: Sequence[str] = ()
    max_retries: int = 2
    record_model: Type[BaseModel] = ConnectorRecord

    @property
    def authenticated(self) -> bool:
        return bool(self.credential_env) and all(bool(os.getenv(name)) for name in self.credential_env)

    def status(self, mode: ConnectorMode = ConnectorMode.FIXTURE) -> ConnectorStatus:
        if mode in {ConnectorMode.FIXTURE, ConnectorMode.FILE}:
            return ConnectorStatus.FIXTURE_MODE
        return ConnectorStatus.CONNECTED if self.authenticated else ConnectorStatus.READY_NOT_AUTHENTICATED

    def validate_records(self, records: Iterable[Dict[str, Any]]) -> List[ConnectorRecord]:
        validated: List[ConnectorRecord] = []
        for index, row in enumerate(records, start=1):
            missing = [field for field in self.required_fields if row.get(field) in (None, "")]
            if missing:
                raise ValueError(f"{self.connector_id} row {index} missing required fields: {', '.join(missing)}")
            source_record = self.record_model.model_validate(row)
            validated.append(ConnectorRecord.model_validate(source_record.model_dump(exclude_none=True)))
        return validated

    def evidence_ref(self) -> str:
        return f"artifacts/evidence/connector-status.json#{self.connector_id}"

    def execute_with_retry(
        self,
        operation: Callable[[], List[Dict[str, Any]]],
        *,
        backoff_seconds: float = 0.25,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> List[Dict[str, Any]]:
        """Retry only transient read failures; never retry schema/auth failures."""
        for attempt in range(self.max_retries + 1):
            try:
                return operation()
            except (TimeoutError, ConnectionError, OSError):
                if attempt >= self.max_retries:
                    raise
                sleeper(backoff_seconds * (2 ** attempt))
        raise RuntimeError("unreachable retry state")

    def _report_range(self, records: List[ConnectorRecord]) -> Optional[ReportRange]:
        values = [row.date for row in records if row.date]
        return ReportRange(start=min(values), end=max(values)) if values else None

    def result(self, records: List[ConnectorRecord], mode: ConnectorMode, fresh_through: Optional[Date] = None) -> ConnectorResult:
        return ConnectorResult(
            connector_id=self.connector_id,
            status=self.status(mode),
            mode=mode,
            fetched_at=datetime.now(timezone.utc),
            fresh_through=fresh_through,
            report_range=self._report_range(records),
            evidence_ref=self.evidence_ref(),
            record_count=len(records),
            records=records,
        )

    @abstractmethod
    def extract(self, mode: ConnectorMode = ConnectorMode.FIXTURE, path: Optional[Path] = None) -> ConnectorResult:
        raise NotImplementedError


class FileFallbackConnector(BaseConnector):
    fixture_path: Path
    date_field: str = "date"

    def __init__(self, live_executor: Optional[Callable[[], List[Dict[str, Any]]]] = None):
        self._live_executor = live_executor

    @property
    def authenticated(self) -> bool:
        return self._live_executor is not None or super().authenticated

    def _read_file(self, path: Path) -> List[Dict[str, Any]]:
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"Connector import not found: {path}")
        suffix = path.suffix.lower()
        if suffix == ".csv":
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                return list(csv.DictReader(handle))
        if suffix == ".json":
            value = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(value, dict) and "records" in value:
                value = value["records"]
            if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
                raise ValueError("JSON connector fallback must be a record array or {records: [...]} object")
            return value
        raise ValueError("Only .csv and .json connector fallbacks are supported")

    def _fresh_through(self, records: List[ConnectorRecord]) -> Optional[Date]:
        values = [getattr(row, self.date_field, None) for row in records]
        parsed: List[Date] = []
        for value in values:
            if value:
                try:
                    parsed.append(Date.fromisoformat(str(value)[:10]))
                except ValueError:
                    continue
        return max(parsed) if parsed else None

    def extract(self, mode: ConnectorMode = ConnectorMode.FIXTURE, path: Optional[Path] = None) -> ConnectorResult:
        if mode == ConnectorMode.LIVE_PRIVATE:
            if not self.authenticated:
                return ConnectorResult(
                    connector_id=self.connector_id,
                    status=ConnectorStatus.READY_NOT_AUTHENTICATED,
                    mode=mode,
                    fetched_at=datetime.now(timezone.utc),
                    evidence_ref=self.evidence_ref(),
                    warnings=["Live read-only credentials are not configured; no request was attempted."],
                )
            if self._live_executor is not None:
                records = self.validate_records(self.execute_with_retry(self._live_executor))
                return ConnectorResult(
                    connector_id=self.connector_id,
                    status=ConnectorStatus.CONNECTED,
                    mode=mode,
                    fetched_at=datetime.now(timezone.utc),
                    fresh_through=self._fresh_through(records),
                    report_range=self._report_range(records),
                    evidence_ref=self.evidence_ref(),
                    record_count=len(records),
                    records=records,
                    warnings=["Ephemeral read-only projection; records were not persisted by the connector."],
                )
            return ConnectorResult(
                connector_id=self.connector_id,
                status=ConnectorStatus.UNAVAILABLE,
                mode=mode,
                fetched_at=datetime.now(timezone.utc),
                evidence_ref=self.evidence_ref(),
                warnings=["Live transport is intentionally environment-owned; use the official read-only client."],
            )
        source = self.fixture_path if mode == ConnectorMode.FIXTURE else path
        if source is None:
            raise ValueError("A CSV or JSON path is required for file mode")
        records = self.validate_records(self._read_file(Path(source)))
        return self.result(records, mode, self._fresh_through(records))

    def safe_extract(self, mode: ConnectorMode = ConnectorMode.FIXTURE, path: Optional[Path] = None) -> ConnectorResult:
        """Return a typed failure without leaking file paths or credential details."""
        try:
            return self.extract(mode=mode, path=path)
        except (ValueError, OSError) as exc:
            retryable = isinstance(exc, OSError) and not isinstance(exc, FileNotFoundError)
            return ConnectorResult(
                connector_id=self.connector_id,
                status=ConnectorStatus.FAILED_WITH_EVIDENCE,
                mode=mode,
                fetched_at=datetime.now(timezone.utc),
                evidence_ref=self.evidence_ref(),
                error=ConnectorError(code=type(exc).__name__.upper(), message="Connector validation, import, or read transport failed.", retryable=retryable),
            )
