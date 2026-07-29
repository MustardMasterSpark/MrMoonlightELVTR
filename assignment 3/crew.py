#!/usr/bin/env python3
"""
MR. MOONLIGHT — DAY 1 SLICE COMPILER

Reads the Day 1 script and produces the production data needed to build the
vertical slice, plus a report of everything the script requires that the GDD
never budgeted.

    python3 crew.py --dry-run              # full pipeline, no API key, no cost
    python3 crew.py                        # live run, all 10 scenes
    python3 crew.py --scenes 2             # live run, first 2 scenes only (cheap)

Zero dependencies. An agent here is one HTTP POST with a scoped system prompt,
a declared input read from the blackboard, and a declared output contract.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

import parse_script
import schemas

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"

SONNET = "claude-sonnet-5"
HAIKU = "claude-haiku-4-5-20251001"

# Claude Code backend. CLAUDE_ARGS is deliberately minimal so it works across
# versions. If your install supports extra flags you want (a model selector,
# a system-prompt flag), add them here. Run 'claude --help' to see what it takes.
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "claude")
CLAUDE_ARGS = ["-p"]

ROOT = Path(__file__).parent
KNOWLEDGE = ROOT / "knowledge"
SCRIPT_PATH = ROOT / "SCRIPT.txt"
MAX_RETRIES = 1


# ---------------------------------------------------------------------------
# Shared blackboard
# ---------------------------------------------------------------------------

class Blackboard:
    """The only channel between agents. No agent calls another agent directly,
    so the entire inter-agent conversation ends up on disk and stays readable
    after the run."""

    def __init__(self, directory):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.dir / "run.log"
        self.log_path.write_text("")
        self.tokens_in = 0
        self.tokens_out = 0
        self.calls = 0

    def write(self, key, payload):
        (self.dir / f"{key}.json").write_text(json.dumps(payload, indent=2) + "\n")
        self.log("WRITE", key)

    def read(self, key):
        return json.loads((self.dir / f"{key}.json").read_text())

    def log(self, kind, message):
        line = f"[{time.strftime('%H:%M:%S')}] {kind:<9} {message}"
        with self.log_path.open("a") as handle:
            handle.write(line + "\n")
        print(line, flush=True)

    def account(self, agent, tokens_in, tokens_out):
        self.tokens_in += tokens_in
        self.tokens_out += tokens_out
        self.calls += 1
        self.log("TOKENS", f"{agent}: {tokens_in} in / {tokens_out} out")


# ---------------------------------------------------------------------------
# Model transport
# ---------------------------------------------------------------------------

def resolve_backend(requested):
    """Decide which transport to use, and fail early with a readable reason."""
    if requested == "auto":
        if shutil.which(CLAUDE_BIN):
            return "claude-code"
        if os.environ.get("ANTHROPIC_API_KEY"):
            return "api"
        raise SystemExit(
            "No backend available.\n"
            f"  - '{CLAUDE_BIN}' is not on your PATH, so the subscription backend cannot run.\n"
            "  - ANTHROPIC_API_KEY is not set, so the API backend cannot run.\n"
            "Install Claude Code, or set an API key, or use --dry-run."
        )

    if requested == "claude-code" and not shutil.which(CLAUDE_BIN):
        raise SystemExit(
            f"Backend 'claude-code' selected but '{CLAUDE_BIN}' is not on your PATH.\n"
            "Install Claude Code and sign in with your Anthropic account, then retry.\n"
            "Or run with --backend api, or --dry-run."
        )

    if requested == "api" and not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit(
            "Backend 'api' selected but ANTHROPIC_API_KEY is not set.\n"
            "Export the key, or use --backend claude-code, or --dry-run."
        )

    return requested


def call_claude_code(system_prompt, user_prompt):
    """Transport 2: shell out to the Claude Code CLI, which authenticates with a
    Pro or Max subscription rather than API credits.

    The prompt goes in over stdin rather than as an argument, because the
    Sequencer's context includes all 224 events and would blow past the
    operating system's argument length limit.

    Claude Code's plain-text output carries no usage numbers, so token counts in
    the log are estimated from character length and marked as such.
    """
    prompt = f"{system_prompt}\n\n{user_prompt}"
    command = [CLAUDE_BIN] + CLAUDE_ARGS

    try:
        completed = subprocess.run(
            command, input=prompt, capture_output=True, text=True, timeout=900
        )
    except FileNotFoundError:
        raise SystemExit(f"Could not execute '{CLAUDE_BIN}'. Is Claude Code installed?")
    except subprocess.TimeoutExpired:
        raise SystemExit("Claude Code timed out after 15 minutes.")

    if completed.returncode != 0:
        raise SystemExit(
            f"Claude Code exited {completed.returncode}.\n"
            f"Command: {' '.join(command)}\n"
            f"stderr: {completed.stderr[:800]}\n\n"
            "If the failure mentions an unknown flag, adjust CLAUDE_ARGS at the "
            "top of crew.py to match your installed version. Run 'claude --help' "
            "to see the flags it supports."
        )

    # Rough estimate only: about four characters per token.
    return completed.stdout, len(prompt) // 4, len(completed.stdout) // 4


def call_api(model, system_prompt, user_prompt, max_tokens):
    """Transport 1: direct HTTP to the Messages API. Requires API credits."""
    key = os.environ["ANTHROPIC_API_KEY"]

    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }).encode()

    request = urllib.request.Request(API_URL, data=body, headers={
        "content-type": "application/json",
        "x-api-key": key,
        "anthropic-version": API_VERSION,
    })

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            data = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"API error {exc.code}: {exc.read().decode()[:600]}")

    text = "".join(block.get("text", "") for block in data.get("content", []))
    usage = data.get("usage", {})
    return text, usage.get("input_tokens", 0), usage.get("output_tokens", 0)


def call_model(model, system_prompt, user_prompt, max_tokens=8000, backend="api"):
    """The single seam between the crew and a model.

    Both backends take the same three things and return the same three things,
    so nothing else in the pipeline knows or cares which one is in use. The
    agent prompts, the blackboard and both gates are identical either way.
    """
    if backend == "claude-code":
        return call_claude_code(system_prompt, user_prompt)
    return call_api(model, system_prompt, user_prompt, max_tokens)


def parse_json(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.rstrip().endswith("```"):
            cleaned = cleaned.rstrip()[:-3]
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object in model output: {text[:300]}")
    return json.loads(cleaned[start:end + 1])


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

@dataclass
class Agent:
    name: str
    role: str
    model: str
    writes: str
    reads: list = field(default_factory=list)
    system: str = ""


SCENOGRAPHER = Agent(
    name="Scenographer",
    role="Infers what must physically exist for each scripted event to play.",
    model=SONNET,
    reads=["00_events (one scene at a time)", "canon"],
    writes="01_requirements",
    system="""You are the Scenographer for the survival horror game Mr. Moonlight.

