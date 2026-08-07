#!/usr/bin/env python3
"""
MR. MOONLIGHT — CONTENT FORGE
A RAG pipeline that generates voice and art-direction content from the game's
own GDD and Day 1 script, then criticises and corrects itself.

    python3 forge.py --dry-run          # full pipeline on fixtures, free
    python3 forge.py --quick            # live, reduced scope, cheap
    python3 forge.py                    # live, full run

Backends:
    --backend claude-code   (default) uses a Pro/Max subscription via the CLI
    --backend api           uses ANTHROPIC_API_KEY
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import kb as knowledge_base
import schemas

ROOT = Path(__file__).parent
API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
SONNET = "claude-sonnet-5"
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "claude")
CLAUDE_ARGS = ["-p"]


# ---------------------------------------------------------------------------
# Triggers — the moments in Day 1 that deserve Tracey's inner commentary.
# Each carries the retrieval query used to ground its generation.
# ---------------------------------------------------------------------------

TRIGGERS = [
    ("waking_hungover", "Waking up hungover at the campsite",
     "Tracey wakes hungover alarm vomit stamina campsite"),
    ("missing_boots", "Realising her boots are gone",
     "boots missing barefoot socks wet forest floor Rylee"),
    ("rylee_radio", "Talking to Rylee on the walkie talkie",
     "Rylee radio conversation walkie talkie jokes Glade"),
    ("inventory_full", "Backpack is full and something must be dropped",
     "inventory capacity backpack weight carry items discard"),
    ("wolves_first", "Seeing a wolf for the first time",
     "wolf wolves pack roam bite fear circling"),
    ("empty_glade", "Finding the Glade abandoned",
     "Glade abandoned belongings scattered bonfire sleeping bags friends"),
    ("the_polaroid", "Picking up the Polaroid of the group",
     "Polaroid photograph group friends camp table"),
    ("pickaxe_telescope", "Pulling the pickaxe out of the telescope",
     "pickaxe telescope frame embedded melee weapon"),
    ("bear_trap", "Stepping into or spotting a bear trap",
     "bear trap punji environmental threat health stamina pain"),
    ("cultists_first", "Seeing cultists for the first time",
     "cultist zealot spotter priest altar robes lamp whistle"),
    ("vernon_cabin", "Reaching Vernon's cabin covered in crosses",
     "Vernon cabin crosses hermit orthodox chapel religion"),
    ("holly_reunion", "Finding Holly alive at Vernon's cabin",
     "Holly cabin reunion marijuana friend alive relief"),
    ("scott_radio", "Hearing Scott in distress over the radio",
     "Scott radio transmission distress mine trapped Shannon panic"),
    ("the_mine", "Going into the mine in the dark",
     "mine mineshaft dark lamp linear route infirmary"),
    ("finding_scott", "Finding Scott unconscious",
     "Scott unconscious infirmary stretcher rescue first aid"),
    ("nightfall", "Night falling with shelter still far away",
     "night darkness three am shelter North Star deadline island shifts"),
]


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------

def resolve_backend(requested):
    if requested == "auto":
        if shutil.which(CLAUDE_BIN):
            return "claude-code"
        if os.environ.get("ANTHROPIC_API_KEY"):
            return "api"
        raise SystemExit("No backend available. Install Claude Code, set "
                         "ANTHROPIC_API_KEY, or use --dry-run.")
    if requested == "claude-code" and not shutil.which(CLAUDE_BIN):
        raise SystemExit(f"'{CLAUDE_BIN}' is not on your PATH. Use --backend api "
                         "or --dry-run.")
    if requested == "api" and not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY is not set. Use --backend claude-code "
                         "or --dry-run.")
    return requested


# Claude Code invocation strategies, tried in order. The CLI is a shim on
# Windows and its stdin handling varies by version and shell, so rather than
# assuming one calling convention we probe once and remember what worked.
_CC_STRATEGY = None

CC_STRATEGIES = [
    ("stdin",        "prompt on stdin, argv list"),
    ("argv",         "prompt as a command-line argument"),
    ("stdin_shell",  "prompt on stdin, through the shell"),
]

MAX_ARGV_CHARS = 6000          # Windows cmd.exe caps a command line near 8191


def _run_claude(strategy, prompt, timeout=900):
    """Return (ok, stdout, stderr, detail)."""
    if strategy == "stdin":
        done = subprocess.run([CLAUDE_BIN] + CLAUDE_ARGS, input=prompt,
                              capture_output=True, text=True, timeout=timeout)
    elif strategy == "argv":
        if len(prompt) > MAX_ARGV_CHARS:
            return False, "", "", "prompt too long for a command-line argument"
        done = subprocess.run([CLAUDE_BIN] + CLAUDE_ARGS + [prompt],
                              capture_output=True, text=True, timeout=timeout)
    elif strategy == "stdin_shell":
        done = subprocess.run(" ".join([CLAUDE_BIN] + CLAUDE_ARGS), input=prompt,
                              capture_output=True, text=True, timeout=timeout,
                              shell=True)
    else:
        return False, "", "", f"unknown strategy {strategy}"

    ok = done.returncode == 0 and done.stdout.strip()
    detail = f"exit {done.returncode}"
    return bool(ok), done.stdout, done.stderr, detail


def probe_claude_code(verbose=True):
    """Find a working invocation. Returns the strategy name or None."""
    global _CC_STRATEGY
    if _CC_STRATEGY:
        return _CC_STRATEGY

    resolved = shutil.which(CLAUDE_BIN)
    if verbose:
        print(f"  binary resolved to : {resolved}")

    probe = "Reply with exactly this word and nothing else: OK"
    for name, description in CC_STRATEGIES:
        try:
            ok, out, err, detail = _run_claude(name, probe, timeout=120)
        except FileNotFoundError:
            if verbose:
                print(f"  {name:12} FAILED   binary not executable")
            continue
        except subprocess.TimeoutExpired:
            if verbose:
                print(f"  {name:12} FAILED   timed out")
            continue
        if ok:
            if verbose:
                print(f"  {name:12} OK       ({description}) -> {out.strip()[:40]!r}")
            _CC_STRATEGY = name
            return name
        if verbose:
            message = (err.strip() or out.strip() or "no output at all")
            print(f"  {name:12} FAILED   {detail}: {message[:160]}")
    return None


def call_model(system_prompt, user_prompt, backend, max_tokens=8000):
    if backend == "claude-code":
        prompt = f"{system_prompt}\n\n{user_prompt}"
        strategy = probe_claude_code(verbose=False)
        if strategy is None:
            raise SystemExit(
                "Claude Code is installed but no invocation worked.\n"
                "Run this for the full picture:\n"
                "    python3 forge.py --test-backend\n\n"
                "Most common cause: Claude Code has not been trusted in this\n"
                "folder yet. Run 'claude' on its own here once, accept the\n"
                "prompt, type /exit, then retry.\n"
                "Otherwise use:  python3 forge.py --backend api")

        try:
            ok, out, err, detail = _run_claude(strategy, prompt)
        except subprocess.TimeoutExpired:
            raise SystemExit("Claude Code timed out after 15 minutes.")

        if not ok:
            raise SystemExit(
                f"Claude Code failed ({detail}) using the '{strategy}' strategy.\n"
                f"stdout: {out.strip()[:500] or '<empty>'}\n"
                f"stderr: {err.strip()[:500] or '<empty>'}\n\n"
                f"Prompt was {len(prompt)} characters.\n"
                "Run 'python3 forge.py --test-backend' to re-probe, or switch to\n"
                "'--backend api'.")
        return out, len(prompt) // 4, len(out) // 4

    body = json.dumps({"model": SONNET, "max_tokens": max_tokens,
                       "system": system_prompt,
                       "messages": [{"role": "user", "content": user_prompt}]}).encode()
    request = urllib.request.Request(API_URL, data=body, headers={
        "content-type": "application/json",
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": API_VERSION})
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            data = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"API error {exc.code}: {exc.read().decode()[:500]}")
    text = "".join(b.get("text", "") for b in data.get("content", []))
    usage = data.get("usage", {})
    return text, usage.get("input_tokens", 0), usage.get("output_tokens", 0)


def parse_json(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.rstrip().endswith("```"):
            cleaned = cleaned.rstrip()[:-3]
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1:
        raise ValueError(f"No JSON in output: {text[:300]}")
    return json.loads(cleaned[start:end + 1])


# ---------------------------------------------------------------------------
# Agent prompts
# ---------------------------------------------------------------------------

TRACEY_VOICE = """Tracey is the player character of Mr. Moonlight.

