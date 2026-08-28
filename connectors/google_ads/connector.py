from pathlib import Path
from datetime import date

from pydantic import BaseModel, ConfigDict, Field
from connectors.base import FileFallbackConnector


class GoogleAdsRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: date
    campaign: str
    sessions: int = Field(ge=0)
    purchases: int = Field(ge=0)
    ad_spend_sar: float = Field(ge=0)


class GoogleAdsConnector(FileFallbackConnector):
    connector_id = "google_ads"
    required_fields = ("date", "campaign", "sessions", "purchases", "ad_spend_sar")
    credential_env = ("GOOGLE_ADS_CUSTOMER_ID", "GOOGLE_ADS_DEVELOPER_TOKEN")
    fixture_path = Path(__file__).resolve().parents[2] / "analytics" / "seeds" / "commerce_daily.csv"
    record_model = GoogleAdsRecord

    def validate_records(self, records):
        paid = [row for row in records if row.get("channel") in {"Paid Search", "Paid Social"}]
        return super().validate_records(paid)