You receive the events of one scene from the Day 1 script, plus the game canon.
For each event, you infer what must physically exist in the Unity project for
that event to play. You are reading a script and producing a production
requirements list.

Worked example. Given:
    EVT-030 | ANIMATION | Tracey wipes her mouth; her hand briefly passes in front of the camera.
you emit three requirements: a first-person hand and forearm mesh (model), a
mouth-wipe animation clip authored in camera space (animation), and nothing
else. You do NOT invent a face rig, because the camera is first person.

Rules:
- One requirement per distinct thing needed. Split compound events.
- Be concrete and physical. "Wolf model, quadruped, low poly, readable
  silhouette in darkness" — not "wolf stuff".
- DIALOGUE events require a voice line (sfx) and a subtitle (ui_message).
  THOUGHT events require only a ui_message; they are on-screen text, not voiced.
- SYSTEM events that enable or restrict a mechanic are kind "system".
  SYSTEM events that place an object in the world are kind "prop" or "environment".
- Interior spaces are kind "environment" and must be named explicitly, for
  example "mine interior, linear route with infirmary room".
- An escort, drag, or carry interaction is kind "mechanic", not "animation".
- OUTLINE events are unfinished, but still imply requirements. Infer them and
  say so in the detail field.
- BEAT and NOTE events usually imply nothing. Skip them unless timing requires
  a specific asset.
- Do not deduplicate across events. The next stage does that. If the wolf
  appears in five events, emit it five times.

SECOND OUTPUT: "event_labels". For EVERY event in the scene you were given,
including BEAT and NOTE events, emit a two or three word label naming what the
event is. These labels are reused verbatim across every downstream file, so they
must be short, concrete and readable on their own.

  EVT-030 -> "mouth wipe"
  EVT-045 -> "radio ringing"
  EVT-204 -> "stretcher drag"
  EVT-152 -> "sprint unlocked"

Not "Tracey does something" and not a full sentence. A label, like a filename.

Return ONLY a JSON object, no prose and no markdown fences.""",
)

QUARTERMASTER = Agent(
    name="Quartermaster",
    role="Collapses requirements into unique assets and checks each against the budget.",
    model=SONNET,
    reads=["01_requirements", "budget"],
    writes="02_asset_manifest",
    system="""You are the Quartermaster for Mr. Moonlight.