Twenty-something, 1978, remote Alaskan island. History major who dropped out.
Functional addict. Grumpy, foul-mouthed, allergic to sincerity. She deflects
everything with a joke that is usually at her own expense or someone else's.
Underneath it she is frightened and will not say so.

Her register: short, dry, profane, specific. She notices ugly practical details
rather than atmosphere. She talks to herself the way someone talks to themselves
when nobody has heard them in hours."""

VOICE_WRITER = """You write Tracey's inner monologue for Mr. Moonlight.

""" + TRACEY_VOICE + """

You will be given a trigger moment and retrieved context from the game's own
design document and Day 1 script. Write THOUGHT lines: inner monologue with no
audio, shown on screen as a subtitle in the style of Silent Hill 1.

Hard rules:
- Exactly ten lines. Every line is a complete standalone thought.
- One line each. Under about 60 characters where possible, hard maximum 90,
  because it has to fit a single subtitle line.
- 1978. No anachronism. No modern slang, no internet-era phrasing, no therapy
  vocabulary. She would not say "trauma", "boundaries", "processing" or "vibe".
- Profanity is in character and welcome, but it is seasoning, not the joke.
  Do not make every line a swear. Around a third is right.
- Vary the shape. Some lines are observations, some are complaints, some are
  jokes, at least one should land somewhere uncomfortable and honest.
- Never explain the plot. She already knows where she is.
- Do not reference anything the retrieved context does not support.

Return ONLY JSON, no prose and no markdown fences:
  {"trigger": "<id>", "lines": ["...", ... ten strings ...]}"""

STAGE_DIRECTOR = """You prepare a recording script for voice actors on
Mr. Moonlight.

""" + TRACEY_VOICE + """

You are given one scene: its retrieved script events and the dialogue already
extracted from it, verbatim, in order. Your job is the material AROUND the
dialogue, never the dialogue itself.

