from pkg.policy import load_policy, evaluate_action
from pathlib import Path

def test_policy_allow():
    policy = load_policy(Path('policies/examples/hipaa.json'))
    decision, missing = evaluate_action(policy, 'copilot.summarize', ['phi'])
    assert decision == 'allow'
    assert missing == []
