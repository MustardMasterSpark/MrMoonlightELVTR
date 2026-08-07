# RAG Retrieval Trace

Every retrieval the pipeline performed, with the query, the chunks BM25
returned, and the output produced from them. This is the evidence that
generation is grounded in the game's own documents.

## Index

- Chunks: **73** (62 from the GDD, 11 from L01)
- Average chunk size: 1713 characters
- Retrieval: BM25 sparse, k1=1.5, b=0.75, stopword-filtered
- Deterministic: the same query always returns the same chunks

---

## 1. `thought:waking_hungover`

**Query**

```
Tracey hangover campsite alarm vomit stamina morning
```

**Retrieved chunks**

<details><summary><code>L01#S01</code> · Scene 01 — WAKING AT THE CAMPSITE · score 13.574 · matched: alarm, campsite, hangover, stamina, tracey, vomit</summary>

```
============================================================================= -->


L01E-001 || VFX:PV || Name: Black screen || Description: The camera view is completely dark. || Execution: after the player starts a new game from the main menu, the black screen is already active || Duration: N/A || Intensity: N/A || Layer: N/A
L01E-000 || VFX:UI || Name: Black screen || Description: after the player starts a new game from the main menu, the black screen is already active. All UI elements (except the subtitle text) are black. || Execution: N/A
L01E-000 || CB:T || Name: Camera blocked from star
```

</details>

<details><summary><code>GDD#007</code> · ELEVATOR PITCH — THE FICTION · score 9.752 · matched: hangover, morning, tracey</summary>

```
A group of friends, a weeklong camping trip, a remote Alaskan island. Trying to have one good last time together
before the important adulthood changes arrive. Something goes wrong.
You are Tracey, a grumpy drug addict trying to save her kidnapped friends from a cult that will sacrifice them at the
end of the week. There is something about the island: each night its terrain shifts into something deadly, and every
night it forces you to find shelter before three in the morning.
Day 1 is where none of that is known yet. Tracey wakes up with a hangover and no boots, and spends a morning
being ann
```

</details>

<details><summary><code>GDD#036</code> · CUT FROM T HE ENEMY ROST ER · score 5.746 · matched: alarm, stamina, tracey</summary>

```
Stone totems, the Cultist Priest and punji traps appear in v0.1 but not in the Day 1 script. All three are removed from
the slice. The priest in particular carries ranged weapons, poison and later spellcasting — a whole combat category the
slice does not need.







 09 IT EMS


Seventeen objects. Every one of them is picked up, handed over or used somewhere in the Day 1 script.

                Item                       Role in Day 1

                Canteen                    The first thing Tracey wants. Drinking clears her vision and starts stamina recovery.
                CONSUMABLE, R
```

</details>

<details><summary><code>GDD#008</code> · ELEVATOR PITCH — THE MECHANICS OF THE SLICE · score 5.196 · matched: campsite, stamina, tracey</summary>

```
• A fixed route, hand built. Day 1 runs on one authored path through eight locations. The procedural island
   generator that reshuffles the map every day is a full-game feature and is not in the slice — see section 12.
 • Navigation you have to stop for. A map and a compass, taken from William's tent. Deploying them locks Tracey
   in place and exposes her, so reading the map is a decision, not a free action.
 • Combat that costs something. A pickaxe with heavy slow swings, and two firearms handed over late. Every blow
   drains stamina. Some encounters are meant to be walked around, not won.
```

</details>

**Output produced from these chunks**

> Whose idea was the second bottle. / Mouth tastes like a wet ashtray. / The sun is too loud today.

---

## 2. `thought:missing_boots`

**Query**

```
boots missing barefoot socks forest floor sprint noise
```

**Retrieved chunks**

<details><summary><code>GDD#027</code> · MOCKUP SCREENS · score 7.131 · matched: noise, sprint</summary>

```
Carry and drop          Backpack holds a limited number of items; the player                  At the blue cooler
                         chooses what to lose.

 Navigate                Deploy map and compass. Locks Tracey in place while                   From William's tent
                         open.

 Swing                   Heavy, slow pickaxe blows that drain stamina.                         Pulled from the telescope frame

 Shoot                   M1911, then the Arisaka. Loud, scarce, and a last resort.             Vernon's cabin, then the mine infirmary

 Drag                    Pul
```

</details>

<details><summary><code>L01#S03</code> · Scene 03 — RADIO CONVERSATION WITH RYLEE · score 6.723 · matched: barefoot, boots, floor, forest, socks</summary>

```
============================================================================= -->

L01E-064 || D:T || Line: Uhhh... hello? || Tone: N/A || Color: white || Display Method: Typewriter || Lipsync: F || Aftertime: 1.0 || Text effect: N/A
L01E-065 || SA || Name: Beat: no response || Description: No response. || Trigger: N/A || Target: N/A || Condition: N/A || Blocking: T || Branch: N/A
L01E-066 || D:T || Line: Hellooo? || Tone: N/A || Color: white || Display Method: Typewriter || Lipsync: F || Aftertime: 1.0 || Text effect: N/A
L01E-067 || SA || Name: Beat: no response || Description: No response.
```

</details>

<details><summary><code>GDD#033</code> · MOCKUP SCREENS · score 6.21 · matched: barefoot, forest</summary>

```
Enemy                                                                      Behaviour to build

                  Wolf                                                                       Roam · circle the player · bite · break off
                  E-W                                                                        when struck · flee when hurt · afraid of fire
                  Introduced at distance on the forest road, where it crosses the path
                  and ignores Tracey entirely — she is barefoot and cannot chase it. It
                  returns as a pack at the Glade, afte
```

</details>

<details><summary><code>GDD#026</code> · MOCKUP SCREENS · score 5.922 · matched: boots, sprint</summary>

```
These are pre-production mockups from v0.1 and are not current builds. Two of them show equipment that is not in
the slice, noted below.




 Zealots close in on the road to the cabin. The buff item shown predates the
                                 current scope.
                                                                                        Caught in the bear trap — the branch point of Scene 07.




                              A Furman charges. The bone axe shown is not in the slice; in Day 1 Tracey carries the pickaxe.









  07 GAME ME CHANICS


Everything below exists in th
```

</details>

**Output produced from these chunks**

> Barefoot. On an island. Cute. / Somebody thought this was funny. / I hope whoever took them steps on something.

---

## 3. `thought:rylee_radio`

**Query**

```
Rylee radio walkie talkie conversation Glade jokes
```

**Retrieved chunks**

<details><summary><code>GDD#036</code> · CUT FROM T HE ENEMY ROST ER · score 10.705 · matched: glade, rylee, talkie, walkie</summary>

```
Stone totems, the Cultist Priest and punji traps appear in v0.1 but not in the Day 1 script. All three are removed from
the slice. The priest in particular carries ranged weapons, poison and later spellcasting — a whole combat category the
slice does not need.







 09 IT EMS


Seventeen objects. Every one of them is picked up, handed over or used somewhere in the Day 1 script.

                Item                       Role in Day 1

                Canteen                    The first thing Tracey wants. Drinking clears her vision and starts stamina recovery.
                CONSUMABLE, R
```

</details>

<details><summary><code>L01#S02</code> · Scene 02 — THE MISSING BOOTS · score 7.215 · matched: conversation, radio, rylee</summary>

```
============================================================================= -->

L01E-043 || SFX || Name: Radio call louder || Description: The radio call becomes louder and easier to locate. || Audio: N/A || Source: N/A || Volume: N/A || Loop: F || Fade: N/A
L01E-044 || D:T || Line: What in the world? || Tone: N/A || Color: white || Display Method: Typewriter || Lipsync: F || Aftertime: 1.0 || Text effect: N/A
L01E-045 || O:3:S || Title: Who's calling? || Description: N/A || Optional: F || Marker: N/A
L01E-046 || HA || Name: store canteen in belt carrier, notice bare feet || Description: Tr
```

</details>

