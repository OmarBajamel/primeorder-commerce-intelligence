"""Validated access to generated public-demo JSON artifacts."""

from __future__ import annotations

import csv
import json
from functools import lru_cache
from pathlib import Path
from datetime import date
from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_DIR = ROOT / "data" / "public-demo" / "api"
ModelT = TypeVar("ModelT", bound=BaseModel)


class PublicDemoRepository:
    def __init__(self, data_dir: Path = DEFAULT_DATA_DIR):
        self.data_dir = data_dir

    def exists(self) -> bool:
        required = {"summary", "funnel", "products", "acquisition", "seo", "customers", "quality", "insights", "connectors"}
        return all((self.data_dir / f"{name}.json").is_file() for name in required)

    @lru_cache(maxsize=32)
    def read(self, name: str) -> Dict[str, Any]:
        if not name.replace("_", "").isalnum():
            raise ValueError("Invalid public artifact name")
        path = self.data_dir / f"{name}.json"
        if not path.is_file():
            raise FileNotFoundError(f"Generated public artifact is unavailable: {name}")
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"Generated public artifact must be a JSON object: {name}")
        return value

    def validated(self, name: str, model: Type[ModelT]) -> ModelT:
        return model.model_validate(self.read(name))

    @lru_cache(maxsize=8)
    def fixture_rows(self, name: str) -> List[Dict[str, str]]:
        if name not in {"commerce_daily", "ga4_daily", "google_ads_daily"}:
            raise ValueError("Fixture is not exposed through the API repository")
        path = self.data_dir.parent / f"{name}.csv"
        if not path.is_file():
            raise FileNotFoundError(f"Generated {name} fixture is unavailable")
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    def fixture_period(self, name: str, date_from: Optional[date], date_to: Optional[date]) -> List[Dict[str, str]]:
        return [
            row for row in self.fixture_rows(name)
            if (not date_from or date.fromisoformat(row["date"]) >= date_from)
            and (not date_to or date.fromisoformat(row["date"]) <= date_to)
        ]
