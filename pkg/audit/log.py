"""Append-only audit log with hash chaining."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, Iterator

STORAGE_DIR = Path("storage")


class AuditLog:
    """Writes events to JSON file with hash chain."""

    def __init__(self, run_id: str) -> None:
        self.path = STORAGE_DIR / f"{run_id}.json"
        self.prev_hash = ""
        if self.path.exists():
            for entry in self.read():
                self.prev_hash = entry["hash"]

    def append(self, event: Dict) -> None:
        event_json = json.dumps(event, sort_keys=True)
        h = hashlib.sha256((self.prev_hash + event_json).encode()).hexdigest()
        record = {"event": event, "prev": self.prev_hash, "hash": h}
        self.path.parent.mkdir(exist_ok=True)
        with self.path.open("a") as f:
            f.write(json.dumps(record) + "\n")
        self.prev_hash = h

    def read(self) -> Iterator[Dict]:
        if not self.path.exists():
            return iter([])
        with self.path.open() as f:
            for line in f:
                yield json.loads(line)


def verify_chain(path: str | Path) -> bool:
    prev = ""
    with open(path) as f:
        for line in f:
            record = json.loads(line)
            event_json = json.dumps(record["event"], sort_keys=True)
            h = hashlib.sha256((prev + event_json).encode()).hexdigest()
            if h != record["hash"]:
                return False
            prev = h
    return True