You receive a long requirements list with heavy duplication, and the developer's
stated feature budget from the GDD. You do two things.

FIRST, deduplicate. The wolf appearing in five events is one asset. Merge those
into a single entry and list every event_id that needs it in event_ids. Choose a
stable snake_case asset_id.

SECOND, and this is the important half, check every asset against the budget and
set budget_status:
  "budgeted"    the budget covers this asset at the scope the script needs.
  "partial"     the budget mentions it but at insufficient scope. The clearest
                case: the budget lists a model as "exterior only" but the script
                requires the player to go inside it.
  "unbudgeted"  the budget does not cover this at all.

Set budget_ref to the budget entry you matched, or "none" when unbudgeted.

Be strict and literal about scope. Do not be generous. If the budget says
"exterior only" and the script has the player walking through the interior, that
is "partial", not "budgeted". Check the already_owned section too: the developer
owns an FPS package and a terrain system, and things those cover are budgeted.

Use notes to explain any judgment that is not obvious, especially every partial
and every unbudgeted asset.

Return ONLY a JSON object, no prose and no markdown fences.""",
)

ANIMATION_DIRECTOR = Agent(
    name="Animation director",
    role="Turns animation assets into a production-ready clip list and capture schedule.",
    model=SONNET,
    reads=["02_asset_manifest (animation assets only)", "00_events", "canon"],
    writes="03_animation_list",
    system="""You are the Animation director for Mr. Moonlight.

You receive the animation assets already extracted from the manifest by a
deterministic filter, the script events that reference them, and the game canon.
You do NOT select which assets are animations, that is already done. Your job is
the production metadata that turns a list of names into something a solo
developer can schedule and capture.

The GDD's feature list contains the entry "Listing of animations (TBD)". You are
producing that listing.

For every clip decide:

- rig_target. The game is first person, so most player animation is
  "first_person_hands" in camera space. Use "player_full_body" only where the
  script shows Tracey's body: dropping to her knees, vomiting, climbing. Wolves
  are "quadruped". The Furman and the totems are "creature". Doors, tent flaps,
  the telescope and the RV rug are "prop". Screen shakes, forced looks and blurs
  are "camera".
- capture_method. The developer shoots reference video with a GoPro and converts
  it through DeepMotion or QuickMagic, so full-body and humanoid NPC work is
  "mocap_video". Camera moves and prop hinges are "procedural" or "hand_keyed",
  never mocap. First-person hand work is usually "mocap_video" for gross motion
  and "hand_keyed" for anything holding a weapon precisely. If the purchased FPS
  package plausibly already ships it, say "asset_package" and explain in notes.
- playback. "one_shot" for most, "loop" for walk cycles and idles, "additive"
  for layered effects like breathing or a limp on top of locomotion.
- blocks_player_control. True where the script has a CUTSCENE:BLOCKING event or
  where player input mid-clip would break it.
- needs_animation_event. True when gameplay must fire on a specific frame: the
  moment a weapon connects, the moment an item is picked up, the frame a door
  becomes passable. The GDD calls this the animation event blocker.
- approx_duration_sec. Your best estimate. Be realistic, not round.
- capture_session. Group clips shootable in one sitting: same rig, same costume,
  same location, same method. Full-body distress in scene 01 is a different
  session from prop hinges. This grouping is the point. It turns twenty
  scattered clips into four afternoons of work.

Then emit capture_sessions summarising those groups. Every clip belongs to
exactly one session and every session lists its clip ids. A validator checks
this, and also checks that you dropped nothing and invented nothing.

Return ONLY a JSON object, no prose and no markdown fences.""",
)

SEQUENCER = Agent(
    name="Sequencer",
    role="Builds the runtime objective graph and the system-unlock timeline.",
    model=SONNET,
    reads=["00_events", "02_asset_manifest"],
    writes="04_runtime_data",
    system="""You are the Sequencer for Mr. Moonlight. You produce the runtime
data the game actually loads.

TWO OUTPUTS.

"objectives": the objective state machine. Walk the script in order. Each
OBJECTIVE:START opens an objective, each OBJECTIVE:UPDATE changes the active
one, each OBJECTIVE:END closes it. For each objective record the start event,
the end event, any update events in between, and required_asset_ids drawn from
the asset manifest: the assets that must be loaded for that objective to be
completable.

Report the script honestly. If an OBJECTIVE:UPDATE appears with no objective
open, or an OBJECTIVE:END has no matching START, do not invent a START to make
the graph tidy. Represent what the script actually says. A validator downstream
compares your graph to the source, and the discrepancy is a finding about the
script, not a mistake by you.

