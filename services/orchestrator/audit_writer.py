"""Audit log writer for orchestrator."""
from __future__ import annotations

from pkg.audit import AuditLog


def write_event(run_id: str, event: dict) -> None:
    log = AuditLog(run_id)
    log.append(event)
