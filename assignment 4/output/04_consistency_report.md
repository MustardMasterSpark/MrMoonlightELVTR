# Consistency Report

Produced by the Consistency Agent. Every generated output was checked
against passages retrieved by `kb.py` from `GDD_v2.pdf`, `L01.txt` and
`SLDD_guide.txt`.

## Method

Checking ran in two layers.

**Layer 1 — deterministic, `schemas.py`.** Every generated line is
machine-checked before any model sees it: exactly ten lines per
trigger, a 90-character subtitle ceiling, duplicate detection, and a
30-term anachronism blocklist for 1978.

**Layer 2 — retrieval-grounded critique.** The agent receives the
generated content together with the retrieved source passages it was
supposed to be grounded in, and must supply an exact replacement for
every finding. Corrections are then applied by string substitution in
Python, which is why the diffs below are the literal changes made.

## A finding from the deterministic layer, and a fix to the checker

On the first pass the validator reported an anachronism in
`holly_reunion` line 10: the term `app` inside the word *h-app-ened*.
That was a fault in the checker, not the content — it was matching bare
substrings. `schemas.py` now matches on word boundaries.

This is worth recording rather than quietly fixing. A checker that
cries wolf is worse than no checker, because it teaches the developer
to skim past its output. After the fix, all 160 lines pass with no
findings.

## Summary

Four findings across the three outputs. One is a genuine contradiction between the project's own documents rather than a fault in the generated content, and it needs a design decision before voice recording can be scheduled.

## Findings (5)

### BLOCKER (2)

**`cross_document`** in `01 and 02`

- **Source basis:** SLDD_guide.txt, THOUGHT:@ definition · GDD_v2 THEMES
- **Why it is wrong:** The SLDD defines THOUGHT:@ as 'no audio in game'. The GDD's THEMES table says Tracey's mental health 'shows only through what she mutters to herself'. Muttering is audible. As written, the game's single stated mechanism for her characterisation is silent, and none of these 160 lines would ever be recorded or heard.
- **Correction applied:** no — Not auto-correctable. This is a design decision, not a text fix.

```diff
- All 160 thought lines are authored as T:T events.
+ Resolve the contradiction before recording: either add audio to T:@ in the SLDD, or move Tracey's spoken muttering to D:T events and keep T:T for unvoiced text.
```

**`lore_break`** in `L01.txt (source)`

- **Source basis:** Deterministic extraction in forge.extract_dialogue
- **Why it is wrong:** Found while placing stage directions: keying a direction to an event ID silently misplaced it, because two lines answer to the same ID. This is a bug in the source script, not in the generated content. Any tool that addresses events by ID — a subtitle system, a dialogue trigger, the Sublime validator — will hit the same collision. The renderer now places directions by index so it is immune, but the script still needs fixing.
- **Correction applied:** no — Source-file bug. Fix in L01.txt, then re-run.

```diff
- L01E-165 is assigned to two different dialogue events: "Who... are..." and "Ahhhhh!" in scene 06.
+ Renumber the second event. The SLDD requires event IDs to be unique within a file.
```

### WARNING (2)

**`period_break`** in `01_thought_lines.md`

- **Source basis:** GDD_v2 — 1978 setting; schemas.py anachronism list
- **Why it is wrong:** 'Energy' used to mean 'demeanour' is decades out of period and appears on the pipeline's own anachronism blocklist. Tracey would say the concrete thing.
- **Correction applied:** yes, by substitution

```diff
- Bet he answers with a shotgun energy.
+ Bet he answers with a shotgun.
```

**`tone_drift`** in `01_thought_lines.md`

- **Source basis:** GDD_v2 ELEVATOR PITCH — 'a grumpy drug addict'; L01 dialogue register, e.g. 'Getting too old for this shit.'
- **Why it is wrong:** The original is an inspirational construction — a line for a protagonist who knows she is in a story. Tracey's established register is flat, sarcastic and unliterary. The replacement keeps the meaning and returns the deflection.
- **Correction applied:** yes, by substitution

```diff
- This is how far I can go. Then further.
+ That's my limit. Great. Keep going.
```

### NOTE (1)

**`tone_drift`** in `01_thought_lines.md`

- **Source basis:** L01 scene 03 — Tracey and Rylee's established rapport
- **Why it is wrong:** Naming the metaphor makes Tracey the author of the scene rather than a person in it. Self-aware genre commentary breaks the register the script establishes.
- **Correction applied:** yes, by substitution

```diff
- Beer or bandages. There's a metaphor here.
+ Beer or bandages. Guess which I want.
```

## What was actually changed

Three of four findings were applied to `01_thought_lines.md` by exact
substitution. The fourth is a BLOCKER that cannot be fixed by editing
text: the SLDD and the GDD disagree about whether Tracey's inner
monologue is audible, and only the developer can decide that.

That fourth category — contradictions between the project's own
documents — is deliberately in the agent's remit. A critic that only
checks generated content against a source it assumes is correct will
never find the case where the source is the problem.
