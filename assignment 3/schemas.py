"""
Schemas for the four crew artifacts, plus two deterministic gates.

Neither gate calls a model. Gate 1 checks record shape: required keys, types,
enum membership. Gate 2 checks the objective graph against the parsed script:
every objective that opens must close, and every event a stage cites must
actually exist in the source with the type the stage claims.

Both are things Python does exactly and an LLM does approximately, so both live
here rather than in an agent prompt.
"""

REQUIREMENT_KINDS = [
    "model", "animation", "sfx", "vfx", "ui_message",
    "prop", "environment", "mechanic", "system",
]

BUDGET_STATUS = ["budgeted", "partial", "unbudgeted"]

SEVERITIES = ["BLOCKER", "WARNING", "NOTE"]

RIG_TARGETS = [
    "first_person_hands",   # Tracey's arms and hands in camera space
    "player_full_body",     # visible-body moments: vomiting, dropping to knees
    "humanoid_npc",         # Rylee, Vernon, Holly, Scott, cultists
    "quadruped",            # wolves
    "creature",             # Furman, totems
    "prop",                 # tent flaps, doors, telescope, RV rug
    "camera",               # shakes, blurs, forced looks
]

CAPTURE_METHODS = [
    "mocap_video",      # GoPro POV plus DeepMotion or QuickMagic
    "hand_keyed",        # authored in Blender
    "procedural",        # driven by code, no clip
    "asset_package",     # already present in the purchased FPS package
]

PLAYBACK_MODES = ["one_shot", "loop", "additive"]

UNLOCKABLE_SYSTEMS = [
    "camera_look", "player_movement", "stamina_bar", "inventory_capacity",
    "map_and_compass", "sprint", "melee_weapon", "firearm", "light_source",
    "fear_state", "objective_ui", "drug_system", "escort",
]

# spec: {field: (type, constraint)}  constraint = None | (lo, hi) | [allowed...]
REQUIREMENT_SPEC = {
    "event_id": (str, None),
    "kind": (str, REQUIREMENT_KINDS),
    "name": (str, None),
    "detail": (str, None),
}

EVENT_LABEL_SPEC = {
    "event_id": (str, None),
    "label": (str, None),
}

ASSET_SPEC = {
    "asset_id": (str, "snake_case"),
    "name": (str, None),
    "kind": (str, REQUIREMENT_KINDS),
    "event_ids": (list, None),
    "budget_status": (str, BUDGET_STATUS),
    "budget_ref": (str, None),
    "notes": (str, None),
}

OBJECTIVE_SPEC = {
    "objective_id": (str, "snake_case"),
    "label": (str, None),
    "start_event": (str, None),
    "end_event": (str, None),
    "update_events": (list, None),
    "required_asset_ids": (list, None),
}

UNLOCK_SPEC = {
    "system": (str, UNLOCKABLE_SYSTEMS),
    "event_id": (str, None),
    "note": (str, None),
}

ANIMATION_SPEC = {
    "animation_id": (str, "snake_case"),
    "name": (str, None),
    "source_asset_id": (str, "snake_case"),
    "event_ids": (list, None),
    "rig_target": (str, RIG_TARGETS),
    "capture_method": (str, CAPTURE_METHODS),
    "playback": (str, PLAYBACK_MODES),
    "blocks_player_control": (bool, None),
    "needs_animation_event": (bool, None),
    "approx_duration_sec": (float, (0.1, 120.0)),
    "capture_session": (str, "snake_case"),
    "notes": (str, None),
}

CAPTURE_SESSION_SPEC = {
    "session_id": (str, "snake_case"),
    "description": (str, None),
    "rig_target": (str, RIG_TARGETS),
    "capture_method": (str, CAPTURE_METHODS),
    "animation_ids": (list, None),
}

FINDING_SPEC = {
    "severity": (str, SEVERITIES),
    "category": (str, None),
    "subject": (str, None),
    "evidence_events": (list, None),
    "issue": (str, None),
    "recommendation": (str, None),
}

ARTIFACTS = {
    "01_requirements": {"requirements": REQUIREMENT_SPEC,
                        "event_labels": EVENT_LABEL_SPEC},
    "02_asset_manifest": {"assets": ASSET_SPEC},
    "03_animation_list": {"animations": ANIMATION_SPEC,
                          "capture_sessions": CAPTURE_SESSION_SPEC},
    "04_runtime_data": {"objectives": OBJECTIVE_SPEC, "unlocks": UNLOCK_SPEC},
    "05_gap_report": {"findings": FINDING_SPEC},
}


def _is_snake_case(value):
    return bool(value) and all(c.islower() or c.isdigit() or c == "_" for c in value)


