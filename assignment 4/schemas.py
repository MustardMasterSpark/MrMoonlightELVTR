"""Deterministic checks on generated content. No model involved."""

import re


MAX_SUBTITLE_CHARS = 90
IDEAL_SUBTITLE_CHARS = 60

# Vocabulary that did not exist, or would not be said, in 1978.
ANACHRONISMS = [
    "trauma", "boundaries", "processing", "vibe", "vibes", "toxic", "triggered",
    "anxiety attack", "panic attack", "self-care", "gaslighting", "energy",
    "closure", "coping mechanism", "spiral", "meltdown", "okay boomer",
    "google", "internet", "online", "app", "download", "text me", "selfie",
    "podcast", "screenshot", "wifi", "smartphone", "email",
]

REQUIRED_LINE_COUNT = 10


def validate_lines(payload):
    """Check one trigger's worth of thought lines."""
    errors = []
    lines = payload.get("lines", [])

    if not isinstance(lines, list):
        return ["'lines' is not a list."]
    if len(lines) != REQUIRED_LINE_COUNT:
        errors.append(f"expected {REQUIRED_LINE_COUNT} lines, got {len(lines)}")

    seen = set()
    for index, line in enumerate(lines, 1):
        if not isinstance(line, str) or not line.strip():
            errors.append(f"line {index} is empty")
            continue
        text = line.strip()
        if len(text) > MAX_SUBTITLE_CHARS:
            errors.append(f"line {index} is {len(text)} chars, over the "
                          f"{MAX_SUBTITLE_CHARS} subtitle limit")
        lowered = text.lower()
        for term in ANACHRONISMS:
            # Word boundaries, not substrings. Matching bare substrings flagged
            # "happened" for containing "app", which is the kind of false
            # positive that trains a developer to ignore the checker.
            if re.search(r"\b" + re.escape(term) + r"\b", lowered):
                errors.append(f"line {index} contains anachronism '{term}'")
        key = lowered.rstrip(".!?")
        if key in seen:
            errors.append(f"line {index} duplicates an earlier line")
        seen.add(key)

    return errors


def line_stats(groups):
    """Aggregate stats used in the reports."""
    lengths = [len(l) for g in groups for l in g.get("lines", [])]
    if not lengths:
        return {}
    over = sum(1 for n in lengths if n > IDEAL_SUBTITLE_CHARS)
    return {
        "total_lines": len(lengths),
        "mean_chars": round(sum(lengths) / len(lengths), 1),
        "longest": max(lengths),
        "over_ideal": over,
    }
