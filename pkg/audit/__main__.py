"""CLI for audit log verification."""
from __future__ import annotations

import argparse
from .log import verify_chain


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_id")
    args = parser.parse_args()
    path = f"storage/{args.run_id}.json"
    ok = verify_chain(path)
    print("OK" if ok else "CORRUPTED")


if __name__ == "__main__":
    main()
