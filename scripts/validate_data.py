#!/usr/bin/env python3
"""Validate the case dataset without changing any files."""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "cases.json"
SCHEMA = ROOT / "schema" / "cases.schema.json"


def describe_path(data, path):
    parts = list(path)
    location = "$" + "".join(
        f"[{part}]" if isinstance(part, int) else f".{part}" for part in parts
    )
    if parts[:1] == ["cases"] and len(parts) > 1 and isinstance(parts[1], int):
        case = data["cases"][parts[1]]
        if isinstance(case, dict) and type(case.get("id")) is int:
            return f"case {case['id']} ({location})"
    return location


def is_http_url(value):
    if re.search(r'[\s\x00-\x1f\x7f\\<>"{}`|^]|%(?![0-9a-fA-F]{2})', value):
        return False
    try:
        parsed = urlsplit(value)
        # Accessing port also rejects invalid and out-of-range port numbers.
        parsed.port
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname)
    except ValueError:
        return False


def validate_data(data):
    """Return validation diagnostics for an already-decoded dataset."""
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = [
        f"{describe_path(data, error.absolute_path)}: {error.message}"
        for error in validator.iter_errors(data)
    ]
    if errors:
        return errors

    categories = set()
    for index, category in enumerate(data["categories"]):
        name = category["name"]
        if name in categories:
            errors.append(f"$.categories[{index}].name: duplicate category {name!r}")
        categories.add(name)

    for index, case in enumerate(data["cases"]):
        cid = case["id"]
        location = f"case {cid!r} ($.cases[{index}])"
        if type(cid) is not int or cid != index + 1:
            errors.append(f"{location}.id: expected JSON integer {index + 1}, got {cid!r}")
        if case["category"] not in categories:
            errors.append(f"{location}.category: {case['category']!r} is not declared in categories")
        for tag_index, tag in enumerate(case.get("tags", [])):
            if tag not in categories:
                errors.append(f"{location}.tags[{tag_index}]: {tag!r} is not declared in categories")
        if not is_http_url(case["source"]):
            errors.append(f"{location}.source: expected a valid HTTP(S) URL with a hostname")
        for source_index, source in enumerate(case.get("extra_sources", [])):
            if not is_http_url(source["url"]):
                errors.append(
                    f"{location}.extra_sources[{source_index}].url: "
                    "expected a valid HTTP(S) URL with a hostname"
                )
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", nargs="?", type=Path, default=DATA)
    args = parser.parse_args()
    try:
        data = json.loads(args.dataset.read_text(encoding="utf-8"))
        errors = validate_data(data)
    except (OSError, ValueError) as error:
        print(f"{args.dataset}: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"{args.dataset}: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(data['cases'])} cases in {args.dataset}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