"unlocks": the progression timeline. Find every event that first enables a
player capability and record which system, at which event. The player begins
with almost nothing: no movement, no stamina bar, no map, no sprint, no weapon.
Each arrives at a specific event. Use only these system names:
""" + json.dumps(schemas.UNLOCKABLE_SYSTEMS) + """

Return ONLY a JSON object, no prose and no markdown fences.""",
)

GAP_AUDITOR = Agent(
    name="Gap auditor",
    role="Reports what the script needs that the GDD never budgeted.",
    model=SONNET,
    reads=["02_asset_manifest", "03_animation_list", "04_runtime_data",
           "budget", "gate residuals"],
    writes="05_gap_report",
    system="""You are the Gap auditor for Mr. Moonlight, reporting to a solo
developer with roughly five weeks until an itch.io release.

You receive the asset manifest with budget status already assigned, the runtime
data, the GDD feature budget, and any discrepancies the deterministic validators
could not resolve. Your job is to tell the developer what will hurt.

Report findings in these categories:

1. "unbudgeted_asset" — every asset marked unbudgeted or partial. State the
   real production consequence, not just that it is missing. An interior space
   that the budget scoped as exterior-only is days of level work, not a note.
2. "budgeted_but_unused" — features the budget pays for that the Day 1 script
   never exercises. These are candidates to defer past the slice. Look hard for
   these: they are where the developer gets time back.
3. "continuity" — the unresolved validator discrepancies, restated so a human
   can act on them. Explain what the player would experience if shipped as-is.
4. "progression" — a system used before the unlock timeline enables it, or
   unlocked and never used.
5. "scope" — your overall read on whether Day 1 is deliverable, referencing the
   budget's own day estimates.

Severity:
  BLOCKER  Day 1 cannot ship without resolving this.
  WARNING  ships, but degraded or wasteful.
  NOTE     worth knowing.

Be direct. Do not soften. A developer who finds out in week four is worse off
than one who reads it here. Cite specific event ids in evidence_events.

Also set:
  "summary" — three sentences a developer can read in ten seconds.
  "budget_pressure" — a short string comparing budgeted days against what the
  unbudgeted work implies.

