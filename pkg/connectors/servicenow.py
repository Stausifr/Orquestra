"""Mock ServiceNow connector."""
from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseConnector


class ServiceNowConnector(BaseConnector):
    """Connector for ServiceNow incidents and agents."""

    def list_agents(self) -> List[Dict[str, Any]]:
        return self._get("/servicenow/agents")

    def list_incidents(self) -> List[Dict[str, Any]]:
        return self._get("/servicenow/incidents")
