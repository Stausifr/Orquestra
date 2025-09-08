from services.orchestrator.workflow_runner import run_workflow, continue_workflow
from services.orchestrator.models import Approval, Workflow, get_session
from pkg.connectors import SnowflakeConnector, CopilotConnector, SalesforceConnector


def fake_query(self, sql):
    return {"data": "", "tags": ["phi"], "cost": {"cpu_ms": 1}}


def fake_summarize(self, text):
    return {"summary": "ok", "cost": {"tokens": 1}}


def fake_update(self, case_id, payload):
    return {"id": case_id}


SnowflakeConnector.query = fake_query
CopilotConnector.summarize = fake_summarize
SalesforceConnector.update_case = fake_update


def test_workflow_approval_and_completion():
    run_id = run_workflow({'case_id': 'C1'})
    with get_session() as session:
        approval = session.query(Approval).filter_by(workflow_id=run_id).first()
        assert approval and approval.status == 'pending'
    continue_workflow(run_id, {'case_id': 'C1'})
    with get_session() as session:
        wf = session.get(Workflow, run_id)
        assert wf.status == 'completed'
