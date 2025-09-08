"""Load and validate policy packs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import jsonschema

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "policies" / "schema.json"

with SCHEMA_PATH.open() as f:
    POLICY_SCHEMA = json.load(f)


def load_policy(path: str | Path) -> Dict[str, Any]:
    """Load a policy JSON file and validate against schema."""
    with open(path) as f:
        data = json.load(f)
    jsonschema.validate(data, POLICY_SCHEMA)
    return data
