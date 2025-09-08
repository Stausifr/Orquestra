"""Simple secrets wrapper."""
from __future__ import annotations

import os


def get_secret(key: str) -> str:
    val = os.getenv(key, "")
    if not val:
        raise KeyError(f"Missing secret: {key}")
    return val


def redact(value: str) -> str:
    return value[:2] + "***" if value else ""
