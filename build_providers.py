#!/usr/bin/env python3
"""Merge providers/*.json into providers.json.

Each file in providers/ is one provider. The file name without the .json
suffix is the provider id. The file holds that provider's entry: a single
object, or an array of entries when one service exposes several protocols.

Key order follows the current providers.json so a rebuild does not reshuffle
the catalog. Provider files that are not already in the catalog are appended
in alphabetical order. The written file uses two-space indentation and no
trailing newline, matching the catalog Crystal Code already ships.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROVIDERS_DIR = ROOT / "providers"
OUTPUT = ROOT / "providers.json"
JSON_INDENT = 2


def main() -> int:
    paths = sorted(PROVIDERS_DIR.glob("*.json"), key=lambda path: path.name)
    if not paths:
        print("No provider files found in providers/", file=sys.stderr)
        return 1

    catalog = {path.stem: load_provider(path) for path in paths}
    ordered = order_names(set(catalog))
    catalog = {name: catalog[name] for name in ordered}
    text = json.dumps(catalog, indent=JSON_INDENT, ensure_ascii=False)
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUTPUT.name} ({len(catalog)} providers)")
    return 0


def load_provider(path: Path) -> dict | list:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"{path.name} is not valid JSON: {error}") from error
    if not isinstance(value, (dict, list)):
        raise SystemExit(f"{path.name} must be a JSON object or array")
    return value


def order_names(names: set[str]) -> list[str]:
    if not OUTPUT.is_file():
        return sorted(names)
    try:
        current = json.loads(OUTPUT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"providers.json is not valid JSON: {error}") from error
    if not isinstance(current, dict):
        raise SystemExit("providers.json must be a JSON object")
    ordered = [name for name in current if name in names]
    ordered.extend(sorted(names.difference(ordered)))
    return ordered


if __name__ == "__main__":
    raise SystemExit(main())
