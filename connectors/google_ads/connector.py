from pathlib import Path
from datetime import date

from pydantic import BaseModel, ConfigDict, Field
from connectors.base import FileFallbackConnector


class GoogleAdsRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: date
    campaign: str
    channel: str
    source: str
    medium: str
    clicks: int = Field(ge=0)
    conversions: float = Field(ge=0)
    conversion_value_sar: float = Field(ge=0)
    ad_spend_sar: float = Field(ge=0)


class GoogleAdsConnector(FileFallbackConnector):
    connector_id = "google_ads"
    required_fields = ("date", "campaign", "clicks", "conversions", "conversion_value_sar", "ad_spend_sar")
    credential_env = ("GOOGLE_ADS_CUSTOMER_ID", "GOOGLE_ADS_DEVELOPER_TOKEN")
    fixture_path = Path(__file__).resolve().parents[2] / "analytics" / "seeds" / "google_ads_daily.csv"
    record_model = GoogleAdsRecord
