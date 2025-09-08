"""FastAPI application for Orquestra orchestrator."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import Dict, List
import json
import asyncio

from pkg.audit import verify_chain
from .models import Agent, Approval, Workflow, get_session
from . import policy_engine
from .workflow_runner import continue_workflow, run_workflow
from .audit_writer import write_event

app = FastAPI(title="Orquestra Orchestrator")
policy_engine.load_all()
TOKENS: Dict[str, str] = {}
PENDING_INCIDENTS: Dict[int, Dict] = {}


class AuthPayload(BaseModel):
    token: str


@app.post("/connectors/{provider}/auth")
def auth(provider: str, payload: AuthPayload) -> Dict[str, str]:
    TOKENS[provider] = payload.token
    return {"status": "ok"}


@app.get("/agents")
def agents() -> List[Dict]:
    with get_session() as session:
        return [
            {"id": a.id, "provider": a.provider, "name": a.name, "last_refreshed": a.last_refreshed}
            for a in session.query(Agent).all()
        ]


class PolicyPath(BaseModel):
    path: str


@app.post("/policies/load")
def load_policy(payload: PolicyPath) -> Dict[str, str]:
    policy_engine.load_all()
    return {"status": "reloaded"}


@app.get("/policies")
def list_policies() -> List[str]:
    return list(policy_engine.loaded_policies.keys())


class Incident(BaseModel):
    case_id: str


@app.post("/incidents/simulate")
def simulate_incident(inc: Incident) -> Dict[str, int]:
    run_id = run_workflow(inc.dict())
    if run_id:
        PENDING_INCIDENTS[run_id] = inc.dict()
    return {"workflow_id": run_id}


@app.get("/workflows/{run_id}")
def get_workflow(run_id: int) -> Dict:
    with get_session() as session:
        wf = session.get(Workflow, run_id)
        if not wf:
            raise HTTPException(404)
        costs = session.query(Agent).count()
        return {"id": wf.id, "status": wf.status, "costs": costs}


@app.get("/approvals/pending")
def approvals_pending() -> List[Dict]:
    with get_session() as session:
        return [
            {"id": a.id, "workflow_id": a.workflow_id, "reason": a.reason}
            for a in session.query(Approval).filter_by(status="pending")
        ]


@app.post("/approvals/{approval_id}/{action}")
def handle_approval(approval_id: int, action: str) -> Dict[str, str]:
    with get_session() as session:
        approval = session.get(Approval, approval_id)
        if not approval:
            raise HTTPException(404)
        approval.status = action
        workflow_id = approval.workflow_id
        session.commit()
    if action == "approve":
        incident = PENDING_INCIDENTS.get(workflow_id)
        continue_workflow(workflow_id, incident)
        with get_session() as session:
            wf = session.get(Workflow, workflow_id)
            if wf:
                wf.status = "completed"
                session.commit()
    return {"status": action}


@app.get("/audit/{run_id}.json")
def audit_json(run_id: int) -> FileResponse:
    path = f"storage/{run_id}.json"
    if not verify_chain(path):
        raise HTTPException(400, "corrupted")
    return FileResponse(path)


@app.get("/audit/{run_id}.pdf")
def audit_pdf(run_id: int) -> FileResponse:
    path = f"storage/{run_id}.pdf"
    # PDF generation stub
    with open(path, "w") as f:
        f.write("audit report")
    return FileResponse(path)


@app.get("/metrics/live")
async def metrics_live():
    async def event_stream():
        for i in range(5):
            yield f"data: {json.dumps({'tick': i})}\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(event_stream(), media_type="text/event-stream")
