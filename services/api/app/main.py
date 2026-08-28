"""Typed, privacy-safe analytics API for local public-demo exploration."""

from __future__ import annotations

import logging
import time
import uuid
from datetime import date
from typing import Optional

from fastapi import APIRouter, FastAPI, HTTPException, Query, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from packages.contracts.primeorder_contracts.models import (
    AcquisitionResponse,
    CustomersResponse,
    ErrorDetail,
    ErrorResponse,
    FunnelResponse,
    HealthResponse,
    InsightsResponse,
    ProductsResponse,
    QualityResponse,
    ReadinessResponse,
    SEOResponse,
    StatusResponse,
    SummaryResponse,
    SummaryTotals,
    Period,
)
from services.api.app.repository import PublicDemoRepository


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
logger = logging.getLogger("primeorder.api")
repository = PublicDemoRepository()

app = FastAPI(
    title="PrimeOrder Commerce Intelligence API",
    version="1.0.0",
    description="Read-only analytics over deterministic synthetic portfolio data.",
)
router = APIRouter()


def _error(status_code: int, code: str, message: str, request_id: str) -> JSONResponse:
    body = ErrorResponse(error=ErrorDetail(code=code, message=message, request_id=request_id))
    return JSONResponse(status_code=status_code, content=body.model_dump(mode="json"))


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))[:64]
    request.state.request_id = request_id
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except FileNotFoundError:
        response = _error(503, "DATASET_UNAVAILABLE", "Generate public-demo fixtures before requesting analytics.", request_id)
    except Exception:
        # Do not attach exception text or stack traces: future live-private
        # transports may raise errors containing upstream payload fragments.
        logger.error("request_failed request_id=%s path=%s", request_id, request.url.path)
        response = _error(500, "INTERNAL_ERROR", "The analytics request could not be completed.", request_id)
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    response.headers["x-request-id"] = request_id
    logger.info("request_id=%s method=%s path=%s status=%s duration_ms=%s", request_id, request.method, request.url.path, response.status_code, duration_ms)
    return response


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    return _error(422, "VALIDATION_ERROR", "One or more request parameters are invalid.", getattr(request.state, "request_id", "unknown"))


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    return _error(exc.status_code, "INVALID_REQUEST", str(exc.detail), getattr(request.state, "request_id", "unknown"))


@router.get("/health", response_model=HealthResponse, tags=["operations"])
def health() -> HealthResponse:
    return HealthResponse()


@router.get("/readiness", response_model=ReadinessResponse, tags=["operations"])
def readiness(response: Response) -> ReadinessResponse:
    available = repository.exists()
    if not available:
        response.status_code = 503
    return ReadinessResponse(
        status="ready" if available else "not_ready",
        data_mode="public-demo",
        dataset_available=available,
        generated_fixture_available=available,
    )


@router.get("/status", response_model=StatusResponse, tags=["connectors"])
def connector_status() -> StatusResponse:
    return repository.validated("connectors", StatusResponse)


@router.get("/summary", response_model=SummaryResponse, tags=["analytics"])
def summary(date_from: Optional[date] = None, date_to: Optional[date] = None) -> SummaryResponse:
    result = repository.validated("summary", SummaryResponse)
    if date_from and date_to and date_from > date_to:
        raise HTTPException(status_code=400, detail="date_from must not be after date_to")
    if date_from or date_to:
        result.timeseries = [point for point in result.timeseries if (not date_from or point.date >= date_from) and (not date_to or point.date <= date_to)]
        rows = repository.commerce_period(date_from, date_to)
        if not rows:
            raise HTTPException(status_code=404, detail="No analytics data exists for the requested period")
        measure_names = [
            "sessions", "users", "product_views", "add_to_carts", "begin_checkouts", "purchases",
            "units_sold", "gross_revenue_sar", "discount_sar", "refund_sar", "net_revenue_sar",
            "cost_sar", "ad_spend_sar",
        ]
        totals = {name: sum(float(row[name]) for row in rows) for name in measure_names}
        totals.update({
            "average_order_value_sar": round(totals["net_revenue_sar"] / totals["purchases"], 2),
            "purchase_conversion_rate": round(totals["purchases"] / totals["sessions"], 6),
            "refund_rate": round(totals["refund_sar"] / totals["gross_revenue_sar"], 6),
            "gross_margin_sar": round(totals["net_revenue_sar"] - totals["cost_sar"], 2),
        })
        selected_dates = sorted(date.fromisoformat(row["date"]) for row in rows)
        result.totals = SummaryTotals.model_validate(totals)
        result.period = Period(start=selected_dates[0], end=selected_dates[-1], days=(selected_dates[-1] - selected_dates[0]).days + 1)
    return result


@router.get("/funnel", response_model=FunnelResponse, tags=["analytics"])
def funnel() -> FunnelResponse:
    return repository.validated("funnel", FunnelResponse)


@router.get("/products", response_model=ProductsResponse, tags=["analytics"])
def products(
    category: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=200),
) -> ProductsResponse:
    result = repository.validated("products", ProductsResponse)
    if category:
        result.items = [item for item in result.items if item.category.casefold() == category.casefold()]
    result.items = result.items[:limit]
    return result


@router.get("/acquisition", response_model=AcquisitionResponse, tags=["analytics"])
def acquisition(
    channel: Optional[str] = None,
    source: Optional[str] = None,
) -> AcquisitionResponse:
    result = repository.validated("acquisition", AcquisitionResponse)
    result.items = [
        item for item in result.items
        if (not channel or item.channel.casefold() == channel.casefold())
        and (not source or item.source.casefold() == source.casefold())
    ]
    return result


@router.get("/seo", response_model=SEOResponse, tags=["analytics"])
def seo(branded: Optional[bool] = None, limit: int = Query(default=50, ge=1, le=200)) -> SEOResponse:
    result = repository.validated("seo", SEOResponse)
    if branded is not None:
        result.items = [item for item in result.items if item.is_branded is branded]
    result.items = result.items[:limit]
    return result


@router.get("/customers", response_model=CustomersResponse, tags=["analytics"])
def customers(customer_type: Optional[str] = Query(default=None, pattern="^(new|returning)$")) -> CustomersResponse:
    result = repository.validated("customers", CustomersResponse)
    if customer_type:
        result.segments = [segment for segment in result.segments if segment.customer_type == customer_type]
    return result


@router.get("/quality", response_model=QualityResponse, tags=["analytics"])
def quality(severity: Optional[str] = None) -> QualityResponse:
    result = repository.validated("quality", QualityResponse)
    if severity:
        result.checks = [check for check in result.checks if check.severity.casefold() == severity.casefold()]
    return result


@router.get("/insights", response_model=InsightsResponse, tags=["analytics"])
def insights(area: Optional[str] = None, limit: int = Query(default=20, ge=1, le=100)) -> InsightsResponse:
    result = repository.validated("insights", InsightsResponse)
    if area:
        result.items = [item for item in result.items if item.area.casefold() == area.casefold()]
    result.items = result.items[:limit]
    return result


app.include_router(router)
app.include_router(router, prefix="/api/v1")