Produce:
- A short scene setting, two or three sentences. Where we are, what has just
  happened, what state the character is in. Written for a performer who has
  never seen the game.
- Brief stage directions to place between lines where a performer genuinely
  needs them: a physical action, a shift of state, a pause that changes a
  reading. Reference the dialogue by its line id. Do not direct every line.
  Silence is a choice; over-direction is worse than none.

Never rewrite, paraphrase, trim or "improve" a line of dialogue. The text is
fixed. You are writing what surrounds it.

Return ONLY JSON, no prose and no markdown fences:
  {"setting": "...",
   "directions": [{"before_line_id": "<id>", "direction": "..."}]}"""

PROP_MASTER = """You are the prop master for Mr. Moonlight, a first-person
survival horror game set on a remote Alaskan island in 1978.

Art direction: low poly in the manner of the PS1 and N64, pixelated low
resolution textures, strongly defined silhouettes so objects read in darkness,
a cold high contrast palette of green, grey and brown.

Given a scene's retrieved script events and the game's art direction, propose the
3D props that scene needs. Be practical. This is a solo developer with roughly
five weeks, so a prop that takes a day to model had better earn it.

For each prop give:
  name           what it is, plainly
  category       one of: environment, set_dressing, interactable, weapon, light_source
  in_source      "explicit" if the script or GDD names it, "inferred" if you are
                 proposing it. Be honest about which.
  why            one line on what it does for the scene
  modelling_note one line on the low poly approach, or reuse if it repeats

Rules:
- 1978. No anachronism.
- Prefer reuse. Say so when a prop repeats from an earlier scene.
- Between six and twelve props per scene. Do not pad.

Return ONLY JSON, no prose and no markdown fences:
  {"scene": "<scene id>", "props": [{...}, ...]}"""

CONSISTENCY_AGENT = """You are the consistency critic for Mr. Moonlight.

You are given generated content and the retrieved passages from the game's own
GDD and Day 1 script that the content was supposed to be grounded in. Your job
is to find where the generated content contradicts the source, drifts out of
period, or breaks the established voice — and to correct it.

Check for:
1. LORE BREAK. A fact contradicting the GDD or script: wrong character,
   wrong location, wrong year, an object that does not exist in the game, an
   event that does not happen.
2. PERIOD BREAK. Anachronistic vocabulary, technology or attitude for 1978.
3. TONE DRIFT. Lines that sound like a generic horror protagonist rather than
   Tracey specifically. Sincerity where she would deflect, eloquence where she
   would be blunt, therapy language, self-aware genre commentary.
4. CROSS-DOCUMENT CONTRADICTION. Where two of the project's own documents
   disagree with each other. Report these even when the generated content is
   faithful to one of them, because the developer needs to know.

For every finding you MUST supply an exact correction: the offending text as it
appears, and the replacement. The replacement must be a drop-in substitute of
similar length that fixes the problem without introducing a new one.

Be specific and be sparing. A report with four real findings is worth more than
one with twenty padded ones.

Return ONLY JSON, no prose and no markdown fences:
  {"findings": [{"severity": "BLOCKER|WARNING|NOTE",
                 "category": "lore_break|period_break|tone_drift|cross_document",
                 "file": "<which output file>",
                 "offending_text": "<exact text to replace>",
                 "corrected_text": "<replacement>",
                 "source_basis": "<which retrieved chunk justifies this>",
                 "explanation": "<why it is wrong>"}],
   "method": "<two or three sentences on how you checked>",
   "summary": "<one paragraph a developer can read in ten seconds>"}"""

VOICE_JUDGE = """You are a voice director assessing whether generated content is
actually performable, for Mr. Moonlight.

""" + TRACEY_VOICE + """

You are given generated thought lines and a voice recording script. Judge them
the way a director judges material before a session, not the way a writer admires
their own work. Be blunt. Flattery here costs the production money.

Assess:
1. SPEAKABILITY. Can an actor say this in one breath, in character? Tongue
   twisters, unnatural clause order, written-not-spoken syntax.
2. SUBTITLE FIT. Thought lines display as a single subtitle line. Anything much
   over 60 characters is a problem.
3. VOICE CONSISTENCY. Does this sound like one person, or like a writer doing an
   impression of a grumpy character? Name the lines that miss.
4. RANGE. Ten lines for one trigger that are all the same joke give an actor
   nothing. Is there variation in shape and intent?
5. DIRECTION QUALITY. Are the stage directions actionable, or vague mood words?

Then, and this is the important part, propose ONE concrete amendment to the
writer's prompt that would most improve the next generation. Not "be more
authentic" — an instruction specific enough to change the output, for example
"at least two of the ten lines must contain no profanity and no joke" or "no line
may begin with the word I". Name the weakest trigger so it can be regenerated.