<details><summary><code>L01#S03</code> · Scene 03 — RADIO CONVERSATION WITH RYLEE · score 6.496 · matched: conversation, glade, jokes, radio, rylee</summary>

```
============================================================================= -->

L01E-064 || D:T || Line: Uhhh... hello? || Tone: N/A || Color: white || Display Method: Typewriter || Lipsync: F || Aftertime: 1.0 || Text effect: N/A
L01E-065 || SA || Name: Beat: no response || Description: No response. || Trigger: N/A || Target: N/A || Condition: N/A || Blocking: T || Branch: N/A
L01E-066 || D:T || Line: Hellooo? || Tone: N/A || Color: white || Display Method: Typewriter || Lipsync: F || Aftertime: 1.0 || Text effect: N/A
L01E-067 || SA || Name: Beat: no response || Description: No response.
```

</details>

<details><summary><code>GDD#015</code> · NAMED BUT NOT PRESENT IN DAY 1 · score 5.793 · matched: conversation, radio</summary>

```
Robert, William and Shannon are talked about in Rylee's radio conversation and appear in the Polaroid photograph.
  They need no model, no rig and no voice for the slice.
  Amaruq and Mr. Moonlight are named in the full-game fiction and do not appear anywhere in the Day 1 script. They
  are out of scope and are not described here.









  04 GAME FLOW


The slice is one day, not seven. The loop below is what a player repeats scene by scene inside that day.




                  Figure 1 — the Day 1 loop. Compared to v0.1: the manual save system is gone, and the seven-day wrapper is gone.
```

</details>

**Output produced from these chunks**

> Of course she's awake and cheerful. / Say something useful. Once. / I can hear her grinning through the static.

---

## 4. `thought:inventory_full`

**Query**

```
backpack carry limit inventory cooler drop item fifth
```

**Retrieved chunks**

<details><summary><code>L01#S02</code> · Scene 02 — THE MISSING BOOTS · score 14.055 · matched: backpack, carry, cooler, fifth, inventory, item, limit</summary>

```
============================================================================= -->

L01E-043 || SFX || Name: Radio call louder || Description: The radio call becomes louder and easier to locate. || Audio: N/A || Source: N/A || Volume: N/A || Loop: F || Fade: N/A
L01E-044 || D:T || Line: What in the world? || Tone: N/A || Color: white || Display Method: Typewriter || Lipsync: F || Aftertime: 1.0 || Text effect: N/A
L01E-045 || O:3:S || Title: Who's calling? || Description: N/A || Optional: F || Marker: N/A
L01E-046 || HA || Name: store canteen in belt carrier, notice bare feet || Description: Tr
```

</details>

<details><summary><code>GDD#027</code> · MOCKUP SCREENS · score 11.515 · matched: backpack, carry, cooler, drop</summary>

```
Carry and drop          Backpack holds a limited number of items; the player                  At the blue cooler
                         chooses what to lose.

 Navigate                Deploy map and compass. Locks Tracey in place while                   From William's tent
                         open.

 Swing                   Heavy, slow pickaxe blows that drain stamina.                         Pulled from the telescope frame

 Shoot                   M1911, then the Arisaka. Loud, scarce, and a last resort.             Vernon's cabin, then the mine infirmary

 Drag                    Pul
```

</details>

<details><summary><code>GDD#008</code> · ELEVATOR PITCH — THE MECHANICS OF THE SLICE · score 11.292 · matched: backpack, carry, drop, fifth</summary>

```
• A fixed route, hand built. Day 1 runs on one authored path through eight locations. The procedural island
   generator that reshuffles the map every day is a full-game feature and is not in the slice — see section 12.
 • Navigation you have to stop for. A map and a compass, taken from William's tent. Deploying them locks Tracey
   in place and exposes her, so reading the map is a decision, not a free action.
 • Combat that costs something. A pickaxe with heavy slow swings, and two firearms handed over late. Every blow
   drains stamina. Some encounters are meant to be walked around, not won.
```

</details>

<details><summary><code>GDD#028</code> · MOCKUP SCREENS · score 8.511 · matched: fifth, inventory, item</summary>

```
during a scripted beat.                             that always get released.







 System               What the player sees                           What it has to hold                    Built from

 Interaction          A prompt icon appears when something can       Range, line of sight, required item.   Owned FPS asset
                      be used.

 Inventory            The fifth pickup is refused and Tracey         Capacity, contents, discard.           Systems Smith
                      complains.

 Stamina              A bar that appears for the first time during   Current, max,
```

</details>

**Output produced from these chunks**

> Pack's full. Something's staying. / Can't carry the world, Trace. / Choose. It's not hard. It's just annoying.

---

## 5. `thought:wolves_first`

**Query**

```
wolf roam circle bite forest road barefoot
```

**Retrieved chunks**

<details><summary><code>GDD#033</code> · MOCKUP SCREENS · score 26.756 · matched: barefoot, bite, circle, forest, road, roam, wolf</summary>

```
Enemy                                                                      Behaviour to build

                  Wolf                                                                       Roam · circle the player · bite · break off
                  E-W                                                                        when struck · flee when hurt · afraid of fire
                  Introduced at distance on the forest road, where it crosses the path
                  and ignores Tracey entirely — she is barefoot and cannot chase it. It
                  returns as a pack at the Glade, afte
```

</details>

<details><summary><code>L01#S05</code> · Scene 05 — THE FOREST ROAD TO THE GLADE · score 9.063 · matched: barefoot, forest, road, wolf</summary>

```
============================================================================= -->

L01E-126 || PA || Name: Travel east || Description: The player travels east through the forest. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A

L01E-127 || SA || Name: Wolf crosses path || Description: A single wolf crosses the player's view at a distance, following a predefined path. It ignores Tracey. Because she is barefoot, she cannot catch it. || Trigger: N/A || Target: N/A || Condition: N/A || Blocking: F || Branch: N/A
L01E-128 || SFX || Name: Distant wolf calls || Descripti
```

</details>

<details><summary><code>GDD#019</code> · LOCATIONS · score 8.799 · matched: forest, road, wolf</summary>

```
Location                                                                                   Where it appears in the
                                                                                                                     script

                          Camping site                                                                               Scenes 01–04
                          The RV, two tents, William's locked tent, the bonfire, the table with the
                          canteen, and two coolers. Everything the player learns in the first ten
                          minute
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 5.249 · matched: forest, wolf</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> I fucking hate dogs. / Big dog. Big, unfriendly dog. / Don't run. Do not run.

---

## 6. `thought:empty_glade`

**Query**

```
Glade abandoned belongings scattered bonfire sleeping bags
```

**Retrieved chunks**

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 19.166 · matched: bags, belongings, bonfire, glade, scattered, sleeping</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>L01#S06</code> · Scene 06 — THE EMPTY GLADE · score 12.808 · matched: abandoned, bags, belongings, bonfire, glade, scattered, sleeping</summary>

```
============================================================================= -->

L01E-145 || PA || Name: Enter the Glade || Description: The player enters the Glade. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A
L01E-146 || SA || Name: Stage abandoned Glade || Description: Stage the Glade as abandoned: belongings are scattered across the ground, the bonfire is extinguished, and the sleeping bags are in disarray. A pickaxe is embedded in the telescope frame. Tracey's boots lie near the bonfire. Near a table are a beer, a soda, and a Polaroid photograph of the g
```

</details>

<details><summary><code>GDD#019</code> · LOCATIONS · score 10.29 · matched: abandoned, bonfire, glade</summary>

```
Location                                                                                   Where it appears in the
                                                                                                                     script

                          Camping site                                                                               Scenes 01–04
                          The RV, two tents, William's locked tent, the bonfire, the table with the
                          canteen, and two coolers. Everything the player learns in the first ten
                          minute
