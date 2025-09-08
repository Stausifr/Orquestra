"""Data masking utilities."""
from __future__ import annotations

from typing import Dict, List


def mask_data(policy: Dict, tags: List[str], data: Dict) -> Dict:
    """Mask data fields based on policy tags."""
    masked = {}
    for k, v in data.items():
        if k in tags:
            strategy = policy.get("masking", {}).get(k, "redact")
            masked[k] = "***" if strategy == "redact" else hash(v)
        else:
            masked[k] = v
    return masked
