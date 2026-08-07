#!/usr/bin/env python3
"""Check the package transferred intact before running anything."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).parent
EXPECTED = {
    "forge.py": 25000, "kb.py": 7000, "schemas.py": 1500,
    "README.md": 8000, "knowledge/GDD.md": 25000, "knowledge/L01.txt": 40000,
}
problems = []
for rel, minimum in EXPECTED.items():
    p = ROOT / rel
    if not p.exists():
        problems.append(f"MISSING   {rel}")
    elif p.stat().st_size == 0:
        problems.append(f"EMPTY     {rel} (0 bytes)")
    elif p.stat().st_size < minimum:
        problems.append(f"TRUNCATED {rel} ({p.stat().st_size} bytes, expected {minimum}+)")
    else:
        print(f"ok        {rel} ({p.stat().st_size:,} bytes)")

try:
    sys.path.insert(0, str(ROOT))
    import kb
    stats = kb.KnowledgeBase(ROOT / "knowledge").stats()
    if stats["total_chunks"] < 50:
        problems.append(f"SHORT     index built only {stats['total_chunks']} chunks")
    else:
        print(f"ok        knowledge base indexes {stats['total_chunks']} chunks "
              f"({stats['gdd_chunks']} GDD, {stats['script_chunks']} script)")
except Exception as exc:
    problems.append(f"FAILED    could not build the index ({exc})")

print()
if problems:
    print("Setup is incomplete:\n")
    for p in problems:
        print("  " + p)
    sys.exit(1)
print("Setup looks good. Run: python3 forge.py --dry-run")