```

</details>

<details><summary><code>GDD#037</code> · CUT FROM T HE ENEMY ROST ER · score 6.978 · matched: abandoned, glade</summary>

```
TOOL                       Tracey in place.



                Polaroid photograph        Lying near the table in the abandoned Glade. A picture of the whole group. Tracey
                KEY ITEM                   stows it in the compass pouch and says nothing.

                Inuit pickaxe              Buried in the telescope frame. Heavy, slow, medium reach, and the only weapon for
                MELEE WEAPON               the middle of the level.




                Matches                    In the red cooler with the radio. Emergency light source.
                LIGHT
```

</details>

**Output produced from these chunks**

> Everything's here except everyone. / Fire's dead. Been dead a while. / Nobody packs like this. Nobody leaves like this.

---

## 7. `thought:the_polaroid`

**Query**

```
Polaroid photograph group friends camp table
```

**Retrieved chunks**

<details><summary><code>GDD#037</code> · CUT FROM T HE ENEMY ROST ER · score 14.39 · matched: group, photograph, polaroid, table</summary>

```
TOOL                       Tracey in place.



                Polaroid photograph        Lying near the table in the abandoned Glade. A picture of the whole group. Tracey
                KEY ITEM                   stows it in the compass pouch and says nothing.

                Inuit pickaxe              Buried in the telescope frame. Heavy, slow, medium reach, and the only weapon for
                MELEE WEAPON               the middle of the level.




                Matches                    In the red cooler with the radio. Emergency light source.
                LIGHT
```

</details>

<details><summary><code>GDD#019</code> · LOCATIONS · score 12.067 · matched: camp, polaroid, table</summary>

```
Location                                                                                   Where it appears in the
                                                                                                                     script

                          Camping site                                                                               Scenes 01–04
                          The RV, two tents, William's locked tent, the bonfire, the table with the
                          canteen, and two coolers. Everything the player learns in the first ten
                          minute
```

</details>

<details><summary><code>L01#S06</code> · Scene 06 — THE EMPTY GLADE · score 11.593 · matched: friends, group, photograph, polaroid, table</summary>

```
============================================================================= -->

L01E-145 || PA || Name: Enter the Glade || Description: The player enters the Glade. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A
L01E-146 || SA || Name: Stage abandoned Glade || Description: Stage the Glade as abandoned: belongings are scattered across the ground, the bonfire is extinguished, and the sleeping bags are in disarray. A pickaxe is embedded in the telescope frame. Tracey's boots lie near the bonfire. Near a table are a beer, a soda, and a Polaroid photograph of the g
```

</details>

<details><summary><code>GDD#015</code> · NAMED BUT NOT PRESENT IN DAY 1 · score 7.882 · matched: photograph, polaroid</summary>

```
Robert, William and Shannon are talked about in Rylee's radio conversation and appear in the Polaroid photograph.
  They need no model, no rig and no voice for the slice.
  Amaruq and Mr. Moonlight are named in the full-game fiction and do not appear anywhere in the Day 1 script. They
  are out of scope and are not described here.









  04 GAME FLOW


The slice is one day, not seven. The loop below is what a player repeats scene by scene inside that day.




                  Figure 1 — the Day 1 loop. Compared to v0.1: the manual save system is gone, and the seven-day wrapper is gone.
```

</details>

**Output produced from these chunks**

> Look at us. Idiots. / That was two days ago. / I'm not even looking at the camera.

---

## 8. `thought:pickaxe_telescope`

**Query**

```
pickaxe telescope frame melee heavy swing stamina
```

**Retrieved chunks**

<details><summary><code>GDD#027</code> · MOCKUP SCREENS · score 18.298 · matched: frame, heavy, melee, pickaxe, stamina, swing, telescope</summary>

```
Carry and drop          Backpack holds a limited number of items; the player                  At the blue cooler
                         chooses what to lose.

 Navigate                Deploy map and compass. Locks Tracey in place while                   From William's tent
                         open.

 Swing                   Heavy, slow pickaxe blows that drain stamina.                         Pulled from the telescope frame

 Shoot                   M1911, then the Arisaka. Loud, scarce, and a last resort.             Vernon's cabin, then the mine infirmary

 Drag                    Pul
```

</details>

<details><summary><code>GDD#037</code> · CUT FROM T HE ENEMY ROST ER · score 16.961 · matched: frame, heavy, melee, pickaxe, stamina, telescope</summary>

```
TOOL                       Tracey in place.



                Polaroid photograph        Lying near the table in the abandoned Glade. A picture of the whole group. Tracey
                KEY ITEM                   stows it in the compass pouch and says nothing.

                Inuit pickaxe              Buried in the telescope frame. Heavy, slow, medium reach, and the only weapon for
                MELEE WEAPON               the middle of the level.




                Matches                    In the red cooler with the radio. Emergency light source.
                LIGHT
```

</details>

<details><summary><code>GDD#028</code> · MOCKUP SCREENS · score 11.083 · matched: melee, pickaxe, stamina, swing</summary>

```
during a scripted beat.                             that always get released.







 System               What the player sees                           What it has to hold                    Built from

 Interaction          A prompt icon appears when something can       Range, line of sight, required item.   Owned FPS asset
                      be used.

 Inventory            The fifth pickup is refused and Tracey         Capacity, contents, discard.           Systems Smith
                      complains.

 Stamina              A bar that appears for the first time during   Current, max,
```

</details>

<details><summary><code>L01#S06</code> · Scene 06 — THE EMPTY GLADE · score 10.364 · matched: frame, melee, pickaxe, telescope</summary>

```
============================================================================= -->

L01E-145 || PA || Name: Enter the Glade || Description: The player enters the Glade. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A
L01E-146 || SA || Name: Stage abandoned Glade || Description: Stage the Glade as abandoned: belongings are scattered across the ground, the bonfire is extinguished, and the sleeping bags are in disarray. A pickaxe is embedded in the telescope frame. Tracey's boots lie near the bonfire. Near a table are a beer, a soda, and a Polaroid photograph of the g
```

</details>

**Output produced from these chunks**

> Somebody drove this in hard. / Heavy. Good. Heavy is good. / This is a tool. It's a tool.

---

## 9. `thought:bear_trap`

**Query**

```
bear trap branch road ambush health hazard
```

**Retrieved chunks**

<details><summary><code>GDD#033</code> · MOCKUP SCREENS · score 17.944 · matched: ambush, bear, branch, health, road, trap</summary>

```
Enemy                                                                      Behaviour to build

                  Wolf                                                                       Roam · circle the player · bite · break off
                  E-W                                                                        when struck · flee when hurt · afraid of fire
                  Introduced at distance on the forest road, where it crosses the path
                  and ignores Tracey entirely — she is barefoot and cannot chase it. It
                  returns as a pack at the Glade, afte
```

</details>

<details><summary><code>L01#S07</code> · Scene 07 — THE ROAD TO VERNON'S CABIN · score 15.955 · matched: ambush, bear, branch, health, road, trap</summary>

```
============================================================================= -->

L01E-174 || PA || Name: Follow route to cabin || Description: The player follows the route toward the cabin. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A
L01E-175 || SA || Name: Place bear trap || Description: Place a bear trap on the path. The first trap cannot kill Tracey, but it removes a large amount of health and stamina. || Trigger: N/A || Target: N/A || Condition: N/A || Blocking: F || Branch: N/A
L01E-176 || OL || Name: Branch A: zealot ambush || Description: BRANCH A: If
```

</details>

<details><summary><code>GDD#034</code> · MOCKUP SCREENS · score 15.097 · matched: bear, branch, health, road, trap</summary>

```
E-S                                                                        whistle to summon · never lose interest once
                  Branch B. If the player is caught in the trap, the zealots do not come.    alerted
                  Two spotters patrol at distance with flashlights instead, and stay non-
                  hostile unless approached. Fighting them while injured is meant to kill
                  you.




                  Furman                                                                     Charge · heavy bites · raises fear on approach
                  E-F
