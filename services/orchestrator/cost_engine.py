"""Cost calculation utilities."""
from __future__ import annotations

from typing import Dict

RATES = {"cpu_ms": 0.00001, "api_ms": 0.00002, "tokens": 0.000001, "data_scanned_mb": 0.0001}


def calc_cost(metrics: Dict[str, float]) -> float:
    return sum(metrics.get(k, 0) * v for k, v in RATES.items())
