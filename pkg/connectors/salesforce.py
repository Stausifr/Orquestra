"""Mock Salesforce connector."""
from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseConnector


class SalesforceConnector(BaseConnector):
    """Updates cases in Salesforce."""

    def list_agents(self) -> List[Dict[str, Any]]:
        return self._get("/salesforce/agents")

    def update_case(self, case_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._post(f"/salesforce/cases/{case_id}/update", payload)
