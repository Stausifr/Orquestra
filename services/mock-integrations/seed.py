"""Seed synthetic data for mock integrations."""
from __future__ import annotations

from app import INCIDENTS


def main() -> None:
    INCIDENTS.clear()
    INCIDENTS.append({"case_id": "C1"})
    print("seeded")


if __name__ == "__main__":
    main()
