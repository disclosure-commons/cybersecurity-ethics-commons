"""
Renumbers the case IDs in data/cases.json.

Run from the repo root:
    python3 scripts/renumber.py

Renumbers the case IDs in data/cases.json. Safe to re-run any time data/cases.json changes.
"""

import json
from pathlib import Path

with Path("data/cases.json").open("r", encoding="utf-8") as f:
    data = json.load(f)

# Sort cases by their existing IDs
data["cases"].sort(key=lambda case: int(case["id"]))

# Assign sequential IDs starting from 1
for new_id, case in enumerate(data["cases"], start=1):
    case["id"] = new_id

# Write to a separate file to preserve the original
output = Path("data/cases_renumbered.json")

with output.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Renumbered {len(data['cases'])} cases.")
print(f"Saved to {output}")