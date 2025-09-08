"""Policy engine integration."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from pkg.policy import evaluate_action, load_policy, mask_data

POLICY_DIR = Path("policies/examples")

loaded_policies: Dict[str, Dict] = {}


def load_all() -> None:
    for path in POLICY_DIR.glob("*.json"):
        loaded_policies[path.name] = load_policy(path)


def evaluate(action: str, tags: List[str]) -> str:
    for policy in loaded_policies.values():
        decision, missing = evaluate_action(policy, action, tags)
        if decision == "deny" or decision == "require_approval":
            return decision
    return "allow"


def mask(policy_name: str, tags: List[str], data: Dict) -> Dict:
    policy = loaded_policies[policy_name]
    return mask_data(policy, tags, data)