```

</details>

<details><summary><code>GDD#026</code> · MOCKUP SCREENS · score 9.165 · matched: bear, branch, road, trap</summary>

```
These are pre-production mockups from v0.1 and are not current builds. Two of them show equipment that is not in
the slice, noted below.




 Zealots close in on the road to the cabin. The buff item shown predates the
                                 current scope.
                                                                                        Caught in the bear trap — the branch point of Scene 07.




                              A Furman charges. The bone axe shown is not in the slice; in Day 1 Tracey carries the pickaxe.









  07 GAME ME CHANICS


Everything below exists in th
```

</details>

**Output produced from these chunks**

> Teeth in the dirt. / Somebody put that there. On purpose. / That's not for animals.

---

## 10. `thought:cultists_first`

**Query**

```
cultist zealot spotter lamp whistle robes altar
```

**Retrieved chunks**

<details><summary><code>GDD#033</code> · MOCKUP SCREENS · score 13.699 · matched: cultist, lamp, spotter, zealot</summary>

```
Enemy                                                                      Behaviour to build

                  Wolf                                                                       Roam · circle the player · bite · break off
                  E-W                                                                        when struck · flee when hurt · afraid of fire
                  Introduced at distance on the forest road, where it crosses the path
                  and ignores Tracey entirely — she is barefoot and cannot chase it. It
                  returns as a pack at the Glade, afte
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 8.546 · matched: cultist, spotter, zealot</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 8.478 · matched: spotter, whistle, zealot</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

<details><summary><code>L01#S00</code> · Scene 00 — Front matter · score 7.396 · matched: cultist, spotter, zealot</summary>

```
L01 — MR. MOONLIGHT, DAY 1
     Converted to SLDD format from the previous EVT-### working draft.

     Conversion notes:
       - Event IDs map one to one: EVT-001 becomes L01E-001. No event was
         reordered, merged or dropped.
       - Old NOTE events became comments, which is what the SLDD reserves
         comments for. Their IDs are retired and not reused: L01E-196,
         L01E-206, L01E-224.
       - Old BEAT events are mapped to SA with Blocking: T. The SLDD has no
         BEAT type; consider adding one.
       - Old OUTLINE events use the type OL, which is NOT yet in the SLDD
```

</details>

**Output produced from these chunks**

> People. Those are people. / Lamps. They're looking for something. / Down. Get down.

---

## 11. `thought:vernon_cabin`

**Query**

```
Vernon cabin crosses hermit orthodox religion door
```

**Retrieved chunks**

<details><summary><code>GDD#025</code> · THEMES · score 19.414 · matched: cabin, crosses, door, orthodox, religion, vernon</summary>

```
Theme                               How Day 1 handles it

 Substance abuse                     The player is not told Tracey is an addict. Day 1 opens on a hangover played for comedy, and ends
                                     with Vernon handing her morphine and Holly handing her marijuana. Neither is explained. The system
                                     underneath them arrives properly on Day 2.

 Religion                            Orthodox Christian imagery from the first Russian settlers of Alaska: crosses nailed to a cabin door, a
                                     Virgin Mary
```

</details>

<details><summary><code>GDD#020</code> · LOCATIONS · score 11.632 · matched: cabin, crosses, door, vernon</summary>

```
and a light in the distance.

                    Vernon's cabin                                                                    Scenes 07–08
                    More of a box than a cabin, warm inside, door covered in crosses. Holly
                    and Vernon are here. It is the only safe room in the level.




                    Flak tower                                                                        Scene 08
                    Visible in the distance. Cannot be entered. If the player walks toward it the
                    game communicates that it is full of cultists and
```

</details>

<details><summary><code>L01#S07</code> · Scene 07 — THE ROAD TO VERNON'S CABIN · score 7.838 · matched: cabin, crosses, door</summary>

```
============================================================================= -->

L01E-174 || PA || Name: Follow route to cabin || Description: The player follows the route toward the cabin. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A
L01E-175 || SA || Name: Place bear trap || Description: Place a bear trap on the path. The first trap cannot kill Tracey, but it removes a large amount of health and stamina. || Trigger: N/A || Target: N/A || Condition: N/A || Blocking: F || Branch: N/A
L01E-176 || OL || Name: Branch A: zealot ambush || Description: BRANCH A: If
```

</details>

<details><summary><code>GDD#039</code> · CONSUMABLE · score 6.018 · matched: cabin, vernon</summary>

```
Mining lamp                    Obtained at the mine entrance. Without it the tunnel is not navigable.
                LIGHT




                M1911 pistol                   Given by Vernon at the cabin. Reliable, high stopping power, and very loud in a forest
                FIREARM                        full of people listening.



                Morphine                       Given by Vernon alongside the pistol. Fast healing and damage reduction, at the cost
                SUBSTANCE                      of nausea and rising fear.

                Marijuana                      Given by
```

</details>

**Output produced from these chunks**

> Crosses. Every inch of the door. / Somebody's very worried about something. / That's not decoration. That's a fence.

---

## 12. `thought:holly_reunion`

**Query**

```
Holly cabin alive marijuana friend reunion
```

**Retrieved chunks**

<details><summary><code>GDD#039</code> · CONSUMABLE · score 8.777 · matched: cabin, holly, marijuana</summary>

```
Mining lamp                    Obtained at the mine entrance. Without it the tunnel is not navigable.
                LIGHT




                M1911 pistol                   Given by Vernon at the cabin. Reliable, high stopping power, and very loud in a forest
                FIREARM                        full of people listening.



                Morphine                       Given by Vernon alongside the pistol. Fast healing and damage reduction, at the cost
                SUBSTANCE                      of nausea and rising fear.

                Marijuana                      Given by
```

</details>

<details><summary><code>GDD#025</code> · THEMES · score 6.994 · matched: cabin, holly, marijuana</summary>

```
Theme                               How Day 1 handles it

 Substance abuse                     The player is not told Tracey is an addict. Day 1 opens on a hangover played for comedy, and ends
                                     with Vernon handing her morphine and Holly handing her marijuana. Neither is explained. The system
                                     underneath them arrives properly on Day 2.

 Religion                            Orthodox Christian imagery from the first Russian settlers of Alaska: crosses nailed to a cabin door, a
                                     Virgin Mary
```

</details>

<details><summary><code>GDD#010</code> · COMPARABLE GAMES · score 6.835 · matched: friend, holly</summary>

```
the uncle of Holly, your childhood friend.
You are Tracey. Twenty-something, a history major who dropped out, in possession of some nasty habits and a
permanently foul mouth. You did not want to come. Your friends insisted far too much. Fine. One more time.


Camping as a kid was fun, but now everything feels heavy and stupid. Maybe I should go easy this
time…………………………………
Great, I feel great! Give me a minute… bleehh, false puke alarm everybody… hey! Hello? Not funny guys, where are my
boots?… where… where is everyone?









 03 CAST


Five characters exist in Day 1. Three more are named in
```

</details>

<details><summary><code>GDD#013</code> · AT T HE CABIN · score 6.826 · matched: cabin, marijuana</summary>

```
Miss Perfect, and exhausting about it. She is at Vernon's cabin when Tracey arrives, and she is the one who
                       hands over the marijuana.




                       Scott
```

</details>

**Output produced from these chunks**

> Holly. Holly's alive. / Don't cry. Do not cry. / She looks worse than me. That's saying something.

---

## 13. `thought:the_mine`

**Query**

```
mine mineshaft dark lamp linear route infirmary
```

**Retrieved chunks**

<details><summary><code>L01#S09</code> · Scene 09 — THE MINE · score 18.533 · matched: infirmary, lamp, linear, mine, route</summary>

```
============================================================================= -->

L01E-197 || OL || Name: Reach mine entrance || Description: The player reaches the mine entrance. || Intended Type: N/A
L01E-198 || OL || Name: Obtain mining lamp || Description: The player obtains or activates a mining lamp. || Intended Type: N/A
L01E-199 || OL || Name: Linear mine route || Description: The mine route is mostly linear. || Intended Type: N/A
L01E-200 || OL || Name: Cultists in the mine || Description: The player encounters and fights cultists inside the mine. || Intended Type: N/A
L01E-201 || OL
```