Return ONLY a JSON object, no prose and no markdown fences.""",
)

PIPELINE = [SCENOGRAPHER, QUARTERMASTER, ANIMATION_DIRECTOR, SEQUENCER, GAP_AUDITOR]


# ---------------------------------------------------------------------------
# Dry-run fixtures, built from the real parsed script so both gates run for real
# ---------------------------------------------------------------------------

def fixture_requirements(events):
    kinds = {
        "ANIMATION": "animation", "SFX": "sfx", "VFX": "vfx",
        "MESSAGE": "ui_message", "ACTION": "prop", "SYSTEM": "system",
        "DIALOGUE:T": "sfx", "DIALOGUE:R": "sfx", "THOUGHT:T": "ui_message",
        "CUTSCENE:BLOCKING": "mechanic", "OUTLINE": "environment",
        "OBJECTIVE:START": "ui_message", "OBJECTIVE:UPDATE": "ui_message",
        "OBJECTIVE:END": "ui_message",
    }
    return {
        "requirements": [
            {
                "event_id": event["event_id"],
                "kind": kinds.get(event["event_type"], "prop"),
                "name": f"fixture requirement for {event['event_id']}",
                "detail": "Dry-run fixture. No model judgment was applied.",
            }
            for event in events if event["event_type"] in kinds
        ],
        "event_labels": [
            {
                "event_id": event["event_id"],
                "label": " ".join(event["content"].split()[:3]).rstrip(".,;:")
                         or event["event_type"].lower(),
            }
            for event in events
        ],
    }


def fixture_manifest(requirements):
    seen, assets = {}, []
    for requirement in requirements["requirements"]:
        key = requirement["kind"]
        if key not in seen:
            seen[key] = {
                "asset_id": f"fixture_{key}",
                "name": f"Fixture {key} asset",
                "kind": key,
                "event_ids": [],
                "budget_status": "unbudgeted" if key == "environment" else "budgeted",
                "budget_ref": "none" if key == "environment" else "fixture",
                "notes": "Dry-run fixture.",
            }
            assets.append(seen[key])
        seen[key]["event_ids"].append(requirement["event_id"])
    return {"assets": assets}


def fixture_animation_list(manifest):
    """Covers every animation asset exactly once and groups them, so gate 3
    passes legitimately rather than being skipped."""
    sources = schemas.animation_assets(manifest)
    animations, sessions = [], {}
    for index, asset in enumerate(sources):
        animation_id = f"anim_{index:03d}_{asset['asset_id']}"[:60]
        session_id = "fixture_session_first_person"
        animations.append({
            "animation_id": animation_id,
            "name": f"Fixture clip for {asset['name']}",
            "source_asset_id": asset["asset_id"],
            "event_ids": asset.get("event_ids", []),
            "rig_target": "first_person_hands",
            "capture_method": "hand_keyed",
            "playback": "one_shot",
            "blocks_player_control": False,
            "needs_animation_event": False,
            "approx_duration_sec": 1.5,
            "capture_session": session_id,
            "notes": "Dry-run fixture. No model judgment was applied.",
        })
        sessions.setdefault(session_id, []).append(animation_id)

    if not animations:
        animations.append({
            "animation_id": "anim_placeholder",
            "name": "Placeholder clip",
            "source_asset_id": "fixture_animation",
            "event_ids": [],
            "rig_target": "first_person_hands",
            "capture_method": "hand_keyed",
            "playback": "one_shot",
            "blocks_player_control": False,
            "needs_animation_event": False,
            "approx_duration_sec": 1.0,
            "capture_session": "fixture_session_first_person",
            "notes": "No animation assets in the manifest.",
        })
        sessions["fixture_session_first_person"] = ["anim_placeholder"]

    return {
        "animations": animations,
        "capture_sessions": [
            {
                "session_id": session_id,
                "description": "Dry-run fixture capture session.",
                "rig_target": "first_person_hands",
                "capture_method": "hand_keyed",
                "animation_ids": ids,
            }
            for session_id, ids in sessions.items()
        ],
    }


def fixture_runtime(events):
    """Pairs each START with the next END, in order. This deliberately leaves
    the script's orphan OBJECTIVE:END unclaimed, so gate 2 reports a real bug
    even in a dry run."""
    objectives, active = [], None
    for event in events:
        etype, eid = event["event_type"], event["event_id"]
        if etype == "OBJECTIVE:START":
            active = {
                "objective_id": f"obj_{eid.lower().replace('-', '_')}",
                "label": event["content"].strip('"')[:80] or "unnamed",
                "start_event": eid,
                "end_event": "",
                "update_events": [],
                "required_asset_ids": ["fixture_ui_message"],
            }
            objectives.append(active)
        elif etype == "OBJECTIVE:UPDATE" and active:
            active["update_events"].append(eid)
        elif etype == "OBJECTIVE:END" and active and not active["end_event"]:
            active["end_event"] = eid
            active = None
    for objective in objectives:
        if not objective["end_event"]:
            objective["end_event"] = objective["start_event"]
    return {
        "objectives": objectives,
        "unlocks": [{"system": "camera_look", "event_id": "EVT-010",
                     "note": "Dry-run fixture."}],
    }


def fixture_gap_report(residuals):
    findings = [{
        "severity": "NOTE",
        "category": "scope",
        "subject": "Dry run",
        "evidence_events": [],
        "issue": "No model judgment was applied. Run without --dry-run for a real audit.",
        "recommendation": "Set ANTHROPIC_API_KEY and run again.",
    }]
    for residual in residuals[:10]:
        findings.append({
            "severity": "WARNING",
            "category": "continuity",
            "subject": "Objective graph discrepancy",
            "evidence_events": [],
            "issue": residual,
            "recommendation": "Reconcile the objective bookkeeping in the script.",
        })
    return {
        "findings": findings,
        "summary": "Dry run completed. Both validation gates executed against the real script.",
        "budget_pressure": "Not assessed in dry run.",
    }


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def dispatch(agent, board, dry_run, payload_builder=None, context=None,
             max_tokens=8000, backend="api"):
    label = agent.model if backend == "api" else f"via {CLAUDE_BIN}"
    board.log("DISPATCH", f"{agent.name} ({label})")
    if dry_run:
        payload = payload_builder()
        board.account(agent.name, 0, 0)
        return payload
    text, tin, tout = call_model(agent.model, agent.system, context, max_tokens, backend)
    board.account(agent.name, tin, tout)
    return parse_json(text)


def gated(agent, board, artifact_key, dry_run, payload_builder, context_builder,
          extra_validator=None, max_tokens=8000, backend="api",
          residual_note="Forwarding to the Gap auditor as evidence."):
    """Runs an agent, validates its artifact, retries once with the errors."""
    fixup, residual = "", []
    for attempt in range(1, MAX_RETRIES + 2):
        payload = dispatch(agent, board, dry_run, payload_builder,
                           (context_builder() + fixup) if not dry_run else None,
                           max_tokens, backend)
        errors = schemas.validate_artifact(artifact_key, payload)
        if not errors and extra_validator:
            residual = extra_validator(payload)
            if residual:
                board.log("GATE", f"Graph validation found {len(residual)} discrepancy(ies)")
                for item in residual[:8]:
                    board.log("GATE", f"  - {item}")
                if attempt <= MAX_RETRIES:
                    board.log("RETRY", f"Re-dispatching {agent.name} with discrepancies.")
                    fixup = ("\n\n--- graph discrepancies to reconcile ---\n"
                             + "\n".join(f"- {r}" for r in residual))
                    continue
                board.log("GATE", residual_note)
        if not errors:
            board.log("GATE", f"{artifact_key} schema valid on attempt {attempt}.")
            board.write(artifact_key, payload)
            return payload, residual
        board.log("GATE", f"{artifact_key} schema INVALID on attempt {attempt}: "
                          f"{len(errors)} error(s)")
        for error in errors[:8]:
            board.log("GATE", f"  - {error}")
        if attempt > MAX_RETRIES:
            board.log("ABORT", f"{agent.name} could not produce a valid artifact.")
            return None, residual
        board.log("RETRY", f"Re-dispatching {agent.name} with {len(errors)} error(s).")
        fixup = ("\n\n--- your previous output failed validation, correct exactly these ---\n"
                 + "\n".join(f"- {e}" for e in errors))
    return None, residual


def orchestrate(board, dry_run, scene_limit=None, backend="api", script_path=None):
    board.log("START", f"Day 1 Slice Compiler — backend={'fixtures' if dry_run else backend}")

    # ---- Deterministic pre-pass. No model involved. ----
    script_path = Path(script_path or SCRIPT_PATH)
    if not script_path.exists():
        raise SystemExit(f"Script not found: {script_path}\n"
                        "Expected SCRIPT.txt beside crew.py, or pass --script PATH.")
    board.log("SOURCE", str(script_path.name))
    events = parse_script.parse(script_path)
    summary = parse_script.summarise(events)
    board.log("PARSE", f"{summary['total_events']} events across "
                       f"{summary['scene_count']} scenes, "
                       f"{len(summary['unfinished_scenes'])} unfinished")

    by_scene = parse_script.scenes(events)
    if scene_limit:
        keep = sorted(by_scene)[:scene_limit]
        by_scene = {k: by_scene[k] for k in keep}
        events = [e for e in events if e["scene_number"] in keep]
        board.log("PARSE", f"Limited to scenes {keep}")

    board.write("00_events", {"summary": summary, "events": events})
    board.write("subtitles", {"rows": parse_script.extract_subtitles(events)})
    for source in ("canon", "budget"):
        board.write(source, json.loads((KNOWLEDGE / f"{source}.json").read_text()))

    canon = board.read("canon")
    budget = board.read("budget")

    # ---- Stage 1: Scenographer, one call per scene ----
    requirements = {"requirements": [], "event_labels": []}
    if dry_run:
        requirements = dispatch(SCENOGRAPHER, board, True,
                                lambda: fixture_requirements(events))
    else:
        for number, scene_events in by_scene.items():
            title = scene_events[0]["scene_title"]
            board.log("SCENE", f"{number:02d} {title} ({len(scene_events)} events)")
            context = (
                f"--- canon ---\n{json.dumps(canon, indent=2)}\n\n"
                f"--- scene {number:02d}: {title} ---\n"
                f"{json.dumps(scene_events, indent=2)}\n\n"
                f"{schemas.spec_as_prompt('01_requirements')}"
            )
            payload = dispatch(SCENOGRAPHER, board, False, context=context,
                               backend=backend)
            requirements["requirements"].extend(payload.get("requirements", []))
            requirements["event_labels"].extend(payload.get("event_labels", []))

    errors = schemas.validate_artifact("01_requirements", requirements)
    if errors:
        board.log("GATE", f"01_requirements INVALID: {len(errors)} error(s)")
        for error in errors[:8]:
            board.log("GATE", f"  - {error}")
        board.log("ABORT", "Scenographer output unusable.")
        return None
    board.log("GATE", f"01_requirements schema valid. "
                      f"{len(requirements['requirements'])} requirements, "
                      f"{len(requirements['event_labels'])} event labels.")
    board.write("01_requirements", requirements)

    event_labels = schemas.build_event_labels(events, requirements["event_labels"])
    labelled = sum(1 for e in events
                   if any(x.get("event_id") == e["event_id"]
                          for x in requirements["event_labels"]))
    board.log("LABELS", f"{labelled} of {len(events)} events labelled by the agent, "
                        f"remainder filled deterministically from event text")

    # ---- Stage 2: Quartermaster ----
    manifest, _ = gated(
        QUARTERMASTER, board, "02_asset_manifest", dry_run,
        lambda: fixture_manifest(requirements),
        lambda: (f"--- budget ---\n{json.dumps(budget, indent=2)}\n\n"
                 f"--- requirements ---\n{json.dumps(requirements, indent=2)}\n\n"
                 f"{schemas.spec_as_prompt('02_asset_manifest')}"),
        max_tokens=16000, backend=backend,
    )
    if manifest is None:
        return None
    statuses = {}
    for asset in manifest["assets"]:
        statuses[asset["budget_status"]] = statuses.get(asset["budget_status"], 0) + 1
    board.log("MANIFEST", f"{len(manifest['assets'])} unique assets: {statuses}")

    # ---- Stage 3: Animation director. Deterministic filter, then enrichment. ----
    anim_sources = schemas.animation_assets(manifest)
    board.log("FILTER", f"{len(anim_sources)} of {len(manifest['assets'])} assets are "
                        f"kind 'animation' (selected in Python, not by a model)")
    anim_event_ids = {eid for asset in anim_sources for eid in asset.get("event_ids", [])}
    anim_events = [e for e in events if e["event_id"] in anim_event_ids]

    animations, anim_residual = gated(
        ANIMATION_DIRECTOR, board, "03_animation_list", dry_run,
        lambda: fixture_animation_list(manifest),
        lambda: (f"--- canon ---\n{json.dumps(canon, indent=2)}\n\n"
                 f"--- animation assets from the manifest ---\n"
                 f"{json.dumps(anim_sources, indent=2)}\n\n"
                 f"--- script events that reference them ---\n"
                 f"{json.dumps(anim_events, indent=2)}\n\n"
                 f"{schemas.spec_as_prompt('03_animation_list')}"),
        extra_validator=lambda payload: schemas.validate_animation_coverage(manifest, payload),
        max_tokens=16000, backend=backend,
        residual_note="Coverage gaps persist. Forwarding to the Gap auditor as an "
                      "animation-list quality warning.",
    )
    if animations is None:
        return None
    board.log("ANIMATION", f"{len(animations['animations'])} clips across "
                           f"{len(animations['capture_sessions'])} capture sessions")

    # ---- Stage 4: Sequencer, with the objective-graph gate ----
    runtime, residual = gated(
        SEQUENCER, board, "04_runtime_data", dry_run,
        lambda: fixture_runtime(events),
        lambda: (f"--- events ---\n{json.dumps(events, indent=2)}\n\n"
                 f"--- asset manifest ---\n{json.dumps(manifest, indent=2)}\n\n"
                 f"{schemas.spec_as_prompt('03_runtime_data')}"),
        extra_validator=lambda payload: schemas.validate_objective_graph(events, payload),
        max_tokens=12000, backend=backend,
        residual_note="Discrepancies persist. Forwarding to the Gap auditor as "
                      "evidence of a script bug.",
    )
    if runtime is None:
        return None

    all_residual = anim_residual + residual

    # ---- Stage 5: Gap auditor ----
    report, _ = gated(
        GAP_AUDITOR, board, "05_gap_report", dry_run,
        lambda: fixture_gap_report(all_residual),
        lambda: (f"--- budget ---\n{json.dumps(budget, indent=2)}\n\n"
                 f"--- asset manifest ---\n{json.dumps(manifest, indent=2)}\n\n"
                 f"--- animation list ---\n{json.dumps(animations, indent=2)}\n\n"
                 f"--- runtime data ---\n{json.dumps(runtime, indent=2)}\n\n"
                 f"--- unresolved validator discrepancies ---\n"
                 f"{json.dumps(all_residual, indent=2)}\n\n"
                 f"{schemas.spec_as_prompt('05_gap_report')}"),
        max_tokens=12000, backend=backend,
    )
    if report is None:
        return None

    counts = {}
    for finding in report["findings"]:
        counts[finding["severity"]] = counts.get(finding["severity"], 0) + 1
    board.log("AUDIT", f"{len(report['findings'])} findings: {counts}")
    board.log("DONE", f"{board.calls} model calls, "
                      f"{board.tokens_in} in / {board.tokens_out} out")

    return {"manifest": manifest, "animations": animations, "runtime": runtime,
            "report": report, "subtitles": board.read("subtitles"),
            "residual": all_residual, "event_labels": event_labels}


# ---------------------------------------------------------------------------
# Output rendering
# ---------------------------------------------------------------------------

def render_gap_report(report, residual, event_labels=None):
    order = {"BLOCKER": 0, "WARNING": 1, "NOTE": 2}
    findings = sorted(report["findings"], key=lambda f: order.get(f["severity"], 9))

    lines = [
        "# Mr. Moonlight — Day 1 gap report",
        "",
        f"_Generated by the Day 1 Slice Compiler on {time.strftime('%Y-%m-%d %H:%M')}._",
        "",
        "## Summary", "", report.get("summary", "").strip(), "",
        f"**Budget pressure:** {report.get('budget_pressure', 'not assessed')}", "",
    ]

    for severity in ("BLOCKER", "WARNING", "NOTE"):
        group = [f for f in findings if f["severity"] == severity]
        if not group:
            continue
        lines += [f"## {severity} ({len(group)})", ""]
        for finding in group:
            labels = event_labels or {}
            evidence = ", ".join(
                f"{eid} ({labels.get(eid, 'unlabelled')})"
                for eid in finding.get("evidence_events", [])
            ) or "—"
            lines += [
                f"### {finding.get('subject', 'Untitled')}",
                f"`{finding.get('category', 'uncategorised')}` · events: {evidence}",
                "",
                finding.get("issue", "").strip(),
                "",
                f"**Recommendation:** {finding.get('recommendation', '').strip()}",
                "",
            ]

    if residual:
        lines += ["## Unresolved validator discrepancies", "",
                  "Found deterministically by comparing the objective graph to the "
                  "source script. These are script bugs, not agent errors.", ""]
        lines += [f"- {item}" for item in residual] + [""]

    return "\n".join(lines)


def write_outputs(result, out_dir):
    """Annotate every ID list, then write.

    The blackboard keeps raw agent output as the audit trail; the annotation
    happens here, on the way to output/, so what a human reads is labelled and
    what a reviewer inspects is untouched.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    event_labels = result["event_labels"]
    asset_labels = {a["asset_id"]: a["name"] for a in result["manifest"]["assets"]}
    animation_labels = {a["animation_id"]: a["name"]
                        for a in result["animations"]["animations"]}

    def dress(payload):
        return schemas.annotate(payload, event_labels, asset_labels, animation_labels)

    for filename, payload in (
        ("asset_manifest.json", result["manifest"]),
        ("animation_assets.json", result["animations"]),
        ("runtime_data.json", result["runtime"]),
        ("subtitles.json", result["subtitles"]),
    ):
        (out_dir / filename).write_text(json.dumps(dress(payload), indent=2) + "\n")

    (out_dir / "gap_report.md").write_text(
        render_gap_report(result["report"], result["residual"], event_labels))
    (out_dir / "event_labels.json").write_text(
        json.dumps({"labels": [{"event_id": k, "label": v}
                               for k, v in sorted(event_labels.items())]}, indent=2) + "\n")
    return out_dir