Return ONLY JSON, no prose and no markdown fences:
  {"verdict": "READY|NEEDS_WORK|NOT_USABLE",
   "assessment": {"speakability": "...", "subtitle_fit": "...",
                  "voice_consistency": "...", "range": "...",
                  "direction_quality": "..."},
   "weakest_lines": [{"trigger": "...", "line": "...", "problem": "..."}],
   "weakest_trigger": "<trigger id to regenerate>",
   "prompt_amendment": "<one instruction to append to the writer's prompt>",
   "summary": "<one paragraph>"}"""


# ---------------------------------------------------------------------------
# Deterministic script extraction
# ---------------------------------------------------------------------------

EVENT_RE = re.compile(r"^(L\d+E-\d+)\s*\|\|\s*([^|]+?)\s*\|\|\s*(.*)$")


def parse_params(rest):
    params = {}
    for field in rest.split("||"):
        if ":" in field:
            key, value = field.split(":", 1)
            params[key.strip()] = value.strip()
    return params


def extract_dialogue(script_text):
    """Pull voiced dialogue out of the SLDD script, verbatim, grouped by scene.

    This is deliberately deterministic. The words an actor will say are lifted
    straight from the script and never pass through a model, because a model that
    'improves' a line silently is worse than useless in a recording script.
    """
    speakers = dict(re.findall(r"^([A-Z][A-Z-]*)\s*=\s*(\S.*?)\s*$", script_text, re.M))
    scenes, current = [], None

    for line in script_text.splitlines():
        banner = re.search(r"SCENE\s+(\d+)\s+—\s+(.+?)\s*$", line)
        if banner:
            current = {"number": int(banner.group(1)),
                       "title": banner.group(2).replace("[OUTLINE]", "").strip(),
                       "lines": []}
            scenes.append(current)
            continue
        match = EVENT_RE.match(line.strip())
        if not match or current is None:
            continue
        event_id, event_type, rest = match.groups()
        if not event_type.startswith("D:"):
            continue
        params = parse_params(rest)
        text = params.get("Line", "N/A")
        if text in ("", "N/A"):
            continue
        abbreviation = event_type.split(":", 1)[1]
        current["lines"].append({
            "id": event_id,
            "speaker": speakers.get(abbreviation, abbreviation),
            "text": text,
            "tone": params.get("Tone", "N/A"),
        })

    return [s for s in scenes if s["lines"]]


def scene_events(script_text, scene_number, limit=60):
    """Raw events for one scene, for the prop master and stage director."""
    collected, inside = [], False
    for line in script_text.splitlines():
        banner = re.search(r"SCENE\s+(\d+)\s+—", line)
        if banner:
            inside = int(banner.group(1)) == scene_number
            continue
        if inside and EVENT_RE.match(line.strip()):
            collected.append(line.strip())
    return "\n".join(collected[:limit])


# ---------------------------------------------------------------------------
# Fixtures for --dry-run
# ---------------------------------------------------------------------------

def fixture(kind, **kwargs):
    if kind == "lines":
        return {"trigger": kwargs["trigger"],
                "lines": [f"Dry run line {i} for {kwargs['trigger']}." for i in range(1, 11)]}
    if kind == "stage":
        return {"setting": "Dry-run setting. No model judgment was applied.",
                "directions": [{"before_line_id": kwargs.get("first_id", "N/A"),
                                "direction": "Dry-run direction."}]}
    if kind == "props":
        return {"scene": kwargs["scene"],
                "props": [{"name": f"Dry-run prop {i}", "category": "set_dressing",
                           "in_source": "inferred", "why": "Fixture.",
                           "modelling_note": "Fixture."} for i in range(1, 7)]}
    if kind == "consistency":
        return {"findings": [{
            "severity": "WARNING", "category": "cross_document",
            "file": "01_thought_lines.md",
            "offending_text": "Dry run line 1 for waking_hungover.",
            "corrected_text": "Dry run line 1 for waking_hungover, corrected.",
            "source_basis": "GDD#010",
            "explanation": "Dry-run fixture correction, to exercise the apply loop."}],
            "method": "Dry run. No retrieval judgment was applied.",
            "summary": "Dry run completed."}
    return {"verdict": "NEEDS_WORK",
            "assessment": {k: "Dry run." for k in
                           ("speakability", "subtitle_fit", "voice_consistency",
                            "range", "direction_quality")},
            "weakest_lines": [{"trigger": "waking_hungover", "line": "Dry run line 1.",
                               "problem": "Fixture."}],
            "weakest_trigger": "waking_hungover",
            "prompt_amendment": "At least two of the ten lines must contain no "
                                "profanity and no joke.",
            "summary": "Dry run completed."}


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

class Forge:
    def __init__(self, backend, dry_run, quick, out_dir):
        self.backend = backend
        self.dry_run = dry_run
        self.quick = quick
        self.out = Path(out_dir)
        self.out.mkdir(parents=True, exist_ok=True)
        self.kb = knowledge_base.KnowledgeBase(ROOT / "knowledge")
        self.script = (ROOT / "knowledge" / "L01.txt").read_text(encoding="utf-8")
        self.tokens_in = self.tokens_out = self.calls = 0
        self.log_lines = []

    def log(self, kind, message):
        line = f"[{time.strftime('%H:%M:%S')}] {kind:<11} {message}"
        self.log_lines.append(line)
        print(line, flush=True)

    def ask(self, system, user, label, fixture_kind=None, **fixture_kwargs):
        self.log("DISPATCH", label)
        if self.dry_run:
            return fixture(fixture_kind, **fixture_kwargs)
        text, tin, tout = call_model(system, user, self.backend)
        self.calls += 1
        self.tokens_in += tin
        self.tokens_out += tout
        self.log("TOKENS", f"{label}: {tin} in / {tout} out")
        return parse_json(text)

    # -- stage 1: thought lines ---------------------------------------------
    def thought_lines(self, extra_instruction=""):
        triggers = TRIGGERS[:4] if self.quick else TRIGGERS
        system = VOICE_WRITER + (f"\n\nADDITIONAL INSTRUCTION:\n{extra_instruction}"
                                 if extra_instruction else "")
        results = []
        for trigger_id, label, query in triggers:
            chunks = self.kb.retrieve(query, top_k=4, purpose=f"thought:{trigger_id}")
            user = (f"TRIGGER: {trigger_id} — {label}\n\n"
                    f"RETRIEVED CONTEXT:\n{self.kb.as_context(chunks)}\n\n"
                    f"Write exactly ten thought lines for this moment.")
            payload = self.ask(system, user, f"Voice writer — {trigger_id}",
                               "lines", trigger=trigger_id)
            payload["label"] = label
            payload["retrieved_ids"] = [c["id"] for c in chunks]
            errors = schemas.validate_lines(payload)
            if errors:
                self.log("GATE", f"{trigger_id}: {len(errors)} issue(s)")
                for e in errors[:3]:
                    self.log("GATE", f"  - {e}")
            results.append(payload)
            self.kb.attach_output(f"thought:{trigger_id}",
                                  " / ".join(payload["lines"][:3]))
        return results

    # -- stage 2: voice recording script ------------------------------------
    def voice_script(self):
        scenes = extract_dialogue(self.script)
        if self.quick:
            scenes = scenes[:3]
        self.log("EXTRACT", f"{sum(len(s['lines']) for s in scenes)} voiced lines "
                            f"across {len(scenes)} scenes (deterministic)")
        for scene in scenes:
            query = f"scene {scene['number']} {scene['title']}"
            chunks = self.kb.retrieve(query, top_k=3,
                                      purpose=f"stage:{scene['number']}")
            dialogue = "\n".join(f"{l['id']} | {l['speaker']}: {l['text']}"
                                 for l in scene["lines"])
            user = (f"SCENE {scene['number']:02d} — {scene['title']}\n\n"
                    f"RETRIEVED CONTEXT:\n{self.kb.as_context(chunks, 3500)}\n\n"
                    f"SCENE EVENTS:\n{scene_events(self.script, scene['number'], 40)}\n\n"
                    f"DIALOGUE, VERBATIM AND FIXED:\n{dialogue}")
            payload = self.ask(STAGE_DIRECTOR, user,
                               f"Stage director — scene {scene['number']:02d}",
                               "stage", first_id=scene["lines"][0]["id"])
            scene["setting"] = payload.get("setting", "")
            scene["directions"] = payload.get("directions", [])
            self.kb.attach_output(f"stage:{scene['number']}", scene["setting"][:300])
        return scenes

    # -- stage 3: props -----------------------------------------------------
    def props(self):
        numbers = sorted({int(m) for m in re.findall(r"SCENE\s+(\d+)\s+—", self.script)})
        if self.quick:
            numbers = numbers[:3]
        results = []
        for number in numbers:
            query = f"scene {number} props location environment art style low poly"
            chunks = self.kb.retrieve(query, top_k=4, purpose=f"props:{number}")
            user = (f"SCENE {number:02d}\n\n"
                    f"RETRIEVED CONTEXT:\n{self.kb.as_context(chunks, 3500)}\n\n"
                    f"SCENE EVENTS:\n{scene_events(self.script, number, 45)}")
            payload = self.ask(PROP_MASTER, user, f"Prop master — scene {number:02d}",
                               "props", scene=f"{number:02d}")
            payload["scene_number"] = number
            results.append(payload)
            self.kb.attach_output(f"props:{number}",
                                  ", ".join(p["name"] for p in payload.get("props", [])[:5]))
        return results

    # -- stage 4: consistency critic and correction --------------------------
    def consistency(self, lines, scenes, prop_sets):
        chunks = self.kb.retrieve(
            "Tracey character personality 1978 Alaska cult art style themes",
            top_k=6, purpose="consistency")
        sample_lines = "\n".join(
            f"[{group['trigger']}] " + " | ".join(group["lines"])
            for group in lines)
        sample_props = "\n".join(
            f"Scene {p['scene_number']:02d}: " +
            ", ".join(pr["name"] for pr in p.get("props", []))
            for p in prop_sets)
        sample_settings = "\n".join(
            f"Scene {s['number']:02d}: {s.get('setting','')}" for s in scenes)

        user = (f"RETRIEVED SOURCE OF TRUTH:\n{self.kb.as_context(chunks, 6000)}\n\n"
                f"=== 01_thought_lines.md ===\n{sample_lines}\n\n"
                f"=== 02_voice_script.md (settings only) ===\n{sample_settings}\n\n"
                f"=== 03_prop_list.md ===\n{sample_props}")
        report = self.ask(CONSISTENCY_AGENT, user, "Consistency agent",
                          "consistency")
        self.kb.attach_output("consistency", report.get("summary", "")[:400])
        return report

    def apply_corrections(self, report, lines, scenes, prop_sets):
        """Apply each correction by exact substitution, and record before/after.

        Substitution is done in Python rather than by asking a model to rewrite
        the file, so the change is exactly what the critic asked for and the
        before/after shown in the report is the literal diff.
        """
        applied = []
        for finding in report.get("findings", []):
            bad = finding.get("offending_text", "")
            good = finding.get("corrected_text", "")
            if not bad or not good:
                continue
            hit = False
            for group in lines:
                for index, line in enumerate(group["lines"]):
                    if bad.strip() and bad.strip() in line:
                        group["lines"][index] = line.replace(bad.strip(), good.strip())
                        hit = True
            for scene in scenes:
                if bad.strip() and bad.strip() in scene.get("setting", ""):
                    scene["setting"] = scene["setting"].replace(bad.strip(), good.strip())
                    hit = True
            for group in prop_sets:
                for prop in group.get("props", []):
                    for field in ("name", "why", "modelling_note"):
                        if bad.strip() and bad.strip() in prop.get(field, ""):
                            prop[field] = prop[field].replace(bad.strip(), good.strip())
                            hit = True
            finding["applied"] = hit
            if hit:
                applied.append(finding)
                self.log("CORRECTED", f"{finding['category']}: "
                                      f"{bad[:45]!r} -> {good[:45]!r}")
            else:
                self.log("SKIPPED", f"could not locate: {bad[:55]!r}")
        return applied

    # -- stage 5: voice judgment and prompt tweak ----------------------------
    def voice_judgment(self, lines, scenes):
        sample = "\n".join(f"[{g['trigger']}]\n" + "\n".join(f"  {l}" for l in g["lines"])
                           for g in lines)
        directions = "\n".join(
            f"Scene {s['number']:02d}: {s.get('setting','')}\n" +
            "\n".join(f"  ({d.get('direction','')})" for d in s.get("directions", []))
            for s in scenes)
        user = (f"=== THOUGHT LINES ===\n{sample}\n\n"
                f"=== VOICE SCRIPT SETTINGS AND DIRECTIONS ===\n{directions}")
        return self.ask(VOICE_JUDGE, user, "Voice judgment agent", "voice")


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_thought_lines(groups, show_ids=False):
    out = ["# Miscellaneous Thought Lines — Tracey", "",
           "Inner monologue, no audio, displayed as a single subtitle line in the",
           "style of Silent Hill 1. Grouped by the moment that triggers them.", "",
           f"_{len(groups)} triggers, {sum(len(g['lines']) for g in groups)} lines._", ""]
    for group in groups:
        out += [f"## {group.get('label', group['trigger'])}", ""]
        if show_ids:
            out += [f"`trigger: {group['trigger']}` · grounded in "
                    f"{', '.join(group.get('retrieved_ids', []))}", ""]
        out += [f"{i}. {line}" for i, line in enumerate(group["lines"], 1)]
        out.append("")
    return "\n".join(out)


def render_voice_script(scenes, show_ids=False):
    cast = sorted({l["speaker"] for s in scenes for l in s["lines"]})
    out = ["# Mr. Moonlight — Day 1", "## Voice recording script", "",
           "Dialogue is reproduced verbatim from the level script and has not been",
           "altered. Settings and directions are written for performance context.",
           "", "**Cast:** " + " · ".join(cast), "",
           f"_{sum(len(s['lines']) for s in scenes)} lines across "
           f"{len(scenes)} scenes._", "",
           "---", ""]
    for scene in scenes:
        out += [f"## Scene {scene['number']:02d} — {scene['title'].title()}", ""]
        if scene.get("setting"):
            out += [f"*{scene['setting']}*", ""]
        # Keyed by index, not by event ID: the script can contain duplicate
        # event IDs (L01E-165 appears twice in scene 06), and keying by ID
        # silently drops or misplaces a direction when that happens.
        directions = {d.get("before_index"): d.get("direction", "")
                      for d in scene.get("directions", [])
                      if d.get("before_index") is not None}
        for position, line in enumerate(scene["lines"]):
            if position in directions:
                out += [f"> ({directions[position]})", ""]
            tone = line["tone"]
            suffix = f"  `{line['id']}`" if show_ids else ""
            if tone and tone != "N/A":
                out.append(f"**{line['speaker'].upper()}**  *({tone})*{suffix}")
            else:
                out.append(f"**{line['speaker'].upper()}**{suffix}")
            out += [f"> {line['text']}", ""]
        out += ["---", ""]
    return "\n".join(out)


def render_props(prop_sets, scene_titles):
    out = ["# Prop List by Scene", "",
           "Low poly, PS1 and N64 era. Pixelated textures, strong silhouettes,",
           "cold high contrast palette. `explicit` means the script or GDD names it;",
           "`inferred` means the prop master is proposing it.", ""]
    total = sum(len(p.get("props", [])) for p in prop_sets)
    explicit = sum(1 for p in prop_sets for pr in p.get("props", [])
                   if pr.get("in_source") == "explicit")
    out += [f"_{total} props across {len(prop_sets)} scenes; {explicit} named in "
            f"source, {total - explicit} proposed._", ""]
    for group in prop_sets:
        number = group["scene_number"]
        out += [f"## Scene {number:02d} — {scene_titles.get(number, '').title()}", "",
                "| Prop | Category | Source | Why | Modelling |",
                "|---|---|---|---|---|"]
        for prop in group.get("props", []):
            out.append("| {} | `{}` | `{}` | {} | {} |".format(
                prop.get("name", ""), prop.get("category", ""),
                prop.get("in_source", ""), prop.get("why", ""),
                prop.get("modelling_note", "")))
        out.append("")
    return "\n".join(out)


def render_consistency(report, applied):
    out = ["# Consistency Report", "",
           "Produced by the Consistency Agent. Every generated output was checked",
           "against retrieved passages from the GDD and the Day 1 script.", "",
           "## Method", "", report.get("method", "").strip(), "",
           "## Summary", "", report.get("summary", "").strip(), ""]

    findings = report.get("findings", [])
    out += [f"## Findings ({len(findings)})", ""]
    if not findings:
        out += ["No inconsistencies found.", ""]
    for order in ("BLOCKER", "WARNING", "NOTE"):
        group = [f for f in findings if f.get("severity") == order]
        if not group:
            continue
        out += [f"### {order} ({len(group)})", ""]
        for finding in group:
            out += [f"**{finding.get('category', '')}** in `{finding.get('file', '')}`",
                    "", f"- **Basis:** {finding.get('source_basis', 'N/A')}",
                    f"- **Problem:** {finding.get('explanation', '')}",
                    f"- **Applied:** {'yes' if finding.get('applied') else 'no — text not located'}",
                    "", "```diff",
                    f"- {finding.get('offending_text', '')}",
                    f"+ {finding.get('corrected_text', '')}", "```", ""]

    out += ["## Corrections actually applied", "",
            f"{len(applied)} of {len(findings)} findings were applied to the output "
            f"files by exact substitution in Python, so the diff above is the "
            f"literal change made.", ""]
    return "\n".join(out)


def render_voice_critique(report, before, after, amendment, trigger):
    out = ["# Voice Judgment Critique", "",
           "Produced by the Voice Judgment Agent, assessing whether the generated",
           "content is performable rather than merely well written.", "",
           f"## Verdict: {report.get('verdict', 'N/A')}", "",
           report.get("summary", "").strip(), "", "## Assessment", ""]
    for key, label in (("speakability", "Speakability"),
                       ("subtitle_fit", "Subtitle fit"),
                       ("voice_consistency", "Voice consistency"),
                       ("range", "Range"),
                       ("direction_quality", "Direction quality")):
        out += [f"### {label}", "", report.get("assessment", {}).get(key, ""), ""]

    weakest = report.get("weakest_lines", [])
    if weakest:
        out += ["## Lines that miss", "", "| Trigger | Line | Problem |", "|---|---|---|"]
        for item in weakest:
            out.append("| `{}` | {} | {} |".format(
                item.get("trigger", ""), item.get("line", ""), item.get("problem", "")))
        out.append("")

    out += ["## The tweak that was made", "",
            "The agent was required to propose one concrete, actionable amendment to",
            "the writer's prompt. The pipeline then applied it and regenerated the",
            "weakest trigger, so the effect is shown rather than asserted.", "",
            f"**Trigger regenerated:** `{trigger}`", "",
            "**Amendment appended to the writer's system prompt:**", "",
            f"> {amendment}", "", "### Before", ""]
    out += [f"{i}. {line}" for i, line in enumerate(before, 1)]
    out += ["", "### After", ""]
    out += [f"{i}. {line}" for i, line in enumerate(after, 1)]
    out.append("")
    return "\n".join(out)


def render_rag_trace(trace, stats):
    out = ["# RAG Retrieval Trace", "",
           "Every retrieval the pipeline performed, with the query, the chunks BM25",
           "returned, and the output produced from them. This is the evidence that",
           "generation is grounded in the game's own documents.", "",
           "## Index", "",
           f"- Chunks: **{stats['total_chunks']}** "
           f"({stats['gdd_chunks']} from the GDD, {stats['script_chunks']} from L01)",
           f"- Average chunk size: {stats['avg_chunk_chars']} characters",
           "- Retrieval: BM25 sparse, k1=1.5, b=0.75, stopword-filtered",
           "- Deterministic: the same query always returns the same chunks", ""]

    for index, entry in enumerate(trace, 1):
        out += [f"---", "", f"## {index}. `{entry['purpose']}`", "",
                "**Query**", "", f"```\n{entry['query']}\n```", "",
                "**Retrieved chunks**", ""]
        for chunk in entry["retrieved"]:
            out += [f"<details><summary><code>{chunk['id']}</code> · "
                    f"{chunk['section']} · score {chunk['score']} · matched: "
                    f"{', '.join(chunk['matched_terms'][:8])}</summary>", "",
                    "```", chunk["excerpt"].strip(), "```", "", "</details>", ""]
        if "output" in entry:
            out += ["**Output produced from these chunks**", "",
                    f"> {entry['output']}", ""]
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Mr. Moonlight Content Forge")
    parser.add_argument("--backend", choices=["claude-code", "api", "auto"],
                        default="claude-code")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--quick", action="store_true",
                        help="4 triggers and 3 scenes instead of the full set.")
    parser.add_argument("--test-backend", action="store_true",
                        help="Probe the Claude Code CLI and report what works. "
                             "Sends one tiny prompt. Run this first if a live run "
                             "fails.")
    parser.add_argument("--with-ids", action="store_true",
                        help="Keep event and chunk IDs in the deliverables. Off by "
                             "default: the voice script and thought lines are "
                             "production documents, and 06_rag_trace.md already "
                             "carries the grounding evidence.")
    parser.add_argument("--out", default=str(ROOT / "output"))
    args = parser.parse_args()

    if args.test_backend:
        print("Testing the Claude Code backend.\n")
        print(f"  CLAUDE_BIN         : {CLAUDE_BIN}")
        print(f"  CLAUDE_ARGS        : {CLAUDE_ARGS}")
        found = probe_claude_code(verbose=True)
        print()
        if found:
            print(f"WORKING. Using the '{found}' strategy.")
            print("Run:  python3 forge.py --quick")
            return 0
        print("No invocation worked. Things to try, in order:\n")
        print("  1. Trust the folder. Claude Code refuses non-interactive runs in")
        print("     an untrusted directory. Run 'claude' here on its own, accept")
        print("     the prompt, type /exit, then retry.")
        print("  2. Check you are signed in:  claude   then  /status")
        print("  3. Check the flag exists:    claude --help | grep -i print")
        print("     If your version uses something other than -p, edit CLAUDE_ARGS")
        print("     at the top of forge.py.")
        print("  4. Fall back to the API:     python3 forge.py --backend api")
        return 1

    backend = "fixtures" if args.dry_run else resolve_backend(args.backend)
    forge = Forge(backend, args.dry_run, args.quick, args.out)
    forge.log("START", f"Content Forge — backend={backend}"
                       f"{' (quick)' if args.quick else ''}")
    forge.log("INDEX", json.dumps(forge.kb.stats()))

    lines = forge.thought_lines()
    scenes = forge.voice_script()
    prop_sets = forge.props()

    report = forge.consistency(lines, scenes, prop_sets)
    applied = forge.apply_corrections(report, lines, scenes, prop_sets)
    forge.log("CONSISTENCY", f"{len(report.get('findings', []))} finding(s), "
                             f"{len(applied)} applied")

    critique = forge.voice_judgment(lines, scenes)
    amendment = critique.get("prompt_amendment", "")
    weakest = critique.get("weakest_trigger") or lines[0]["trigger"]
    forge.log("VOICE", f"verdict={critique.get('verdict')} — regenerating "
                       f"'{weakest}' with the proposed amendment")

    before_group = next((g for g in lines if g["trigger"] == weakest), lines[0])
    before = list(before_group["lines"])
    trigger_spec = next((t for t in TRIGGERS if t[0] == weakest), TRIGGERS[0])
    chunks = forge.kb.retrieve(trigger_spec[2], top_k=4,
                               purpose=f"retweak:{weakest}")
    system = VOICE_WRITER + f"\n\nADDITIONAL INSTRUCTION:\n{amendment}"
    user = (f"TRIGGER: {trigger_spec[0]} — {trigger_spec[1]}\n\n"
            f"RETRIEVED CONTEXT:\n{forge.kb.as_context(chunks)}\n\n"
            f"Write exactly ten thought lines for this moment.")
    regenerated = forge.ask(system, user, f"Voice writer v2 — {weakest}",
                            "lines", trigger=weakest)
    after = regenerated["lines"]
    before_group["lines"] = after
    forge.kb.attach_output(f"retweak:{weakest}", " / ".join(after[:3]))

    scene_titles = {s["number"]: s["title"] for s in scenes}
    out = Path(args.out)
    files = {
        "01_thought_lines.md": render_thought_lines(lines, args.with_ids),
        "02_voice_script.md": render_voice_script(scenes, args.with_ids),
        "03_prop_list.md": render_props(prop_sets, scene_titles),
        "04_consistency_report.md": render_consistency(report, applied),
        "05_voice_critique.md": render_voice_critique(
            critique, before, after, amendment, weakest),
        "06_rag_trace.md": render_rag_trace(forge.kb.trace, forge.kb.stats()),
    }
    if args.dry_run:
        banner = (
            "> # \u26a0\ufe0f  FIXTURE OUTPUT — NOT REAL CONTENT\n"
            "> \n"
            "> This file was produced by `--dry-run`, which exercises the whole\n"
            "> pipeline using canned placeholder data and calls no model at all.\n"
            "> Every line below is a fixture.\n"
            "> \n"
            "> For real content run: `python3 forge.py --quick` (cheap) or\n"
            "> `python3 forge.py` (full).\n\n---\n\n")
        files = {name: banner + body for name, body in files.items()}

    for name, body in files.items():
        (out / name).write_text(body, encoding="utf-8")

    forge.kb.dump_trace(out / "rag_trace.json")
    (out / "run.log").write_text("\n".join(forge.log_lines), encoding="utf-8")

    forge.log("DONE", f"{forge.calls} model calls, "
                      f"{forge.tokens_in} in / {forge.tokens_out} out")
    print("\n" + "=" * 72)
    if args.dry_run:
        print("  DRY RUN — the six files below contain FIXTURE data, not real")
        print("  content. No model was called. Run without --dry-run for output")
        print("  you can actually use:")
        print("      python3 forge.py --quick     (cheap, reduced scope)")
        print("      python3 forge.py             (full run)")
        print("=" * 72)
    for name in files:
        print(f"  {name}")
    print("=" * 72)
    print(f"\nOutput: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
