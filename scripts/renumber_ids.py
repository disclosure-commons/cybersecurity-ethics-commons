"""
Reads data/cases.json and writes a copy with sequential case IDs.

Run from the repo root:
    python3 scripts/renumber_ids.py

Sorts cases by their existing numeric IDs and assigns IDs starting at 1.
Writes data/cases_renumbered.json, leaving data/cases.json unchanged.
Re-running overwrites data/cases_renumbered.json.
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
