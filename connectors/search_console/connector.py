from pathlib import Path
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from connectors.base import FileFallbackConnector


class SearchConsoleRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: date
    query: str; page: str
    country: str
    device: Literal["mobile", "desktop", "tablet"]
    clicks: int = Field(ge=0); impressions: int = Field(ge=0)
    ctr: float = Field(ge=0, le=1)
    average_position: float = Field(gt=0)
    is_branded: bool


class SearchConsoleConnector(FileFallbackConnector):
    connector_id = "search_console"
    required_fields = ("date", "query", "page", "clicks", "impressions", "ctr", "average_position")
    credential_env = ("GSC_SITE_URL", "GOOGLE_APPLICATION_CREDENTIALS")
    fixture_path = Path(__file__).resolve().parents[2] / "analytics" / "seeds" / "search_console.csv"
    record_model = SearchConsoleRecord
