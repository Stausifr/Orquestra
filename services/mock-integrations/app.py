from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="Mock Integrations")

INCIDENTS: List[Dict] = []
AGENTS = {
    "servicenow": [{"name": "sn_bot"}],
    "snowflake": [{"name": "sf_worker"}],
    "copilot": [{"name": "copilot"}],
    "salesforce": [{"name": "sf_bot"}]
}

class Incident(BaseModel):
    case_id: str

@app.get("/servicenow/incidents")
def list_incidents():
    return INCIDENTS

@app.get("/servicenow/agents")
def sn_agents():
    return AGENTS["servicenow"]

@app.get("/snowflake/agents")
def sf_agents():
    return AGENTS["snowflake"]

@app.post("/snowflake/query")
def snowflake_query(payload: Dict[str, str]):
    data = {"mrn": "123", "dob": "1990"}
    return {"data": str(data), "tags": ["phi"], "cost": {"cpu_ms": 5}}

@app.get("/copilot/agents")
def copilot_agents():
    return AGENTS["copilot"]

class Summarize(BaseModel):
    text: str

@app.post("/copilot/summarize")
def copilot_summarize(payload: Summarize):
    return {"summary": payload.text[:10], "cost": {"tokens": len(payload.text)}}

@app.get("/salesforce/agents")
def sales_agents():
    return AGENTS["salesforce"]

@app.post("/salesforce/cases/{case_id}/update")
def update_case(case_id: str, payload: Dict[str, str]):
    return {"id": case_id, "status": "updated"}
