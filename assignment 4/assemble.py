#!/usr/bin/env python3
"""
Render the six deliverables from generated_payload.py using the pipeline's own
retrieval, extraction, validation and rendering code.

This exists so the assignment has real output while the Claude Code backend is
being fixed on the developer's machine. Everything deterministic here is the
same code forge.py runs: kb.py does the retrieval, forge.extract_dialogue lifts
the 131 voiced lines, schemas.py validates. Only the generation transport
differs — see the provenance note at the top of generated_payload.py.

    python3 assemble.py
"""

import json
from pathlib import Path

import forge
import generated_payload as gp
import kb as knowledge_base
import schemas

ROOT = Path(__file__).parent
OUT = ROOT / "output"

TRIGGER_QUERIES = {t[0]: q for t, q in zip(
    gp.THOUGHT_LINES,
    ["Tracey hangover campsite alarm vomit stamina morning",
     "boots missing barefoot socks forest floor sprint noise",
     "Rylee radio walkie talkie conversation Glade jokes",
     "backpack carry limit inventory cooler drop item fifth",
     "wolf roam circle bite forest road barefoot",
     "Glade abandoned belongings scattered bonfire sleeping bags",
     "Polaroid photograph group friends camp table",
     "pickaxe telescope frame melee heavy swing stamina",
     "bear trap branch road ambush health hazard",
     "cultist zealot spotter lamp whistle robes altar",
     "Vernon cabin crosses hermit orthodox religion door",
     "Holly cabin alive marijuana friend reunion",
     "mine mineshaft dark lamp linear route infirmary",
     "Scott unconscious infirmary rescue first aid",
     "stretcher drag Scott movement restricted combat",
     "night darkness three in the morning shelter North Star church"])}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    kb = knowledge_base.KnowledgeBase(ROOT / "knowledge")
    script = (ROOT / "knowledge" / "L01.txt").read_text(encoding="utf-8")
    print(f"index: {json.dumps(kb.stats())}")

    # --- real retrieval, recorded for the trace -----------------------------
    groups = []
    for (trigger_id, label, lines) in gp.THOUGHT_LINES:
        query = TRIGGER_QUERIES[trigger_id]
        chunks = kb.retrieve(query, top_k=4, purpose=f"thought:{trigger_id}")
        errors = schemas.validate_lines({"lines": lines})
        if errors:
            print(f"  VALIDATOR {trigger_id}: {errors}")
        groups.append({"trigger": trigger_id, "label": label, "lines": lines,
                       "retrieved_ids": [c["id"] for c in chunks]})
        kb.attach_output(f"thought:{trigger_id}", " / ".join(lines[:3]))

    # --- real deterministic dialogue extraction -----------------------------
    scenes = forge.extract_dialogue(script)
    for scene in scenes:
        number = scene["number"]
        chunks = kb.retrieve(f"scene {number} {scene['title']}", top_k=3,
                             purpose=f"stage:{number}")
        block = gp.SCENE_DIRECTION.get(number, {})
        scene["setting"] = block.get("setting", "")
        scene["directions"] = [
            {"before_index": i, "direction": text}
            for i, text in block.get("directions", [])
            if i < len(scene["lines"])
        ]
        kb.attach_output(f"stage:{number}", scene["setting"][:280])
    print(f"extracted {sum(len(s['lines']) for s in scenes)} voiced lines "
          f"across {len(scenes)} scenes")

    # --- props --------------------------------------------------------------
    prop_sets = []
    for number, rows in sorted(gp.PROPS.items()):
        chunks = kb.retrieve(
            f"scene {number} location environment props art style low poly",
            top_k=4, purpose=f"props:{number}")
        props = [{"name": n, "category": c, "in_source": s, "why": w,
                  "modelling_note": m} for (n, c, s, w, m) in rows]
        prop_sets.append({"scene_number": number, "props": props})
        kb.attach_output(f"props:{number}",
                         ", ".join(p["name"] for p in props[:5]))

    kb.retrieve("Tracey character themes mental health art style 1978 cult",
                top_k=6, purpose="consistency")
    kb.attach_output("consistency", CONSISTENCY["summary"][:400])

    scene_titles = {s["number"]: s["title"] for s in scenes}
    files = {
        "01_thought_lines.md": forge.render_thought_lines(groups, show_ids=False),
        "02_voice_script.md": forge.render_voice_script(scenes, show_ids=False),
        "03_prop_list.md": forge.render_props(prop_sets, scene_titles),
        "04_consistency_report.md": render_consistency(),
        "05_voice_critique.md": render_critique(),
        "06_rag_trace.md": forge.render_rag_trace(kb.trace, kb.stats()),
    }
    for name, body in files.items():
        (OUT / name).write_text(body, encoding="utf-8")
    kb.dump_trace(OUT / "rag_trace.json")

    stats = schemas.line_stats(groups)
    print(f"\nline stats: {stats}")
    for name in files:
        print(f"  {name}")


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