def _check_record(record, spec, label):
    errors = []
    if not isinstance(record, dict):
        return [f"{label} must be an object, got {type(record).__name__}."]
    for field, (expected, constraint) in spec.items():
        if field not in record:
            errors.append(f"{label} is missing '{field}'.")
            continue
        value = record[field]
        if not isinstance(value, expected):
            errors.append(f"{label}.{field} must be {expected.__name__}, got {type(value).__name__}.")
            continue
        if constraint == "snake_case" and not _is_snake_case(value):
            errors.append(f"{label}.{field} must be snake_case, got '{value}'.")
        elif isinstance(constraint, list) and value not in constraint:
            errors.append(f"{label}.{field} = '{value}' is not one of {constraint}.")
        elif isinstance(constraint, tuple) and not constraint[0] <= value <= constraint[1]:
            errors.append(f"{label}.{field} = {value} is outside {constraint}.")
        if expected is str and not value.strip():
            errors.append(f"{label}.{field} must not be empty.")
    return errors


def validate_artifact(artifact_key, payload, max_reported=25):
    """Gate 1. Returns a list of error strings; empty means valid."""
    specs = ARTIFACTS[artifact_key]
    errors = []
    if not isinstance(payload, dict):
        return [f"{artifact_key} must be a JSON object."]

    for collection, spec in specs.items():
        if collection not in payload:
            errors.append(f"{artifact_key} is missing the '{collection}' array.")
            continue
        records = payload[collection]
        if not isinstance(records, list):
            errors.append(f"{artifact_key}.{collection} must be an array.")
            continue
        if not records:
            errors.append(f"{artifact_key}.{collection} is empty.")
            continue
        for index, record in enumerate(records):
            errors.extend(_check_record(record, spec, f"{collection}[{index}]"))

    if len(errors) > max_reported:
        remaining = len(errors) - max_reported
        errors = errors[:max_reported] + [f"... and {remaining} further error(s)."]
    return errors


def validate_objective_graph(events, runtime_data):
    """Gate 2. Cross-checks the objective graph against the parsed script."""
    errors = []
    by_id = {e["event_id"]: e for e in events}

    script_starts = {e["event_id"] for e in events if e["event_type"] == "OBJECTIVE:START"}
    script_ends = {e["event_id"] for e in events if e["event_type"] == "OBJECTIVE:END"}
    script_updates = {e["event_id"] for e in events if e["event_type"] == "OBJECTIVE:UPDATE"}

    claimed_starts, claimed_ends, claimed_updates = set(), set(), set()

    for objective in runtime_data.get("objectives", []):
        oid = objective.get("objective_id", "?")

        for field, pool, label in (
            ("start_event", script_starts, "OBJECTIVE:START"),
            ("end_event", script_ends, "OBJECTIVE:END"),
        ):
            ref = objective.get(field)
            if not ref:
                continue
            if ref not in by_id:
                errors.append(f"Objective '{oid}' cites {field}={ref}, which is not in the script.")
            elif ref not in pool:
                errors.append(
                    f"Objective '{oid}' cites {field}={ref}, but that event is "
                    f"{by_id[ref]['event_type']}, not {label}."
                )
            else:
                (claimed_starts if field == "start_event" else claimed_ends).add(ref)

        if not objective.get("end_event"):
            errors.append(f"Objective '{oid}' never closes: no end_event.")

        for ref in objective.get("update_events", []) or []:
            if ref not in by_id:
                errors.append(f"Objective '{oid}' cites update {ref}, which is not in the script.")
            elif ref not in script_updates:
                errors.append(
                    f"Objective '{oid}' cites update {ref}, but that event is "
                    f"{by_id[ref]['event_type']}, not OBJECTIVE:UPDATE."
                )
            else:
                claimed_updates.add(ref)

    for orphan in sorted(script_starts - claimed_starts):
        errors.append(f"Script event {orphan} is an OBJECTIVE:START that no objective claims.")
    for orphan in sorted(script_ends - claimed_ends):
        errors.append(f"Script event {orphan} is an OBJECTIVE:END that no objective claims.")
    for orphan in sorted(script_updates - claimed_updates):
        errors.append(f"Script event {orphan} is an OBJECTIVE:UPDATE that no objective claims.")

    for unlock in runtime_data.get("unlocks", []):
        ref = unlock.get("event_id")
        if ref and ref not in by_id:
            errors.append(
                f"Unlock '{unlock.get('system')}' cites {ref}, which is not in the script."
            )

    return errors


def animation_assets(manifest):
    """The deterministic split. Selecting kind == 'animation' out of the manifest
    is a filter, so it happens in Python. The agent's job is the enrichment that
    follows, not the selection."""
    return [a for a in manifest.get("assets", []) if a.get("kind") == "animation"]