</details>

<details><summary><code>GDD#020</code> · LOCATIONS · score 14.893 · matched: infirmary, lamp, linear, mineshaft</summary>

```
and a light in the distance.

                    Vernon's cabin                                                                    Scenes 07–08
                    More of a box than a cabin, warm inside, door covered in crosses. Holly
                    and Vernon are here. It is the only safe room in the level.




                    Flak tower                                                                        Scene 08
                    Visible in the distance. Cannot be entered. If the player walks toward it the
                    game communicates that it is full of cultists and
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 10.023 · matched: infirmary, linear, mine, route</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#040</code> · SUBSTANCE · score 7.495 · matched: infirmary, mine</summary>

```
Arisaka rifle                  In the mine infirmary next to Scott. Long range, high damage, and awkward to use
                FIREARM                        while dragging a stretcher.




                Stretcher                      In the infirmary. Scott goes on it, and the last third of the level is spent pulling it.
```

</details>

**Output produced from these chunks**

> Dark. Properly dark. / Lamp's not much. Lamp's what we have. / It smells like wet iron.

---

## 14. `thought:finding_scott`

**Query**

```
Scott unconscious infirmary rescue first aid
```

**Retrieved chunks**

<details><summary><code>L01#S09</code> · Scene 09 — THE MINE · score 15.357 · matched: infirmary, rescue, scott, unconscious</summary>

```
============================================================================= -->

L01E-197 || OL || Name: Reach mine entrance || Description: The player reaches the mine entrance. || Intended Type: N/A
L01E-198 || OL || Name: Obtain mining lamp || Description: The player obtains or activates a mining lamp. || Intended Type: N/A
L01E-199 || OL || Name: Linear mine route || Description: The mine route is mostly linear. || Intended Type: N/A
L01E-200 || OL || Name: Cultists in the mine || Description: The player encounters and fights cultists inside the mine. || Intended Type: N/A
L01E-201 || OL
```

</details>

<details><summary><code>GDD#040</code> · SUBSTANCE · score 8.412 · matched: infirmary, scott</summary>

```
Arisaka rifle                  In the mine infirmary next to Scott. Long range, high damage, and awkward to use
                FIREARM                        while dragging a stretcher.




                Stretcher                      In the infirmary. Scott goes on it, and the last third of the level is spent pulling it.
```

</details>

<details><summary><code>GDD#027</code> · MOCKUP SCREENS · score 7.383 · matched: first, infirmary, scott</summary>

```
Carry and drop          Backpack holds a limited number of items; the player                  At the blue cooler
                         chooses what to lose.

 Navigate                Deploy map and compass. Locks Tracey in place while                   From William's tent
                         open.

 Swing                   Heavy, slow pickaxe blows that drain stamina.                         Pulled from the telescope frame

 Shoot                   M1911, then the Arisaka. Loud, scarce, and a last resort.             Vernon's cabin, then the mine infirmary

 Drag                    Pul
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 6.248 · matched: first, scott, unconscious</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> Scott. Scott, wake up. / He's breathing. He's breathing. / That's a lot of blood for one person.

---

## 15. `thought:dragging_stretcher`

**Query**

```
stretcher drag Scott movement restricted combat
```

**Retrieved chunks**

<details><summary><code>GDD#027</code> · MOCKUP SCREENS · score 18.127 · matched: combat, drag, movement, restricted, scott, stretcher</summary>

```
Carry and drop          Backpack holds a limited number of items; the player                  At the blue cooler
                         chooses what to lose.

 Navigate                Deploy map and compass. Locks Tracey in place while                   From William's tent
                         open.

 Swing                   Heavy, slow pickaxe blows that drain stamina.                         Pulled from the telescope frame

 Shoot                   M1911, then the Arisaka. Loud, scarce, and a last resort.             Vernon's cabin, then the mine infirmary

 Drag                    Pul
```

</details>

<details><summary><code>L01#S09</code> · Scene 09 — THE MINE · score 10.088 · matched: combat, scott, stretcher</summary>

```
============================================================================= -->

L01E-197 || OL || Name: Reach mine entrance || Description: The player reaches the mine entrance. || Intended Type: N/A
L01E-198 || OL || Name: Obtain mining lamp || Description: The player obtains or activates a mining lamp. || Intended Type: N/A
L01E-199 || OL || Name: Linear mine route || Description: The mine route is mostly linear. || Intended Type: N/A
L01E-200 || OL || Name: Cultists in the mine || Description: The player encounters and fights cultists inside the mine. || Intended Type: N/A
L01E-201 || OL
```

</details>

<details><summary><code>GDD#014</code> · FOUND IN T HE MINE · score 8.336 · matched: drag, stretcher</summary>

```
Dodged the draft and still wants to join the air force. He transmits once on the radio, and after that he is an
                       unconscious body on a stretcher that the player has to drag out.




                       Vernon
                       AT T HE CABIN, T HEN ON T HE RADIO
                       Holly's uncle, the island's only resident. Tubercular, armed, and the only person who behaves like he knows
                       what is happening. He gives Tracey the M1911 and the morphine, points her at the mine, and later creates
                       the distraction that lets
```

</details>

<details><summary><code>GDD#040</code> · SUBSTANCE · score 7.806 · matched: scott, stretcher</summary>

```
Arisaka rifle                  In the mine infirmary next to Scott. Long range, high damage, and awkward to use
                FIREARM                        while dragging a stretcher.




                Stretcher                      In the infirmary. Scott goes on it, and the last third of the level is spent pulling it.
```

</details>

**Output produced from these chunks**

> Heavier than he looks. / Slow. Everything's slow now. / Can't fight and pull. Can't do both.

---

## 16. `thought:nightfall`

**Query**

```
night darkness three in the morning shelter North Star church
```

**Retrieved chunks**

<details><summary><code>L01#S10</code> · Scene 10 — THE NIGHT ESCAPE · score 19.972 · matched: church, darkness, night, north, shelter, star</summary>

```
============================================================================= -->

L01E-207 || OL || Name: Full darkness || Description: It is now fully dark outside. || Intended Type: N/A
L01E-208 || SFX || Name: Whistles, wolves, flare || Description: Distant whistles, wolves, and a flare signal can be heard or seen. || Audio: N/A || Source: N/A || Volume: N/A || Loop: F || Fade: N/A
L01E-209 || OL || Name: Vernon radio contact || Description: Vernon contacts Tracey by radio. || Intended Type: N/A
L01E-210 || OL || Name: Follow the North Star || Description: Vernon tells her to head north an
```

</details>

<details><summary><code>GDD#007</code> · ELEVATOR PITCH — THE FICTION · score 12.61 · matched: morning, night, shelter, three</summary>

```
A group of friends, a weeklong camping trip, a remote Alaskan island. Trying to have one good last time together
before the important adulthood changes arrive. Something goes wrong.
You are Tracey, a grumpy drug addict trying to save her kidnapped friends from a cult that will sacrifice them at the
end of the week. There is something about the island: each night its terrain shifts into something deadly, and every
night it forces you to find shelter before three in the morning.
Day 1 is where none of that is known yet. Tracey wakes up with a hangover and no boots, and spends a morning
being ann
```

</details>

<details><summary><code>GDD#060</code> · CRITICAL FEATURES · score 7.864 · matched: church, night, three</summary>

```
Mon 17 – Sun 23           Steps 5 and 6a. Full route walkable. Inventory, stamina,       Enemy models and animation sets. Lighting sets
 Aug                       fear, navigation, melee.                                       baked.








Dates                  Agent track — code                                             My track — art, audio, writing

Mon 24 – Sun 30        Step 6b. Four enemies live. Bear-trap branches. Escort.        Audio pass. UI pass. Church, Hill of Crosses, flak tower
Aug                    Night escape.                                                  silhouette.
```

</details>

<details><summary><code>GDD#022</code> · KEYWORDS · score 7.829 · matched: darkness, night</summary>

