"""Base connector defining common interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

import os
import requests


class BaseConnector(ABC):
    """Abstract connector with basic HTTP helpers."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or os.getenv("MOCK_BASE_URL", "http://localhost:9000")

    def _get(self, path: str) -> Dict[str, Any]:
        resp = requests.get(f"{self.base_url}{path}", timeout=5)
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        resp = requests.post(f"{self.base_url}{path}", json=payload, timeout=5)
        resp.raise_for_status()
        return resp.json()

    @abstractmethod
    def list_agents(self) -> List[Dict[str, Any]]:
        """Return available agents."""

