"""Lightweight integrity checks for the C2CAD-Bench release artifact."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "results" / "showcase_db.js"


def main() -> None:
    text = DB_PATH.read_text(encoding="utf-8")
    match = re.search(r"window\.SHOWCASE_DB\s*=\s*(\{.*\});?\s*$", text, re.S)
    if not match:
        raise SystemExit(f"Could not parse {DB_PATH}")

    db = json.loads(match.group(1))
    golden = db.get("golden", [])
    models = db.get("models", {})
    result_count = sum(len(v) for v in models.values())

    print(f"{len(golden)} golden test cases")
    print(f"{len(models)} models")
    print(f"{result_count} model-case results")

    expected = (75, 13, 975)
    actual = (len(golden), len(models), result_count)
    if actual != expected:
        raise SystemExit(f"Unexpected artifact size: expected {expected}, got {actual}")


if __name__ == "__main__":
    main()