```
Substance abuse · punk-acid style · foul language · crude combat · claustrophobic darkness · item management · exploration
· regret · monsters · traps · hide and seek · objective centric · night sky
```

</details>

**Output produced from these chunks**

> Sun's going. Sun's going fast. / That's not how the sky should look. / Three in the morning. Somebody said three.

---

## 17. `stage:1`

**Query**

```
scene 1 WAKING AT THE CAMPSITE
```

**Retrieved chunks**

<details><summary><code>GDD#058</code> · CRITICAL FEATURES · score 4.069 · matched: campsite, scene</summary>

```
3        Map what I already own                                                                       package-map.md exists and I have read it
          A read-only pass over the FPS package and the terrain package. Find the extension
          points, the prefabs that matter and the files that must not be touched. Decide wrap or
          modify for each one, in writing.

 4        Build the script runner                                                                      Scene 01 plays start to finish, driven
          The parser and the event system that turns the text file into a playing
```

</details>

<details><summary><code>L01#S01</code> · Scene 01 — WAKING AT THE CAMPSITE · score 4.046 · matched: campsite, scene, waking</summary>

```
============================================================================= -->


L01E-001 || VFX:PV || Name: Black screen || Description: The camera view is completely dark. || Execution: after the player starts a new game from the main menu, the black screen is already active || Duration: N/A || Intensity: N/A || Layer: N/A
L01E-000 || VFX:UI || Name: Black screen || Description: after the player starts a new game from the main menu, the black screen is already active. All UI elements (except the subtitle text) are black. || Execution: N/A
L01E-000 || CB:T || Name: Camera blocked from star
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 3.559 · matched: campsite, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

**Output produced from these chunks**

> Dawn at the campsite. Tracey is face down in a tent she does not remember getting into, hungover badly enough that it is funny to everyone except her. A cheap Seiko alarm is going off somewhere near her head and will not stop. She is alone. Nothing supernatural has happened yet a

---

## 18. `stage:2`

**Query**

```
scene 2 THE MISSING BOOTS
```

**Retrieved chunks**

<details><summary><code>L01#S02</code> · Scene 02 — THE MISSING BOOTS · score 5.615 · matched: boots, missing, scene</summary>

```
============================================================================= -->

L01E-043 || SFX || Name: Radio call louder || Description: The radio call becomes louder and easier to locate. || Audio: N/A || Source: N/A || Volume: N/A || Loop: F || Fade: N/A
L01E-044 || D:T || Line: What in the world? || Tone: N/A || Color: white || Display Method: Typewriter || Lipsync: F || Aftertime: 1.0 || Text effect: N/A
L01E-045 || O:3:S || Title: Who's calling? || Description: N/A || Optional: F || Marker: N/A
L01E-046 || HA || Name: store canteen in belt carrier, notice bare feet || Description: Tr
```

</details>

<details><summary><code>GDD#019</code> · LOCATIONS · score 4.197 · matched: boots, scene</summary>

```
Location                                                                                   Where it appears in the
                                                                                                                     script

                          Camping site                                                                               Scenes 01–04
                          The RV, two tents, William's locked tent, the bonfire, the table with the
                          canteen, and two coolers. Everything the player learns in the first ten
                          minute
```

</details>

<details><summary><code>L01#S06</code> · Scene 06 — THE EMPTY GLADE · score 3.252 · matched: boots, scene</summary>

```
============================================================================= -->

L01E-145 || PA || Name: Enter the Glade || Description: The player enters the Glade. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A
L01E-146 || SA || Name: Stage abandoned Glade || Description: Stage the Glade as abandoned: belongings are scattered across the ground, the bonfire is extinguished, and the sleeping bags are in disarray. A pickaxe is embedded in the telescope frame. Tracey's boots lie near the bonfire. Near a table are a beer, a soda, and a Polaroid photograph of the g
```

</details>

**Output produced from these chunks**

> Outside, minutes later. Her boots are gone from where she left them. She is standing in wet socks on cold ground working out that this is now her whole day. Play the indignity, not the danger. She thinks a friend did this as a joke.

---

## 19. `stage:3`

**Query**

```
scene 3 RADIO CONVERSATION WITH RYLEE
```

**Retrieved chunks**

<details><summary><code>L01#S02</code> · Scene 02 — THE MISSING BOOTS · score 7.81 · matched: conversation, radio, rylee, scene</summary>

```
============================================================================= -->

L01E-043 || SFX || Name: Radio call louder || Description: The radio call becomes louder and easier to locate. || Audio: N/A || Source: N/A || Volume: N/A || Loop: F || Fade: N/A
L01E-044 || D:T || Line: What in the world? || Tone: N/A || Color: white || Display Method: Typewriter || Lipsync: F || Aftertime: 1.0 || Text effect: N/A
L01E-045 || O:3:S || Title: Who's calling? || Description: N/A || Optional: F || Marker: N/A
L01E-046 || HA || Name: store canteen in belt carrier, notice bare feet || Description: Tr
```

</details>

<details><summary><code>GDD#015</code> · NAMED BUT NOT PRESENT IN DAY 1 · score 7.659 · matched: conversation, radio, scene</summary>

```
Robert, William and Shannon are talked about in Rylee's radio conversation and appear in the Polaroid photograph.
  They need no model, no rig and no voice for the slice.
  Amaruq and Mr. Moonlight are named in the full-game fiction and do not appear anywhere in the Day 1 script. They
  are out of scope and are not described here.









  04 GAME FLOW


The slice is one day, not seven. The loop below is what a player repeats scene by scene inside that day.




                  Figure 1 — the Day 1 loop. Compared to v0.1: the manual save system is gone, and the seven-day wrapper is gone.
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 5.518 · matched: radio, rylee, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

**Output produced from these chunks**

> The walkie talkie. Rylee is somewhere else on the island and in a much better mood. This is the longest conversation in the level and the only one where Tracey is comfortable. The two of them have known each other a long time and insult each other fluently; the affection is under

---

## 20. `stage:4`

**Query**

```
scene 4 WILL'S TENT AND THE COMPASS
```

**Retrieved chunks**

<details><summary><code>L01#S04</code> · Scene 04 — WILL'S TENT AND THE COMPASS · score 13.131 · matched: compass, scene, tent, will's</summary>

```
============================================================================= -->

L01E-108 || PA || Name: Try locked tent || Description: The player attempts to open William's tent without the key. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A
L01E-109 || T:T || Line: The key was under the rug, according to the cow. || Color: white || Display Method: Typewriter || Aftertime: 1.0 || Text effect: N/A


L01E-110 || PA || Name: Interact with RV rug || Description: The player interacts with the rug beneath the RV. || Trigger: N/A || Target: N/A || Requires: N/A || B
```

</details>

<details><summary><code>GDD#036</code> · CUT FROM T HE ENEMY ROST ER · score 7.06 · matched: compass, tent</summary>

```
Stone totems, the Cultist Priest and punji traps appear in v0.1 but not in the Day 1 script. All three are removed from
the slice. The priest in particular carries ranged weapons, poison and later spellcasting — a whole combat category the
slice does not need.







 09 IT EMS


Seventeen objects. Every one of them is picked up, handed over or used somewhere in the Day 1 script.

                Item                       Role in Day 1

                Canteen                    The first thing Tracey wants. Drinking clears her vision and starts stamina recovery.
                CONSUMABLE, R
```

</details>

<details><summary><code>GDD#019</code> · LOCATIONS · score 5.193 · matched: scene, tent</summary>

```
Location                                                                                   Where it appears in the
                                                                                                                     script

                          Camping site                                                                               Scenes 01–04
                          The RV, two tents, William's locked tent, the bonfire, the table with the
                          canteen, and two coolers. Everything the player learns in the first ten
                          minute
```

</details>

**Output produced from these chunks**

> Inside William's tent, uninvited. She is taking his map and compass because she needs them, and being brisk about it so she does not have to think about why his tent is empty. Businesslike. Two short lines, both to herself.

