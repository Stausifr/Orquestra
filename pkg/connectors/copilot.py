"""Mock Microsoft Copilot connector."""
from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseConnector


class CopilotConnector(BaseConnector):
    """Summarizes text via mock LLM."""

    def list_agents(self) -> List[Dict[str, Any]]:
        return self._get("/copilot/agents")

    def summarize(self, text: str) -> Dict[str, Any]:
        return self._post("/copilot/summarize", {"text": text})
