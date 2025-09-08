"""Refresh agent registry."""
from __future__ import annotations

import datetime as dt

from pkg.connectors import (
    CopilotConnector,
    SalesforceConnector,
    ServiceNowConnector,
    SnowflakeConnector,
)
from services.orchestrator.models import Agent, get_session


def refresh() -> None:
    connectors = {
        "servicenow": ServiceNowConnector(),
        "snowflake": SnowflakeConnector(),
        "copilot": CopilotConnector(),
        "salesforce": SalesforceConnector(),
    }
    with get_session() as session:
        for provider, conn in connectors.items():
            for agent in conn.list_agents():
                record = session.query(Agent).filter_by(provider=provider, name=agent["name"]).first()
                if not record:
                    record = Agent(provider=provider, name=agent["name"])
                    session.add(record)
                record.last_refreshed = dt.datetime.utcnow()
        session.commit()