---

## 21. `stage:5`

**Query**

```
scene 5 THE FOREST ROAD TO THE GLADE
```

**Retrieved chunks**

<details><summary><code>GDD#019</code> · LOCATIONS · score 10.047 · matched: forest, glade, road, scene</summary>

```
Location                                                                                   Where it appears in the
                                                                                                                     script

                          Camping site                                                                               Scenes 01–04
                          The RV, two tents, William's locked tent, the bonfire, the table with the
                          canteen, and two coolers. Everything the player learns in the first ten
                          minute
```

</details>

<details><summary><code>GDD#033</code> · MOCKUP SCREENS · score 8.974 · matched: forest, glade, road</summary>

```
Enemy                                                                      Behaviour to build

                  Wolf                                                                       Roam · circle the player · bite · break off
                  E-W                                                                        when struck · flee when hurt · afraid of fire
                  Introduced at distance on the forest road, where it crosses the path
                  and ignores Tracey entirely — she is barefoot and cannot chase it. It
                  returns as a pack at the Glade, afte
```

</details>

<details><summary><code>L01#S05</code> · Scene 05 — THE FOREST ROAD TO THE GLADE · score 7.132 · matched: forest, glade, road, scene</summary>

```
============================================================================= -->

L01E-126 || PA || Name: Travel east || Description: The player travels east through the forest. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A

L01E-127 || SA || Name: Wolf crosses path || Description: A single wolf crosses the player's view at a distance, following a predefined path. It ignores Tracey. Because she is barefoot, she cannot catch it. || Trigger: N/A || Target: N/A || Condition: N/A || Blocking: F || Branch: N/A
L01E-128 || SFX || Name: Distant wolf calls || Descripti
```

</details>

**Output produced from these chunks**

> The forest road, walking east, barefoot. Something crosses the path ahead of her — a wolf, at distance, which ignores her completely. The fear here is new and she has no vocabulary for it yet. These are three small sounds, not speeches.

---

## 22. `stage:6`

**Query**

```
scene 6 THE EMPTY GLADE
```

**Retrieved chunks**

<details><summary><code>L01#S06</code> · Scene 06 — THE EMPTY GLADE · score 4.544 · matched: empty, glade, scene</summary>

```
============================================================================= -->

L01E-145 || PA || Name: Enter the Glade || Description: The player enters the Glade. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A
L01E-146 || SA || Name: Stage abandoned Glade || Description: Stage the Glade as abandoned: belongings are scattered across the ground, the bonfire is extinguished, and the sleeping bags are in disarray. A pickaxe is embedded in the telescope frame. Tracey's boots lie near the bonfire. Near a table are a beer, a soda, and a Polaroid photograph of the g
```

</details>

<details><summary><code>GDD#019</code> · LOCATIONS · score 4.197 · matched: glade, scene</summary>

```
Location                                                                                   Where it appears in the
                                                                                                                     script

                          Camping site                                                                               Scenes 01–04
                          The RV, two tents, William's locked tent, the bonfire, the table with the
                          canteen, and two coolers. Everything the player learns in the first ten
                          minute
```

</details>

<details><summary><code>L01#S05</code> · Scene 05 — THE FOREST ROAD TO THE GLADE · score 3.492 · matched: glade, scene</summary>

```
============================================================================= -->

L01E-126 || PA || Name: Travel east || Description: The player travels east through the forest. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A

L01E-127 || SA || Name: Wolf crosses path || Description: A single wolf crosses the player's view at a distance, following a predefined path. It ignores Tracey. Because she is barefoot, she cannot catch it. || Trigger: N/A || Target: N/A || Condition: N/A || Blocking: F || Branch: N/A
L01E-128 || SFX || Name: Distant wolf calls || Descripti
```

</details>

**Output produced from these chunks**

> The Glade, where her friends were supposed to be. Their belongings are scattered, the bonfire is long dead, the sleeping bags are empty. This is where the level turns and where the actor's job changes. Tracey's defences are verbal, and here they stop working. She calls out, gets 

---

## 23. `stage:7`

**Query**

```
scene 7 THE ROAD TO VERNON'S CABIN
```

**Retrieved chunks**

<details><summary><code>L01#S07</code> · Scene 07 — THE ROAD TO VERNON'S CABIN · score 7.721 · matched: cabin, road, scene, vernon's</summary>

```
============================================================================= -->

L01E-174 || PA || Name: Follow route to cabin || Description: The player follows the route toward the cabin. || Trigger: N/A || Target: N/A || Requires: N/A || Blocking: F || Branch: N/A
L01E-175 || SA || Name: Place bear trap || Description: Place a bear trap on the path. The first trap cannot kill Tracey, but it removes a large amount of health and stamina. || Trigger: N/A || Target: N/A || Condition: N/A || Blocking: F || Branch: N/A
L01E-176 || OL || Name: Branch A: zealot ambush || Description: BRANCH A: If
```

</details>

<details><summary><code>GDD#020</code> · LOCATIONS · score 7.124 · matched: cabin, scene, vernon's</summary>

```
and a light in the distance.

                    Vernon's cabin                                                                    Scenes 07–08
                    More of a box than a cabin, warm inside, door covered in crosses. Holly
                    and Vernon are here. It is the only safe room in the level.




                    Flak tower                                                                        Scene 08
                    Visible in the distance. Cannot be entered. If the player walks toward it the
                    game communicates that it is full of cultists and
```

</details>

<details><summary><code>GDD#013</code> · AT T HE CABIN · score 6.371 · matched: cabin, vernon's</summary>

```
Miss Perfect, and exhausting about it. She is at Vernon's cabin when Tracey arrives, and she is the one who
                       hands over the marijuana.




                       Scott
```

</details>

**Output produced from these chunks**

> The road to the cabin, after violence. She has killed someone and she is not equipped for that. One line, quiet, entirely unlike the rest of her register.

---

## 24. `stage:8`

**Query**

```
scene 8 VERNON'S CABIN
```

**Retrieved chunks**

<details><summary><code>GDD#020</code> · LOCATIONS · score 7.124 · matched: cabin, scene, vernon's</summary>

```
and a light in the distance.

                    Vernon's cabin                                                                    Scenes 07–08
                    More of a box than a cabin, warm inside, door covered in crosses. Holly
                    and Vernon are here. It is the only safe room in the level.




                    Flak tower                                                                        Scene 08
                    Visible in the distance. Cannot be entered. If the player walks toward it the
                    game communicates that it is full of cultists and
```

</details>

<details><summary><code>GDD#013</code> · AT T HE CABIN · score 6.371 · matched: cabin, vernon's</summary>

```
Miss Perfect, and exhausting about it. She is at Vernon's cabin when Tracey arrives, and she is the one who
                       hands over the marijuana.




                       Scott
```

</details>

<details><summary><code>GDD#018</code> · THE ROUTE · score 5.496 · matched: cabin, vernon's</summary>

```
The player moves east from the campsite to the Glade, then to Vernon's cabin, then into the mine, then north to the
church. There are no optional areas and no backtracking. The only branch in the level is at the bear trap, and it
changes which enemy the player meets, not where they go.
```

</details>

**Output produced from these chunks**

> Vernon's cabin. Crosses nailed over every inch of the door, firelight inside, the first warmth in the level. Holly is alive. Vernon is a sick hermit with tuberculosis who knows more than he says and is running out of time to say it. Scott comes through on the radio. This is the b

---

## 25. `props:1`

**Query**

```
scene 1 location environment props art style low poly
```

**Retrieved chunks**

<details><summary><code>GDD#023</code> · ART STYLE · score 13.818 · matched: art, low, poly, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 9.057 · matched: art, environment, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 7.876 · matched: art, low, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 7.41 · matched: location, props</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> Two-person canvas tent, period, Sleeping bag, unzipped, Seiko wristwatch with alarm, Canteen, aluminium, Blue cooler

---

## 26. `props:2`

