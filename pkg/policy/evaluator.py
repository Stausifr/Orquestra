"""Policy evaluator."""
from __future__ import annotations

from typing import Dict, List, Tuple


def evaluate_action(policy: Dict, action: str, tags: List[str]) -> Tuple[str, List[str]]:
    """Return decision and missing tags for action."""
    rule = policy["rules"].get(action)
    if not rule:
        return "allow", []
    required = set(rule["required_tags"])
    missing = list(required - set(tags))
    return rule["decision"], missing
