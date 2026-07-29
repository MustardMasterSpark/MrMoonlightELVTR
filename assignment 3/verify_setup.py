#!/usr/bin/env python3
"""
Check that the repo transferred intact before running the crew.

Empty or truncated files are the most common setup failure: a folder gets
downloaded file by file, a subdirectory arrives as 0 bytes, and the first
symptom is an unhelpful json.load error four stages into a run.

    python3 verify_setup.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent

# path -> (minimum plausible bytes, is_json)
EXPECTED = {
    "crew.py": (30000, False),
    "parse_script.py": (3000, False),
    "schemas.py": (9000, False),
    "README.md": (10000, False),
    "architecture.mmd": (2000, False),
    "knowledge/canon.json": (4000, True),
    "knowledge/budget.json": (4000, True),
    "SCRIPT.txt": (15000, False),
}

MIN_EVENTS = 200


def main():
    problems = []

    for relative, (minimum, is_json) in EXPECTED.items():
        path = ROOT / relative

        if not path.exists():
            problems.append(f"MISSING   {relative}")
            continue

        size = path.stat().st_size
        if size == 0:
            problems.append(f"EMPTY     {relative} (0 bytes)")
            continue
        if size < minimum:
            problems.append(
                f"TRUNCATED {relative} ({size} bytes, expected at least {minimum})"
            )
            continue

        if is_json:
            try:
                payload = json.loads(path.read_text())
            except json.JSONDecodeError as exc:
                problems.append(f"BAD JSON  {relative} ({exc})")
                continue
            if not isinstance(payload, dict) or not payload:
                problems.append(f"EMPTY     {relative} (parsed to an empty object)")
                continue

        print(f"ok        {relative} ({size:,} bytes)")

    # The script is the crew's whole input, so check it parses to real events.
    script = ROOT / "SCRIPT.txt"
    if script.exists() and script.stat().st_size > 0:
        try:
            sys.path.insert(0, str(ROOT))
            import parse_script
            events = parse_script.parse(script)
            if len(events) < MIN_EVENTS:
                problems.append(
                    f"SHORT     script parsed to only {len(events)} events, "
                    f"expected at least {MIN_EVENTS}"
                )
            else:
                print(f"ok        script parses to {len(events)} events")
        except Exception as exc:
            problems.append(f"UNPARSED  script could not be parsed ({exc})")

    print()
    if problems:
        print("Setup is incomplete:\n")
        for problem in problems:
            print(f"  {problem}")
        print("\nRe-download the files listed above. Anything reported as EMPTY or")
        print("TRUNCATED transferred badly rather than being something you need to write.")
        return 1

    print("Setup looks good. Run: python3 crew.py --dry-run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
