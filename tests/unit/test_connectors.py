from pkg.connectors import ServiceNowConnector

def test_servicenow_list_agents(monkeypatch):
    sn = ServiceNowConnector(base_url='')
    monkeypatch.setattr(sn, '_get', lambda path: [{'name': 'bot'}])
    agents = sn.list_agents()
    assert agents[0]['name'] == 'bot'