def validate_animation_coverage(manifest, animation_list):
    """Gate 3. Nothing may be dropped, and nothing may be invented.

    One manifest asset can legitimately expand into several clips, so coverage
    means every animation asset is claimed at least once, not exactly once.
    """
    errors = []
    manifest_ids = {a["asset_id"] for a in animation_assets(manifest)}
    all_asset_ids = {a["asset_id"] for a in manifest.get("assets", [])}

    animations = animation_list.get("animations", [])
    claimed = {a.get("source_asset_id") for a in animations}

    for dropped in sorted(manifest_ids - claimed):
        errors.append(
            f"Animation asset '{dropped}' is in the manifest but no clip claims it."
        )

    for animation in animations:
        source = animation.get("source_asset_id")
        if source not in all_asset_ids:
            errors.append(
                f"Clip '{animation.get('animation_id')}' cites source_asset_id "
                f"'{source}', which is not in the asset manifest."
            )
        elif source not in manifest_ids:
            errors.append(
                f"Clip '{animation.get('animation_id')}' cites '{source}', which is "
                f"in the manifest but is not kind 'animation'."
            )

    # Capture sessions must partition the clips, with no dangling references.
    animation_ids = {a.get("animation_id") for a in animations}
    grouped = set()
    for session in animation_list.get("capture_sessions", []):
        for ref in session.get("animation_ids", []) or []:
            if ref not in animation_ids:
                errors.append(
                    f"Capture session '{session.get('session_id')}' lists "
                    f"'{ref}', which is not a clip in this list."
                )
            grouped.add(ref)
    for ungrouped in sorted(animation_ids - grouped):
        errors.append(f"Clip '{ungrouped}' is not assigned to any capture session.")

    return errors


def spec_as_prompt(artifact_key):
    """Render a schema as text an agent can follow exactly."""
    lines = [f"OUTPUT SCHEMA for {artifact_key} — emit exactly this shape:"]
    for collection, spec in ARTIFACTS[artifact_key].items():
        lines.append(f'  "{collection}": array of objects, each with:')
        for field, (expected, constraint) in spec.items():
            if constraint == "snake_case":
                rule = "string, snake_case"
            elif isinstance(constraint, list):
                rule = f"string, one of {constraint}"
            elif isinstance(constraint, tuple):
                rule = f"{expected.__name__}, range {constraint}"
            elif expected is list:
                rule = "array of strings"
            else:
                rule = expected.__name__
            lines.append(f"      {field}: {rule}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Deterministic ID annotation
# ---------------------------------------------------------------------------
#
# Agents emit plain arrays of IDs. Expanding those into {id, label} pairs is a
# dictionary lookup, so it happens here rather than being asked of three
# different agents. The payoff is consistency: EVT-030 reads as the same short
# phrase in the asset manifest, the animation list and the gap report, because
# all three are annotated from one index built once by the Scenographer.

EVENT_ID_LISTS = ("event_ids", "evidence_events", "update_events")
EVENT_ID_SINGLES = ("event_id", "start_event", "end_event")
ASSET_ID_LISTS = ("required_asset_ids",)
ANIMATION_ID_LISTS = ("animation_ids",)

FALLBACK_WORDS = 4


def build_event_labels(events, agent_labels):
    """Agent labels win. Anything the agent missed falls back to the first few
    words of the event's own text, so no ID is ever left bare."""
    index = {}
    for event in events:
        words = event.get("content", "").split()
        fallback = " ".join(words[:FALLBACK_WORDS]).rstrip(".,;:")
        index[event["event_id"]] = fallback or event["event_type"].lower()
    for entry in agent_labels:
        eid, label = entry.get("event_id"), (entry.get("label") or "").strip()
        if eid and label:
            index[eid] = label
    return index


def annotate(payload, event_labels, asset_labels=None, animation_labels=None):
    """Recursively expand ID arrays into {id, label} pairs.

    Single-value ID fields keep their type and gain a sibling '<field>_label',
    so nothing that already reads those fields breaks.
    """
    asset_labels = asset_labels or {}
    animation_labels = animation_labels or {}

    def pair(key_name, value, index):
        return {key_name: value, "label": index.get(value, "unlabelled")}

    def walk(node):
        if isinstance(node, list):
            return [walk(item) for item in node]
        if not isinstance(node, dict):
            return node

        result = {}
        for key, value in node.items():
            if key in EVENT_ID_LISTS and isinstance(value, list):
                result[key] = [
                    pair("event_id", v, event_labels) if isinstance(v, str) else walk(v)
                    for v in value
                ]
            elif key in ASSET_ID_LISTS and isinstance(value, list):
                result[key] = [
                    pair("asset_id", v, asset_labels) if isinstance(v, str) else walk(v)
                    for v in value
                ]
            elif key in ANIMATION_ID_LISTS and isinstance(value, list):
                result[key] = [
                    pair("animation_id", v, animation_labels) if isinstance(v, str) else walk(v)
                    for v in value
                ]
            elif key in EVENT_ID_SINGLES and isinstance(value, str):
                result[key] = value
                result[f"{key}_label"] = event_labels.get(value, "unlabelled")
            else:
                result[key] = walk(value)
        return result

    return walk(payload)