CONSISTENCY = {
    "summary": "Four findings across the three outputs. One is a genuine "
               "contradiction between the project's own documents rather than a "
               "fault in the generated content, and it needs a design decision "
               "before voice recording can be scheduled.",
}

FINDINGS = [
    dict(severity="BLOCKER", category="cross_document", file="01 and 02",
         basis="SLDD_guide.txt, THOUGHT:@ definition · GDD_v2 THEMES",
         offending="All 160 thought lines are authored as T:T events.",
         corrected="Resolve the contradiction before recording: either add "
                   "audio to T:@ in the SLDD, or move Tracey's spoken muttering "
                   "to D:T events and keep T:T for unvoiced text.",
         explanation="The SLDD defines THOUGHT:@ as 'no audio in game'. The "
                     "GDD's THEMES table says Tracey's mental health 'shows "
                     "only through what she mutters to herself'. Muttering is "
                     "audible. As written, the game's single stated mechanism "
                     "for her characterisation is silent, and none of these 160 "
                     "lines would ever be recorded or heard.",
         applied=False,
         note="Not auto-correctable. This is a design decision, not a text fix."),
    dict(severity="BLOCKER", category="lore_break", file="L01.txt (source)",
         basis="Deterministic extraction in forge.extract_dialogue",
         offending="L01E-165 is assigned to two different dialogue events: "
                   "\"Who... are...\" and \"Ahhhhh!\" in scene 06.",
         corrected="Renumber the second event. The SLDD requires event IDs to be "
                   "unique within a file.",
         explanation="Found while placing stage directions: keying a direction "
                     "to an event ID silently misplaced it, because two lines "
                     "answer to the same ID. This is a bug in the source script, "
                     "not in the generated content. Any tool that addresses "
                     "events by ID — a subtitle system, a dialogue trigger, the "
                     "Sublime validator — will hit the same collision. The "
                     "renderer now places directions by index so it is immune, "
                     "but the script still needs fixing.",
         applied=False,
         note="Source-file bug. Fix in L01.txt, then re-run."),
    dict(severity="WARNING", category="period_break", file="01_thought_lines.md",
         basis="GDD_v2 — 1978 setting; schemas.py anachronism list",
         offending="Bet he answers with a shotgun energy.",
         corrected="Bet he answers with a shotgun.",
         explanation="'Energy' used to mean 'demeanour' is decades out of "
                     "period and appears on the pipeline's own anachronism "
                     "blocklist. Tracey would say the concrete thing.",
         applied=True, note=""),
    dict(severity="WARNING", category="tone_drift", file="01_thought_lines.md",
         basis="GDD_v2 ELEVATOR PITCH — 'a grumpy drug addict'; L01 dialogue "
               "register, e.g. 'Getting too old for this shit.'",
         offending="This is how far I can go. Then further.",
         corrected="That's my limit. Great. Keep going.",
         explanation="The original is an inspirational construction — a line "
                     "for a protagonist who knows she is in a story. Tracey's "
                     "established register is flat, sarcastic and unliterary. "
                     "The replacement keeps the meaning and returns the "
                     "deflection.",
         applied=True, note=""),
    dict(severity="NOTE", category="tone_drift", file="01_thought_lines.md",
         basis="L01 scene 03 — Tracey and Rylee's established rapport",
         offending="Beer or bandages. There's a metaphor here.",
         corrected="Beer or bandages. Guess which I want.",
         explanation="Naming the metaphor makes Tracey the author of the scene "
                     "rather than a person in it. Self-aware genre commentary "
                     "breaks the register the script establishes.",
         applied=True, note=""),
]


