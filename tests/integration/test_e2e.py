from fastapi.testclient import TestClient
from services.orchestrator.app import app
from services.orchestrator.models import get_session, Workflow
from pkg.connectors import SnowflakeConnector, CopilotConnector, SalesforceConnector

client = TestClient(app)


def fake_query(self, sql):
    return {"data": "", "tags": ["phi"], "cost": {"cpu_ms": 1}}


def fake_summarize(self, text):
    return {"summary": "ok", "cost": {"tokens": 1}}


def fake_update(self, case_id, payload):
    return {"id": case_id}


SnowflakeConnector.query = fake_query
CopilotConnector.summarize = fake_summarize
SalesforceConnector.update_case = fake_update


def test_end_to_end():
    resp = client.post('/incidents/simulate', json={'case_id': 'C1'})
    run_id = resp.json()['workflow_id']
    resp = client.get('/approvals/pending')
    approval = [a for a in resp.json() if a['workflow_id'] == run_id][0]
    client.post(f"/approvals/{approval['id']}/approve")
    with get_session() as session:
        wf = session.get(Workflow, run_id)
        assert wf.status == 'completed'