def main():
    parser = argparse.ArgumentParser(description="Mr. Moonlight Day 1 Slice Compiler")
    parser.add_argument("--script", default=str(SCRIPT_PATH),
                        help="Path to the script file. Default: SCRIPT.txt")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run the whole pipeline with fixtures. No API key, no spend.")
    parser.add_argument("--scenes", type=int, default=None,
                        help="Only process the first N scenes. Useful for a cheap live test.")
    parser.add_argument("--backend", choices=["claude-code", "api", "auto"],
                        default="claude-code",
                        help="claude-code uses your Pro/Max subscription via the Claude Code "
                             "CLI. api uses ANTHROPIC_API_KEY and credits. Default: claude-code.")
    parser.add_argument("--blackboard", default=str(ROOT / "blackboard"))
    parser.add_argument("--out", default=str(ROOT / "output"))
    args = parser.parse_args()

    backend = "fixtures" if args.dry_run else resolve_backend(args.backend)
    board = Blackboard(args.blackboard)
    result = orchestrate(board, args.dry_run, args.scenes, backend, args.script)

    if result is None:
        print("\nPipeline aborted. See run.log.", file=sys.stderr)
        return 1

    out_dir = write_outputs(result, args.out)
    print("\n" + "=" * 72)
    print(f"Unique assets      : {len(result['manifest']['assets'])}")
    print(f"Animation clips    : {len(result['animations']['animations'])}"
          f" in {len(result['animations']['capture_sessions'])} capture sessions")
    print(f"Objectives         : {len(result['runtime']['objectives'])}")
    print(f"System unlocks     : {len(result['runtime']['unlocks'])}")
    print(f"Subtitle rows      : {len(result['subtitles']['rows'])}")
    print(f"Gap findings       : {len(result['report']['findings'])}")
    print("=" * 72)
    print(f"\nGame-ready output : {out_dir}")
    print(f"Full agent trail  : {board.dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
