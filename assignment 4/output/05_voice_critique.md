# Voice Judgment Critique

Produced by the Voice Judgment Agent. The question is not whether the
writing is good. It is whether an actor can perform it and whether it
sounds like *Mr. Moonlight*.

## Verdict: NEEDS_WORK — usable, with one systematic weakness

The content is recordable as it stands. Tracey is recognisably one
person across all 160 lines, and the register matches the dialogue
already written into L01. The weakness is range, not voice: too many
sets reach for the same defensive joke, which is correct for the
morning and wrong for the mine.

## Measured

| Metric | Value |
|---|---|
| Lines assessed | 160 across 16 triggers |
| Mean length | 31.2 characters |
| Longest line | 49 characters |
| Over the 60-char comfortable target | 0 |
| Over the 90-char hard ceiling | 0 |

## Assessment

### Speakability

Strong, and largely because of a structural decision rather than a stylistic one: the lines are short. Mean length is 31 characters, longest is 49. Nothing here needs a breath in the middle. The repeated-word constructions — 'Don't run. Do not run.', 'Watch the ground. Watch the ground.' — are the most performable lines in the set, because the repetition gives the actor a built-in escalation to play. Two lines are single words ('Don't.') and those are the hardest to get right; expect several takes.

### Subtitle fit

No failures. Every one of the 160 lines is under the 90-character hard ceiling, and none exceeds the 60-character comfortable target. This was enforced by `schemas.py` rather than trusted to the writer, which is the correct division of labour.

### Voice consistency

Good, with the caveat below. The set holds a single register: flat, sarcastic, practical, profane at roughly one line in four. It matches the dialogue already in L01 — 'Why the fuck didn't I turn it off?', 'Getting too old for this shit.' The failures were all in the same direction, toward literary self-awareness, and the two that mattered were corrected. An actor could record all sixteen sets in one session without losing the character.

### Range

The weakest dimension, and the reason the verdict is not READY. Several sets solve the same problem the same way: undercut the moment with a joke. That works for `waking_hungover` and `missing_boots`, where comedy is the point. It actively hurts `finding_scott` and `empty_glade`, where the GDD asks for the level to turn. `empty_glade` is the strongest set precisely because it stops joking by line four.

### Direction quality

The stage directions in `02_voice_script.md` are actionable rather than atmospheric. 'Do not make this pretty', 'She already knows — she calls out anyway', 'the reaction has not arrived yet' all tell a performer what to do. Density is right: scene 06 has four directions across eight lines because it carries the turn, scene 04 has one across two lines. Scene 03 is under-directed for a 34-line conversation and should get two or three more passes before a session.

## Lines that miss

| Trigger | Line | Problem |
|---|---|---|
| `dragging_stretcher` | This is how far I can go. Then further. | Inspirational construction. Tracey does not narrate her own courage. |
| `inventory_full` | Beer or bandages. There's a metaphor here. | Naming the metaphor makes her the author of the scene. |
| `vernon_cabin` | Bet he answers with a shotgun energy. | 'Energy' in this sense is decades out of period. |
| `finding_scott` | I'm not a nurse. I'm barely a person. | Retained, but it is the joke reflex firing at the wrong moment. Flag for the director. |

## The tweak

One concrete amendment to the Voice Writer's prompt, chosen because
range was the measured weakness rather than a matter of taste:

> **At least three of the ten lines must contain no joke, no sarcasm
> and no profanity. In any set where the trigger is frightening or
> sad, the last three lines must stop deflecting entirely. Tracey's
> humour is a defence — show it failing, not just working.**

### What it changed

Applied to `empty_glade`, the weakest-scoring set before the tweak:

**Before**

1. Everything's here except everyone.
2. Fire's dead. Been dead a while.
3. Great. A mystery. Love a mystery.
4. Nobody packs like this.
5. Say something. Anybody.
6. Bet they're hiding. Hilarious, guys.
7. Sleeping bags. Empty ones.
8. I was mad at them ten minutes ago.
9. This is somebody's idea of a prank.
10. Okay. Okay. Think.

**After**

1. Everything's here except everyone.
2. Fire's dead. Been dead a while.
3. Nobody packs like this. Nobody leaves like this.
4. Say something. Anybody.
5. This is where they were supposed to be.
6. Don't panic. Panicking is a decision.
7. Sleeping bags. Empty sleeping bags.
8. I was mad at them ten minutes ago.
9. Okay. Okay. Think.
10. I don't want to be the one who finds them.

The joke lines at 3, 6 and 9 are gone. Line 8 now lands as guilt
instead of a punchline because nothing around it is joking, and line
10 gives the actor somewhere to arrive. This is the version shipped in
`01_thought_lines.md`.

## Recommendation before a recording session

1. **Resolve the T:T audio contradiction first.** See the BLOCKER in
   `04_consistency_report.md`. If thought lines are never voiced, none
   of this goes in a session and the deliverable is subtitle text.
2. **Direct scene 03 further.** Thirty-four lines of comic rapport
   with three directions will drift in the booth.
3. **Cast Tracey for dryness, not for grit.** The role fails if the
   actor plays tough. She is funny and tired, and the fear has to
   arrive through the humour breaking down.
4. **Record scene 06 last.** It is the only scream in the level and it
   will cost the voice.
