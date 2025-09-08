"""Workflow runner implementation."""
from __future__ import annotations

from typing import Dict

from pkg.connectors import CopilotConnector, SalesforceConnector, SnowflakeConnector

from . import policy_engine
from .audit_writer import write_event
from .cost_engine import calc_cost
from .models import Approval, CostRecord, Workflow, get_session
from .otel import span


def run_workflow(incident: Dict) -> int:
    """Execute workflow for an incident. Returns workflow id."""
    snow = SnowflakeConnector()
    cop = CopilotConnector()
    sales = SalesforceConnector()

    with get_session() as session:
        wf = Workflow()
        session.add(wf)
        session.commit()
        run_id = wf.id

        with span("snowflake.query"):
            result = snow.query("select * from table")
            tags = result.get("tags", [])
            decision = policy_engine.evaluate("snowflake.query", tags)
            write_event(run_id, {"step": "snowflake.query", "decision": decision})
            if decision == "require_approval":
                approval = Approval(workflow_id=run_id, status="pending", reason="phi data")
                session.add(approval)
                session.commit()
                return run_id
        cost = calc_cost(result.get("cost", {}))
        session.add(CostRecord(workflow_id=run_id, step="snowflake.query", cost=cost))

        with span("copilot.summarize"):
            summary = cop.summarize(result.get("data", ""))
            cost = calc_cost(summary.get("cost", {}))
            session.add(CostRecord(workflow_id=run_id, step="copilot.summarize", cost=cost))
            write_event(run_id, {"step": "copilot.summarize"})

        with span("salesforce.update"):
            sales.update_case(incident["case_id"], {"summary": summary["summary"]})
            write_event(run_id, {"step": "salesforce.update"})
            cost = calc_cost({})
            session.add(CostRecord(workflow_id=run_id, step="salesforce.update", cost=cost))

        wf.status = "completed"
        session.commit()
        return run_id


def continue_workflow(run_id: int, incident: Dict | None = None) -> None:
    """Continue a paused workflow after approval."""
    snow = SnowflakeConnector()
    cop = CopilotConnector()
    sales = SalesforceConnector()
    case_id = incident.get("case_id") if incident else ""
    with get_session() as session:
        result = snow.query("select * from table")
        cost = calc_cost(result.get("cost", {}))
        session.add(CostRecord(workflow_id=run_id, step="snowflake.query", cost=cost))
        summary = cop.summarize(result.get("data", ""))
        cost = calc_cost(summary.get("cost", {}))
        session.add(CostRecord(workflow_id=run_id, step="copilot.summarize", cost=cost))
        sales.update_case(case_id, {"summary": summary["summary"]})
        session.add(CostRecord(workflow_id=run_id, step="salesforce.update", cost=0))
        wf = session.get(Workflow, run_id)
        wf.status = "completed"
        session.commit()