**Query**

```
scene 2 location environment props art style low poly
```

**Retrieved chunks**

<details><summary><code>GDD#023</code> · ART STYLE · score 13.818 · matched: art, low, poly, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 9.057 · matched: art, environment, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 7.876 · matched: art, low, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 7.41 · matched: location, props</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> Hiking boots, Tracey's, Wet wool socks, Muddy ground, footprint decals, Tent flap, animated, Clothes line with hanging laundry

---

## 27. `props:3`

**Query**

```
scene 3 location environment props art style low poly
```

**Retrieved chunks**

<details><summary><code>GDD#023</code> · ART STYLE · score 13.818 · matched: art, low, poly, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 9.057 · matched: art, environment, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 7.876 · matched: art, low, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 7.41 · matched: location, props</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> Walkie talkie handset, RV interior rug, Tent key, small brass, Camp table, folding, Soda can, period

---

## 28. `props:4`

**Query**

```
scene 4 location environment props art style low poly
```

**Retrieved chunks**

<details><summary><code>GDD#023</code> · ART STYLE · score 13.818 · matched: art, low, poly, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 9.057 · matched: art, environment, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 7.876 · matched: art, low, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 7.41 · matched: location, props</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> William's tent, exterior and interior, Padlock, broken, Compass, brass, period, Paper map, folded and unfolded, Neck pouch, canvas

---

## 29. `props:5`

**Query**

```
scene 5 location environment props art style low poly
```

**Retrieved chunks**

<details><summary><code>GDD#023</code> · ART STYLE · score 13.818 · matched: art, low, poly, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 9.057 · matched: art, environment, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 7.876 · matched: art, low, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 7.41 · matched: location, props</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> Forest road, dirt path mesh, Wolf, Fog volume and particles, Undergrowth and fern cards, Fallen log, mossy

---

## 30. `props:6`

**Query**

```
scene 6 location environment props art style low poly
```

**Retrieved chunks**

<details><summary><code>GDD#023</code> · ART STYLE · score 13.818 · matched: art, low, poly, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 9.057 · matched: art, environment, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 7.876 · matched: art, low, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 7.41 · matched: location, props</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> Telescope on tripod, Pickaxe, Polaroid photograph of the group, Sleeping bags, empty and disarrayed, Scattered belongings kit

---

## 31. `props:7`

**Query**

```
scene 7 location environment props art style low poly
```

**Retrieved chunks**

<details><summary><code>GDD#023</code> · ART STYLE · score 13.818 · matched: art, low, poly, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 9.057 · matched: art, environment, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 7.876 · matched: art, low, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 7.41 · matched: location, props</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> Bear trap, open and sprung, Cultist Zealot, Cultist Spotter with lamp, Handheld oil lamp, lit, Knife and scythe

---

## 32. `props:8`

**Query**

```
scene 8 location environment props art style low poly
```

**Retrieved chunks**

<details><summary><code>GDD#023</code> · ART STYLE · score 13.818 · matched: art, low, poly, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 9.057 · matched: art, environment, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 7.876 · matched: art, low, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 7.41 · matched: location, props</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> Vernon's cabin interior, Fireplace with live fire, M1911 pistol, Morphine syrettes in a tin, Marijuana, rolled

---

## 33. `props:9`

**Query**

```
scene 9 location environment props art style low poly
```

**Retrieved chunks**

<details><summary><code>GDD#023</code> · ART STYLE · score 13.818 · matched: art, low, poly, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 9.057 · matched: art, environment, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 7.876 · matched: art, low, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 7.41 · matched: location, props</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> Mine entrance and headframe, Mine interior tunnel kit, Mining lamp, handheld, Infirmary room dressing, Stretcher, canvas and wood

---

## 34. `props:10`

**Query**

```
scene 10 location environment props art style low poly
```

**Retrieved chunks**

<details><summary><code>GDD#023</code> · ART STYLE · score 13.818 · matched: art, low, poly, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#051</code> · CRITICAL FEATURES · score 9.057 · matched: art, environment, scene</summary>

```
Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package as
```

</details>

<details><summary><code>GDD#052</code> · CRITICAL FEATURES · score 7.876 · matched: art, low, scene</summary>

```
Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig
```

</details>

<details><summary><code>GDD#053</code> · CRITICAL FEATURES · score 7.41 · matched: location, props</summary>

```
Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender








 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith age
```

</details>

**Output produced from these chunks**

> Hill of Crosses, Virgin Mary statue, Church exterior and entrance, Circle of fire, Night sky with North Star

---

## 35. `consistency`

**Query**

```
Tracey character themes mental health art style 1978 cult
```

**Retrieved chunks**

<details><summary><code>GDD#002</code> · MATURE CONTENT · score 20.747 · matched: 1978, art, health, mental, style, themes, tracey</summary>

```
This is a work of fiction. Contains violence, substance abuse, mental-health themes, religious and blasphemous imagery,
and strong language. Discretion advised.









  INDEX


(Click on the titles, they are hyperlinks to travel across the Document to the chapters and back to the index)



 01      Executive Summary                      One pager, core loop, win and loss conditions, elevator pitch, comparable games, ship
                                                dates.

 02      Story                                  1978, Aanniarvik Island, Tracey, and how Day 1 begins.

 03      Cas
```

</details>

<details><summary><code>GDD#025</code> · THEMES · score 19.358 · matched: 1978, character, health, mental, themes, tracey</summary>

```
Theme                               How Day 1 handles it

 Substance abuse                     The player is not told Tracey is an addict. Day 1 opens on a hangover played for comedy, and ends
                                     with Vernon handing her morphine and Holly handing her marijuana. Neither is explained. The system
                                     underneath them arrives properly on Day 2.

 Religion                            Orthodox Christian imagery from the first Russian settlers of Alaska: crosses nailed to a cabin door, a
                                     Virgin Mary
```

</details>

<details><summary><code>GDD#009</code> · COMPARABLE GAMES · score 6.283 · matched: 1978, cult</summary>

```
Game                           What we take from it

Slenderman: The Eight Pages    Being hunted in a dark forest while looking for scattered things.
(2012)

Misery (2025)                  A daily run against a hard clock, ending at a shelter.

Dusk (2018)                    Crude, violent low-poly shooting against a cult.

The Forest (2018)              Resource pressure and a hostile population in the woods.

Silent Hill 1 (1999)           Plain white subtitle lines, and telling the story through them rather than around them.


DATES

Milestone                      Date

Vertical slice playa
```

</details>

<details><summary><code>GDD#023</code> · ART STYLE · score 6.264 · matched: art, style</summary>

```
Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin
```

</details>

<details><summary><code>GDD#054</code> · CRITICAL FEATURES · score 5.797 · matched: health, style</summary>

```
E. User interface
 Feature or asset                                                               How it gets built

 Subtitle renderer, Silent Hill 1 style, typewriter and immediate               Nani Novel, adapted for first-person use

 Stamina bar with reveal and hide                                               Systems Smith agent

 Health indicator                                                               Systems Smith agent

 Interaction prompt icon                                                        FPS asset UI, restyled

 Backpack screen with discard
```

</details>

<details><summary><code>GDD#007</code> · ELEVATOR PITCH — THE FICTION · score 5.782 · matched: cult, tracey</summary>

```
A group of friends, a weeklong camping trip, a remote Alaskan island. Trying to have one good last time together
before the important adulthood changes arrive. Something goes wrong.
You are Tracey, a grumpy drug addict trying to save her kidnapped friends from a cult that will sacrifice them at the
end of the week. There is something about the island: each night its terrain shifts into something deadly, and every
night it forces you to find shelter before three in the morning.
Day 1 is where none of that is known yet. Tracey wakes up with a hangover and no boots, and spends a morning
being ann
```

</details>

**Output produced from these chunks**

> Four findings across the three outputs. One is a genuine contradiction between the project's own documents rather than a fault in the generated content, and it needs a design decision before voice recording can be scheduled.
