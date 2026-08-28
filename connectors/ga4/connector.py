from pathlib import Path
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from connectors.base import FileFallbackConnector


class GA4Record(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: date
    channel: str; source: str; medium: str; campaign: str
    device: Literal["mobile", "desktop", "tablet"]
    sessions: int = Field(ge=0); users: int = Field(ge=0)
    product_views: int = Field(ge=0); add_to_carts: int = Field(ge=0)
    begin_checkouts: int = Field(ge=0); purchases: int = Field(ge=0)
    purchase_revenue_sar: float = Field(ge=0)
    consent_state_coverage: float = Field(ge=0, le=1)


class GA4Connector(FileFallbackConnector):
    connector_id = "ga4"
    required_fields = ("date", "sessions", "users", "purchases", "purchase_revenue_sar")
    credential_env = ("GA4_PROPERTY_ID", "GOOGLE_APPLICATION_CREDENTIALS")
    fixture_path = Path(__file__).resolve().parents[2] / "analytics" / "seeds" / "ga4_daily.csv"
    record_model = GA4Record
