from pathlib import Path
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from connectors.base import FileFallbackConnector


class ClarityRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: date
    device: Literal["mobile", "desktop", "tablet"]
    country: str
    sessions: int = Field(ge=0)
    dead_clicks: int = Field(ge=0); rage_clicks: int = Field(ge=0)
    excessive_scrolls: int = Field(ge=0); javascript_errors: int = Field(ge=0)


class ClarityConnector(FileFallbackConnector):
    connector_id = "clarity"
    required_fields = ("date", "sessions", "dead_clicks", "rage_clicks", "excessive_scrolls")
    credential_env = ("CLARITY_PROJECT_ID", "CLARITY_API_TOKEN")
    fixture_path = Path(__file__).resolve().parents[2] / "analytics" / "seeds" / "clarity_daily.csv"
    record_model = ClarityRecord
