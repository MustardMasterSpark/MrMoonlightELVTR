"""
Deterministic pre-pass. No model is called anywhere in this file.

SCRIPT.txt has the form:

    SCENE 01 — WAKING AT THE CAMPSITE
    EVT-001 | VFX | The screen is completely black.

Splitting that into records is a regex problem, not a judgment problem, so it
happens in Python. Every token an LLM spends counting pipe characters is a token
it is not spending on the work only a model can do.

Produces two artifacts:
  00_events.json     every event as a record, tagged with its scene
  subtitles.json     the dialogue and thought table, ready for a subtitle system
"""

import json
import re
from pathlib import Path

EVENT_RE = re.compile(r"^(EVT-\d+)\s*\|\s*([A-Z:]+)\s*\|\s*(.*)$")
SCENE_RE = re.compile(r"^SCENE\s+(\d+)\s+[—-]\s+(.*)$")

SPEAKERS = {"DIALOGUE:T": "Tracey", "DIALOGUE:R": "Rylee", "THOUGHT:T": "Tracey"}

# Event types that describe something the player hears, sees or does, and
# therefore imply production work. NOTE is excluded: it is a memo to the author.
PRODUCTION_TYPES = {
    "ACTION", "SYSTEM", "ANIMATION", "CUTSCENE:BLOCKING", "VFX", "SFX",
    "MESSAGE", "DIALOGUE:T", "DIALOGUE:R", "THOUGHT:T",
    "OBJECTIVE:START", "OBJECTIVE:UPDATE", "OBJECTIVE:END", "OUTLINE",
}


def parse(script_path):
    events = []
    scene_number, scene_title, scene_is_outline = 0, "Front matter", False
    in_body = False

    for raw in Path(script_path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()

        scene_match = SCENE_RE.match(line)
        if scene_match:
            in_body = True
            scene_number = int(scene_match.group(1))
            scene_title = scene_match.group(2).replace("[OUTLINE]", "").strip()
            scene_is_outline = "[OUTLINE]" in scene_match.group(2)
            continue

        event_match = EVENT_RE.match(line)
        if not event_match or not in_body:
            continue

        event_id, event_type, content = event_match.groups()
        events.append({
            "event_id": event_id,
            "event_type": event_type,
            "content": content.strip(),
            "scene_number": scene_number,
            "scene_title": scene_title,
            "scene_is_outline": scene_is_outline,
            "implies_production_work": event_type in PRODUCTION_TYPES,
        })

    return events


def extract_subtitles(events):
    """Pull spoken lines and on-screen thoughts into a localisable table.

    Quoted text becomes the subtitle. Unquoted text is a stage direction the
    author wrote in place of a final line, so it is flagged rather than shipped.
    """
    rows = []
    for event in events:
        if event["event_type"] not in SPEAKERS:
            continue
        quoted = re.findall(r'"([^"]+)"', event["content"])
        rows.append({
            "key": event["event_id"],
            "speaker": SPEAKERS[event["event_type"]],
            "delivery": "on_screen_text" if event["event_type"].startswith("THOUGHT") else "voiced",
            "line": quoted[0] if quoted else "",
            "direction": event["content"] if not quoted else
                         event["content"].split('"')[-1].strip() or None,
            "needs_writing": not quoted,
            "scene_number": event["scene_number"],
        })
    return rows


def summarise(events):
    by_type, by_scene, outline_scenes = {}, {}, []
    for event in events:
        by_type[event["event_type"]] = by_type.get(event["event_type"], 0) + 1
        key = f"{event['scene_number']:02d} {event['scene_title']}"
        by_scene[key] = by_scene.get(key, 0) + 1
        if event["scene_is_outline"] and key not in outline_scenes:
            outline_scenes.append(key)
    return {
        "total_events": len(events),
        "scene_count": len({e["scene_number"] for e in events}),
        "events_by_type": dict(sorted(by_type.items(), key=lambda kv: -kv[1])),
        "events_by_scene": by_scene,
        "unfinished_scenes": outline_scenes,
    }


def scenes(events):
    """Group events by scene so agents can be called one scene at a time."""
    grouped = {}
    for event in events:
        grouped.setdefault(event["scene_number"], []).append(event)
    return dict(sorted(grouped.items()))


if __name__ == "__main__":
    import sys
    parsed = parse(sys.argv[1] if len(sys.argv) > 1
                   else Path(__file__).parent / "SCRIPT.txt")
    print(json.dumps(summarise(parsed), indent=2))
