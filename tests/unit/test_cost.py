from services.orchestrator.cost_engine import calc_cost

def test_cost_calc():
    cost = calc_cost({'cpu_ms': 100})
    assert cost > 0
