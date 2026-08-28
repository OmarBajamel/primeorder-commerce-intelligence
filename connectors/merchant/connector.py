from pathlib import Path
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from connectors.base import FileFallbackConnector


class MerchantRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    date: date
    product_id: str
    destination: str
    status: Literal["approved", "disapproved"]
    issue_code: str
    affected_items: int = Field(ge=0)


class MerchantConnector(FileFallbackConnector):
    connector_id = "merchant"
    required_fields = ("date", "product_id", "destination", "status", "affected_items")
    credential_env = ("MERCHANT_ACCOUNT_ID", "GOOGLE_APPLICATION_CREDENTIALS")
    fixture_path = Path(__file__).resolve().parents[2] / "analytics" / "seeds" / "merchant_diagnostics.csv"
    record_model = MerchantRecord
