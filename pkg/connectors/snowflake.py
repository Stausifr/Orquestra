"""Mock Snowflake connector."""
from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseConnector


class SnowflakeConnector(BaseConnector):
    """Executes synthetic queries returning tagged data."""

    def list_agents(self) -> List[Dict[str, Any]]:
        return self._get("/snowflake/agents")

    def query(self, sql: str) -> Dict[str, Any]:
        return self._post("/snowflake/query", {"sql": sql})
