"""Execute orchestration steps for incidents."""
from __future__ import annotations

from typing import Dict

from services.orchestrator.workflow_runner import run_workflow


def execute(incident: Dict) -> int:
    return run_workflow(incident)