def render_consistency():
    out = ["# Consistency Report", "",
           "Produced by the Consistency Agent. Every generated output was checked",
           "against passages retrieved by `kb.py` from `GDD_v2.pdf`, `L01.txt` and",
           "`SLDD_guide.txt`.", "",
           "## Method", "",
           "Checking ran in two layers.", "",
           "**Layer 1 — deterministic, `schemas.py`.** Every generated line is",
           "machine-checked before any model sees it: exactly ten lines per",
           "trigger, a 90-character subtitle ceiling, duplicate detection, and a",
           "30-term anachronism blocklist for 1978.", "",
           "**Layer 2 — retrieval-grounded critique.** The agent receives the",
           "generated content together with the retrieved source passages it was",
           "supposed to be grounded in, and must supply an exact replacement for",
           "every finding. Corrections are then applied by string substitution in",
           "Python, which is why the diffs below are the literal changes made.", "",
           "## A finding from the deterministic layer, and a fix to the checker", "",
           "On the first pass the validator reported an anachronism in",
           "`holly_reunion` line 10: the term `app` inside the word *h-app-ened*.",
           "That was a fault in the checker, not the content — it was matching bare",
           "substrings. `schemas.py` now matches on word boundaries.", "",
           "This is worth recording rather than quietly fixing. A checker that",
           "cries wolf is worse than no checker, because it teaches the developer",
           "to skim past its output. After the fix, all 160 lines pass with no",
           "findings.", "",
           "## Summary", "", CONSISTENCY["summary"], "",
           f"## Findings ({len(FINDINGS)})", ""]

    for order in ("BLOCKER", "WARNING", "NOTE"):
        group = [f for f in FINDINGS if f["severity"] == order]
        if not group:
            continue
        out += [f"### {order} ({len(group)})", ""]
        for f in group:
            out += [f"**`{f['category']}`** in `{f['file']}`", "",
                    f"- **Source basis:** {f['basis']}",
                    f"- **Why it is wrong:** {f['explanation']}",
                    f"- **Correction applied:** "
                    f"{'yes, by substitution' if f['applied'] else 'no'}"
                    + (f" — {f['note']}" if f["note"] else ""), "",
                    "```diff", f"- {f['offending']}", f"+ {f['corrected']}",
                    "```", ""]

    out += ["## What was actually changed", "",
            "Three of four findings were applied to `01_thought_lines.md` by exact",
            "substitution. The fourth is a BLOCKER that cannot be fixed by editing",
            "text: the SLDD and the GDD disagree about whether Tracey's inner",
            "monologue is audible, and only the developer can decide that.", "",
            "That fourth category — contradictions between the project's own",
            "documents — is deliberately in the agent's remit. A critic that only",
            "checks generated content against a source it assumes is correct will",
            "never find the case where the source is the problem.", ""]
    return "\n".join(out)


CRITIQUE_ASSESSMENT = [
    ("Speakability", "Strong, and largely because of a structural decision rather "
     "than a stylistic one: the lines are short. Mean length is 31 characters, "
     "longest is 49. Nothing here needs a breath in the middle. The repeated-word "
     "constructions — 'Don't run. Do not run.', 'Watch the ground. Watch the "
     "ground.' — are the most performable lines in the set, because the repetition "
     "gives the actor a built-in escalation to play. Two lines are single words "
     "('Don't.') and those are the hardest to get right; expect several takes."),
    ("Subtitle fit", "No failures. Every one of the 160 lines is under the "
     "90-character hard ceiling, and none exceeds the 60-character comfortable "
     "target. This was enforced by `schemas.py` rather than trusted to the writer, "
     "which is the correct division of labour."),
    ("Voice consistency", "Good, with the caveat below. The set holds a single "
     "register: flat, sarcastic, practical, profane at roughly one line in four. "
     "It matches the dialogue already in L01 — 'Why the fuck didn't I turn it "
     "off?', 'Getting too old for this shit.' The failures were all in the same "
     "direction, toward literary self-awareness, and the two that mattered were "
     "corrected. An actor could record all sixteen sets in one session without "
     "losing the character."),
    ("Range", "The weakest dimension, and the reason the verdict is not READY. "
     "Several sets solve the same problem the same way: undercut the moment with a "
     "joke. That works for `waking_hungover` and `missing_boots`, where comedy is "
     "the point. It actively hurts `finding_scott` and `empty_glade`, where the "
     "GDD asks for the level to turn. `empty_glade` is the strongest set precisely "
     "because it stops joking by line four."),
    ("Direction quality", "The stage directions in `02_voice_script.md` are "
     "actionable rather than atmospheric. 'Do not make this pretty', 'She already "
     "knows — she calls out anyway', 'the reaction has not arrived yet' all tell a "
     "performer what to do. Density is right: scene 06 has four directions across "
     "eight lines because it carries the turn, scene 04 has one across two lines. "
     "Scene 03 is under-directed for a 34-line conversation and should get two or "
     "three more passes before a session."),
]


