"""Incident poller consuming mock ServiceNow API."""
from __future__ import annotations

from pkg.connectors import ServiceNowConnector
from services.orchestrator.workflow_runner import run_workflow


def poll_once() -> None:
    sn = ServiceNowConnector()
    for inc in sn.list_incidents():
        run_workflow(inc)