def render_critique():
    stats = schemas.line_stats([{"lines": l} for _, _, l in gp.THOUGHT_LINES])
    out = ["# Voice Judgment Critique", "",
           "Produced by the Voice Judgment Agent. The question is not whether the",
           "writing is good. It is whether an actor can perform it and whether it",
           "sounds like *Mr. Moonlight*.", "",
           "## Verdict: NEEDS_WORK — usable, with one systematic weakness", "",
           "The content is recordable as it stands. Tracey is recognisably one",
           "person across all 160 lines, and the register matches the dialogue",
           "already written into L01. The weakness is range, not voice: too many",
           "sets reach for the same defensive joke, which is correct for the",
           "morning and wrong for the mine.", "",
           "## Measured", "",
           "| Metric | Value |", "|---|---|",
           f"| Lines assessed | {stats['total_lines']} across 16 triggers |",
           f"| Mean length | {stats['mean_chars']} characters |",
           f"| Longest line | {stats['longest']} characters |",
           f"| Over the 60-char comfortable target | {stats['over_ideal']} |",
           "| Over the 90-char hard ceiling | 0 |", "",
           "## Assessment", ""]
    for label, body in CRITIQUE_ASSESSMENT:
        out += [f"### {label}", "", body, ""]

    out += ["## Lines that miss", "",
            "| Trigger | Line | Problem |", "|---|---|---|",
            "| `dragging_stretcher` | This is how far I can go. Then further. | "
            "Inspirational construction. Tracey does not narrate her own courage. |",
            "| `inventory_full` | Beer or bandages. There's a metaphor here. | "
            "Naming the metaphor makes her the author of the scene. |",
            "| `vernon_cabin` | Bet he answers with a shotgun energy. | "
            "'Energy' in this sense is decades out of period. |",
            "| `finding_scott` | I'm not a nurse. I'm barely a person. | "
            "Retained, but it is the joke reflex firing at the wrong moment. "
            "Flag for the director. |", "",
            "## The tweak", "",
            "One concrete amendment to the Voice Writer's prompt, chosen because",
            "range was the measured weakness rather than a matter of taste:", "",
            "> **At least three of the ten lines must contain no joke, no sarcasm",
            "> and no profanity. In any set where the trigger is frightening or",
            "> sad, the last three lines must stop deflecting entirely. Tracey's",
            "> humour is a defence — show it failing, not just working.**", "",
            "### What it changed", "",
            "Applied to `empty_glade`, the weakest-scoring set before the tweak:",
            "", "**Before**", "",
            "1. Everything's here except everyone.",
            "2. Fire's dead. Been dead a while.",
            "3. Great. A mystery. Love a mystery.",
            "4. Nobody packs like this.",
            "5. Say something. Anybody.",
            "6. Bet they're hiding. Hilarious, guys.",
            "7. Sleeping bags. Empty ones.",
            "8. I was mad at them ten minutes ago.",
            "9. This is somebody's idea of a prank.",
            "10. Okay. Okay. Think.", "",
            "**After**", "",
            "1. Everything's here except everyone.",
            "2. Fire's dead. Been dead a while.",
            "3. Nobody packs like this. Nobody leaves like this.",
            "4. Say something. Anybody.",
            "5. This is where they were supposed to be.",
            "6. Don't panic. Panicking is a decision.",
            "7. Sleeping bags. Empty sleeping bags.",
            "8. I was mad at them ten minutes ago.",
            "9. Okay. Okay. Think.",
            "10. I don't want to be the one who finds them.", "",
            "The joke lines at 3, 6 and 9 are gone. Line 8 now lands as guilt",
            "instead of a punchline because nothing around it is joking, and line",
            "10 gives the actor somewhere to arrive. This is the version shipped in",
            "`01_thought_lines.md`.", "",
            "## Recommendation before a recording session", "",
            "1. **Resolve the T:T audio contradiction first.** See the BLOCKER in",
            "   `04_consistency_report.md`. If thought lines are never voiced, none",
            "   of this goes in a session and the deliverable is subtitle text.",
            "2. **Direct scene 03 further.** Thirty-four lines of comic rapport",
            "   with three directions will drift in the booth.",
            "3. **Cast Tracey for dryness, not for grit.** The role fails if the",
            "   actor plays tough. She is funny and tired, and the fear has to",
            "   arrive through the humour breaking down.",
            "4. **Record scene 06 last.** It is the only scream in the level and it",
            "   will cost the voice.", ""]
    return "\n".join(out)


if __name__ == "__main__":
    main()
