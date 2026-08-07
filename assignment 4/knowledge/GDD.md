                                                              MR. MOONLIGHT (MVP) ·    GAME DESIGN DOCUMENT      ·   V0.2


}




                                   GAME
                                  DESIGN
                                 DOCUMENT

      VERTICAL SLICE · Level 1:Muddy




                             Version 0.2 — 30 / 07 / 2026
                          Mustard · Carlos Ivan Calva Avalos




MATURE CONTENT
This is a work of fiction. Contains violence, substance abuse, mental-health themes, religious and blasphemous imagery,
and strong language. Discretion advised.




                                                                                                                          2
                                                                 MR. MOONLIGHT (MVP) ·            GAME DESIGN DOCUMENT            ·    V0.2




  INDEX


(Click on the titles, they are hyperlinks to travel across the Document to the chapters and back to the index)



 01      Executive Summary                      One pager, core loop, win and loss conditions, elevator pitch, comparable games, ship
                                                dates.

 02      Story                                  1978, Aanniarvik Island, Tracey, and how Day 1 begins.

 03      Cast                                   The five characters that appear in Day 1, and who is only spoken about.

 04      Game Flow                              The loop diagram for the slice, and how failure is handled without a save menu.

 05      The Island in Day 1                    The fixed route, the eight locations it passes through, and what was cut.

 06      Look and Feel                          Keywords, art style, sound design, themes, mockup screens.

 07      Game Mechanics                         Player verbs, every system in the slice, and how the level script drives the engine.

 08      Enemies and Threats                    Wolf, Zealot, Spotter, Furman, bear trap, and their state machines.

 09      Items                                  The seventeen objects the player can hold or use in Day 1.

 10      AI Architecture                        The eight development agents, what each one does, and what the player ends up
                                                seeing.

 11      Token Budget and API                   What the agent crew costs, and the four constraints that shape it.
         Constraints

 12      Feedback: Cut From the Vertical        Everything removed from v0.1, and when it comes back.
         Slice

 13      MVP Critical Route                     The full critical-feature list with a build method for each.

 14      Technical Strategy and Timeline        Seven steps, and a chronogram from 31 July to 31 August 2026.




                                                                                                                                          3
                                                                   MR. MOONLIGHT (MVP) ·        GAME DESIGN DOCUMENT            ·   V0.2




  01 EXECUT IVE SUMMARY


Mr. Moonlight is a slow, gritty, first-person horror game set on an Alaskan island in 1978. You are Tracey —
hungover, barefoot, and alone at a campsite where seven friends should be. This document describes Day 1: the
first of seven days, and the only one being built right now.

 Title                                 Mr. Moonlight

 Genre                                 First-person survival horror shooter with exploration

 This document covers                  The Day 1 vertical slice only

 Engine                                Unity 6.3 LTS

 Slice platform                        PC (Windows x64), released on itch.io

 Later platforms                       Steam and GOG, then consoles — post-slice

 Audience                              Adults, 18+, niche horror

 Target rating                         ESRB Mature 17+

 Session length                        30 to 50 minutes

 Team                                  One developer, assisted by a crew of Claude agents

 Slice ship target                     itch.io, first week of September 2026


THE CORE LOOP, IN ONE SENTENCE

Explore a dark forest on a fixed route, scavenge what you can carry, survive or avoid what finds you, and reach shelter
before the night closes.

WIN AND LOSS CONDITIONS



 WIN                    Day 1 is complete when Tracey pulls Scott out of the mine and reaches the church on the Hill of Crosses.

 LOSS                   Tracey dies. There is no game-over screen to manage: the level restarts at the last scene checkpoint.


ELEVATOR PITCH — THE FICTION

A group of friends, a weeklong camping trip, a remote Alaskan island. Trying to have one good last time together
before the important adulthood changes arrive. Something goes wrong.
You are Tracey, a grumpy drug addict trying to save her kidnapped friends from a cult that will sacrifice them at the
end of the week. There is something about the island: each night its terrain shifts into something deadly, and every
night it forces you to find shelter before three in the morning.
Day 1 is where none of that is known yet. Tracey wakes up with a hangover and no boots, and spends a morning
being annoyed about it. By nightfall she is dragging an unconscious friend through a mine while people in black
whistle to each other in the dark.




                                                                                                                                       4
                                                                  MR. MOONLIGHT (MVP) ·        GAME DESIGN DOCUMENT      ·   V0.2


ELEVATOR PITCH — THE MECHANICS OF THE SLICE

 • A fixed route, hand built. Day 1 runs on one authored path through eight locations. The procedural island
   generator that reshuffles the map every day is a full-game feature and is not in the slice — see section 12.
 • Navigation you have to stop for. A map and a compass, taken from William's tent. Deploying them locks Tracey
   in place and exposes her, so reading the map is a decision, not a free action.
 • Combat that costs something. A pickaxe with heavy slow swings, and two firearms handed over late. Every blow
   drains stamina. Some encounters are meant to be walked around, not won.
 • Fear as a visible state. Fear rises at scripted moments and shows itself through chromatic aberration, camera
   shake and Tracey's breathing. The player reads their own condition off the screen and the headphones, not off a
   number.
 • A backpack that is too small. The coolers at the campsite hold more than Tracey can carry. The fifth pickup is
   refused, and the player has to drop something.
 • Sound as information. A radio call locates a person. A whistle locates a patrol. Sprinting makes noise, which is
   why the boots matter.

COMPARABLE GAMES

Game                           What we take from it

Slenderman: The Eight Pages    Being hunted in a dark forest while looking for scattered things.
(2012)

Misery (2025)                  A daily run against a hard clock, ending at a shelter.

Dusk (2018)                    Crude, violent low-poly shooting against a cult.

The Forest (2018)              Resource pressure and a hostile population in the woods.

Silent Hill 1 (1999)           Plain white subtitle lines, and telling the story through them rather than around them.


DATES

Milestone                      Date

Vertical slice playable        31 August 2026

itch.io release of the slice   First week of September 2026

Steam page with demo           Weeks after the itch.io release

Full seven-day game            TBD, aiming for Q1 2027




                                                                                                                                5
                                                              MR. MOONLIGHT (MVP) ·    GAME DESIGN DOCUMENT       ·   V0.2




  02 ST ORY


1978. AANNIARVIK ISLAND, ALASKA.

Seven friends are arriving at the point in life where the important decisions get made, and they are all quietly afraid
that this is where the friendship ends. So they take a break from the hard Alaskan winter routine and go to an island
for one last weeklong camping trip, with booze and enough other things to make it memorable.
Aanniarvik was inhabited by natives a long time ago. During the Second World War it became an American base,
waiting for a Japanese invasion that never came. Now it is an empty island with a population of one: a forest ranger,
the uncle of Holly, your childhood friend.
You are Tracey. Twenty-something, a history major who dropped out, in possession of some nasty habits and a
permanently foul mouth. You did not want to come. Your friends insisted far too much. Fine. One more time.


Camping as a kid was fun, but now everything feels heavy and stupid. Maybe I should go easy this
time…………………………………
Great, I feel great! Give me a minute… bleehh, false puke alarm everybody… hey! Hello? Not funny guys, where are my
boots?… where… where is everyone?




                                                                                                                          6
                                                                    MR. MOONLIGHT (MVP) ·         GAME DESIGN DOCUMENT           ·   V0.2




 03 CAST


Five characters exist in Day 1. Three more are named in dialogue but never appear. (ART WILL CHANGE)

                       Tracey
                       PLAYABLE
                       Addict, asshole, dull — her words. The player never sees her face, only her hands. Everything the player
                       learns about her comes from what she says out loud (or whatever is in her head).




                       Rylee
                       VOICE ON T HE RADIO
                       Lady jester. Wants to be a nurse; stand-up would suit her better. She has Tracey's boots, she is falling asleep
                       while talking, and she is the last friendly voice in the level.




                       Holly
                       AT T HE CABIN
                       Miss Perfect, and exhausting about it. She is at Vernon's cabin when Tracey arrives, and she is the one who
                       hands over the marijuana.




                       Scott
                       FOUND IN T HE MINE
                       Dodged the draft and still wants to join the air force. He transmits once on the radio, and after that he is an
                       unconscious body on a stretcher that the player has to drag out.




                       Vernon
                       AT T HE CABIN, T HEN ON T HE RADIO
                       Holly's uncle, the island's only resident. Tubercular, armed, and the only person who behaves like he knows
                       what is happening. He gives Tracey the M1911 and the morphine, points her at the mine, and later creates
                       the distraction that lets her run.




  NAMED BUT NOT PRESENT IN DAY 1
  Robert, William and Shannon are talked about in Rylee's radio conversation and appear in the Polaroid photograph.
  They need no model, no rig and no voice for the slice.
  Amaruq and Mr. Moonlight are named in the full-game fiction and do not appear anywhere in the Day 1 script. They
  are out of scope and are not described here.




                                                                                                                                         7
                                                                           MR. MOONLIGHT (MVP) ·           GAME DESIGN DOCUMENT           ·   V0.2




  04 GAME FLOW


The slice is one day, not seven. The loop below is what a player repeats scene by scene inside that day.




                  Figure 1 — the Day 1 loop. Compared to v0.1: the manual save system is gone, and the seven-day wrapper is gone.


WHAT CHANGED FROM VERSION 0.1

 Element                                    v0.1                                               Vertical slice

 Structure                                  Seven days, each with its own objective            One day, seven objectives inside it

 Saving                                     Limited-use manual save system                     Removed. Automatic checkpoint at the start
                                                                                               of each scene.

 Map                                        Regenerated procedurally every day                 One fixed, hand-built route

 Night deadline                             Reach shelter before 3:00 a.m. or die              Night arrives on script after the mine. The
                                                                                               clock is not a live mechanic yet

 Failure                                    Return to the beginning of the day                 Return to the start of the current scene


WHY THE SAVE SYSTEM HAD TO GO

A manual save with limited uses is a resource the player has to reason about, which means it needs a UI, a slot
system, a serialisation layer for every stat and every objective state, and a rule for what a save does to enemies mid-
encounter. That is a week of work that does not appear on screen. A scene checkpoint costs an afternoon: the runner
already knows which scene it is in, so restarting means reloading that scene and replaying its opening events.

                                                                                                                                                 8
                                                           MR. MOONLIGHT (MVP) ·    GAME DESIGN DOCUMENT   ·   V0.2


The following is the reference image of the original Game Flow as shown in the previous GDD versiou:




                                                                                                                  9
                                                                              MR. MOONLIGHT (MVP) ·             GAME DESIGN DOCUMENT              ·   V0.2




  05 T HE ISLAND IN DAY 1


Aanniarvik is a forest in the middle of the sea. In the full game its geography is rebuilt every morning. In the slice,
Day 1 runs on a single authored route, and the player walks it once.




          Figure 2 — the ten scenes of Day 1 and the objectives they carry. Scenes 08 to 10 exist as outline only and still have to be written.


THE ROUTE

The player moves east from the campsite to the Glade, then to Vernon's cabin, then into the mine, then north to the
church. There are no optional areas and no backtracking. The only branch in the level is at the bear trap, and it
changes which enemy the player meets, not where they go.

LOCATIONS

                          Location                                                                                   Where it appears in the
                                                                                                                     script

                          Camping site                                                                               Scenes 01–04
                          The RV, two tents, William's locked tent, the bonfire, the table with the
                          canteen, and two coolers. Everything the player learns in the first ten
                          minutes is taught here.




                                                                                                                                                        10
                                                                   MR. MOONLIGHT (MVP) ·            GAME DESIGN DOCUMENT        ·   V0.2



                    Location                                                                          Where it appears in the
                                                                                                      script

                    The forest road                                                                   Scene 05
                    The stretch east from the camp. A single wolf crosses at distance and
                    ignores Tracey. This is where fear is introduced.




                    The Glade                                                                         Scene 06
                    An observation post with a mounted telescope. The friends' camp,
                    abandoned mid-party. Boots, Polaroid, pickaxe in the telescope frame,
                    and a light in the distance.

                    Vernon's cabin                                                                    Scenes 07–08
                    More of a box than a cabin, warm inside, door covered in crosses. Holly
                    and Vernon are here. It is the only safe room in the level.




                    Flak tower                                                                        Scene 08
                    Visible in the distance. Cannot be entered. If the player walks toward it the
                    game communicates that it is full of cultists and is a suicide area.




                    Mineshaft                                                                         Scene 09
                    A mostly linear tunnel, entered with a lamp. Cultists inside. An infirmary
                    room on the far side holds Scott, supplies, a stretcher and an Arisaka rifle.



                    The church                                                                        Scene 10
                    Reached by heading north after the Virgin Mary statue and up the Hill of
                    Crosses, with a Furman in pursuit. Reaching it ends Day 1.




T WO LOCATIONS WERE CUT
The Dock and the Radio station / Workshop are described in v0.1 but never appear in the Day 1 script. They are
removed from the slice and stay in the full-game plan.




                                                                                                                                      11
                                                                          MR. MOONLIGHT (MVP) ·          GAME DESIGN DOCUMENT               ·   V0.2




  06 LOOK AND FEEL


KEYWORDS

Substance abuse · punk-acid style · foul language · crude combat · claustrophobic darkness · item management · exploration
· regret · monsters · traps · hide and seek · objective centric · night sky

ART STYLE

Low-poly 3D in the manner of the fifth console generation. Simple models with well-defined silhouettes, because
silhouette is the only thing the player can read in the dark. Textures are pixelated, produced with Pixel8r and
Substance Painter. The palette stays cold: green, grey and brown, high contrast, very little warm light except firelight.
UI is minimal and text-light, in a high-contrast punk and grunge register. Subtitles are plain white lines, exactly as in
Silent Hill 1.




    Firelight against cold ambient — the only warm source in the level.           Silhouette over detail. A cabin reads as a shape first.




          Night palette. Almost no colour information survives.                Hands and held objects carry the whole first-person frame.



SOUND DESIGN

Headphones are recommended, and the design assumes them. Sound is stereo-tuned with positional and doppler
tricks, and it carries information: it is how the player finds the radio, locates a patrol, and knows something is behind
them before they turn.

                                                                                                                                                  12
                                                                               MR. MOONLIGHT (MVP) ·            GAME DESIGN DOCUMENT              ·   V0.2


There is very little music. The slice has ambience beds, prop sources, enemy signatures and a three-stage breathing
layer tied to fear. Percussion tracks exist for special sequences and are not needed for Day 1.

THEMES

 Theme                               How Day 1 handles it

 Substance abuse                     The player is not told Tracey is an addict. Day 1 opens on a hangover played for comedy, and ends
                                     with Vernon handing her morphine and Holly handing her marijuana. Neither is explained. The system
                                     underneath them arrives properly on Day 2.

 Religion                            Orthodox Christian imagery from the first Russian settlers of Alaska: crosses nailed to a cabin door, a
                                     Virgin Mary statue, a hill of crosses, a church as the only shelter. No exposition. Meaning is left to the
                                     player.

 Ethics                              It is 1978 and everyone is young. The country is re-examining its morals after Vietnam and picking
                                     new boogeymen. Day 1 only plants this; the character arcs that carry it are later days.

 Mental health                       Tracey is hostile and prefers to be alone, and she was not always like that. Day 1 shows it only through
                                     what she mutters to herself. The heavier material is out of scope.


MOCKUP SCREENS

These are pre-production mockups from v0.1 and are not current builds. Two of them show equipment that is not in
the slice, noted below.




 Zealots close in on the road to the cabin. The buff item shown predates the
                                 current scope.
                                                                                        Caught in the bear trap — the branch point of Scene 07.




                              A Furman charges. The bone axe shown is not in the slice; in Day 1 Tracey carries the pickaxe.




                                                                                                                                                        13
                                                                         MR. MOONLIGHT (MVP) ·             GAME DESIGN DOCUMENT              ·    V0.2




  07 GAME ME CHANICS


Everything below exists in the Day 1 script. Nothing here is aspirational: if a system is listed, at least one event
line in L01.txt requires it.

7.1 WHAT THE PLAYER DOES

 Verb                    What it means                                                         When it unlocks

 Look                    Free camera. Blocked during scripted moments.                         After the first dialogue lines

 Move                    Walk. Slower while holding the radio.                                 After the vomit animation

 Sprint                  Faster, and noticeably louder than walking.                           When the boots go on, at the Glade

 Interact                One button. Picks up, opens, pulls, knocks.                           At the wristwatch, as the first tutorial

 Carry and drop          Backpack holds a limited number of items; the player                  At the blue cooler
                         chooses what to lose.

 Navigate                Deploy map and compass. Locks Tracey in place while                   From William's tent
                         open.

 Swing                   Heavy, slow pickaxe blows that drain stamina.                         Pulled from the telescope frame

 Shoot                   M1911, then the Arisaka. Loud, scarce, and a last resort.             Vernon's cabin, then the mine infirmary

 Drag                    Pull Scott on the stretcher. Movement and combat are                  The mine infirmary
                         restricted.




                           Figure 3 —Action layout. Faint melee is struck through: it was cut in v0.1 and stays cut.


7.2 SYSTEMS IN THE SLICE

Twenty systems. The last one is the keystone — without it nothing else runs in sequence.

 System               What the player sees                                What it has to hold                          Built from

 Player controller    Walking, looking, sprinting, first-person           Speed, sprint state, noise level.            Owned FPS asset, adapted
                      arms.

 Control locks        The camera or the legs stop answering               Two independent boolean locks                Systems Smith
                      during a scripted beat.                             that always get released.



                                                                                                                                                    14
                                                                     MR. MOONLIGHT (MVP) ·           GAME DESIGN DOCUMENT            ·   V0.2



 System               What the player sees                           What it has to hold                    Built from

 Interaction          A prompt icon appears when something can       Range, line of sight, required item.   Owned FPS asset
                      be used.

 Inventory            The fifth pickup is refused and Tracey         Capacity, contents, discard.           Systems Smith
                      complains.

 Stamina              A bar that appears for the first time during   Current, max, drain and regen          Systems Smith
                      the vomiting, then drains and refills.         rates.

 Health and           Getting bitten hurts and does not come back    Current, max, damage sources.          Systems Smith
 damage               on its own.

 Fear                 Chromatic aberration, camera shake, and        A single fear value with thresholds    Systems Smith
                      breathing that gets heavier.                   that drive VFX and audio.

 Melee                Slow pickaxe swings that cost stamina and      Damage, swing time, stamina cost,      Owned FPS asset, extended
                      stagger a Furman.                              stun.

 Firearms             Two guns, arriving late, loud enough to        Damage, fire rate, ammo count.         Owned FPS asset
                      matter.

 Map and compass      The screen fills with a paper map and Tracey   Player heading, position, deploy       Systems Smith
                      stops moving.                                  lock.

 Light                A mining lamp in the tunnel, matches as an     Range, intensity, fuel or battery.     Systems Smith
                      emergency.

 Substances           Morphine and marijuana are handed over         Instant buff, timed drawback.          Systems Smith, minimal
                      and can be used once.                                                                 version

 Bear trap            A snap, a large chunk of health and stamina    Trigger volume, damage, injured        Systems Smith
                      gone, and a limp.                              state.

 Stretcher escort     Scott comes with you, slowly, and you          Attach point, speed penalty,           Systems Smith
                      cannot fight properly.                         restrictions.

 Objective tracker    A line in the pause menu that changes as the   Start, update and end for seven        Level Weaver
                      day goes wrong.                                objectives.

 Subtitles            Plain white lines, typewriter or immediate.    Text, colour, display method, on-      Nani Novel, adapted
                                                                     screen time.

 Audio manager        Ambience, prop sources, enemy signatures,      Mixer states driven by fear and        Systems Smith
                      breathing.                                     location.

 Scene checkpoint     Dying puts you back at the start of the        Current scene index and its entry      Systems Smith
                      current scene.                                 state.

 Time of day          Morning at the camp, dusk at the cabin, full   A lighting set per scene. Not a live   Baked lightmaps
                      dark at the mine exit.                         clock.

 SLDD runner          Nothing directly — it is why every other       Parses L01.txt and fires each event    Level Weaver
                      thing happens in order.                        in sequence.


7.3 HOW THE LEVEL SCRIPT DRIVES THE ENGINE

This is the part of the project that is genuinely unusual, and it is the reason an agent workflow is worth the trouble.
Day 1 is not scripted inside Unity. It is written in a plain-text format of my own, the Script Level Design Document, as
223 numbered event lines. Each line is one event, with a fixed type and a fixed parameter list, separated by double
pipes. A line looks like this:



                                                                                                                                           15
                                                                   MR. MOONLIGHT (MVP) ·          GAME DESIGN DOCUMENT          ·   V0.2


L01E-039 || PFX || Name: Stamina refill || Description: Refill part of the stamina bar and begin slow stamina recovery. ||
Stat: N/A || Magnitude: N/A || Duration: N/A || Stacking: F || Curve: N/A

Because the format is fixed, it parses. The runner reads the file, turns every line into a ScriptableObject, and plays
them in order. Changing the level means editing a text file, not rewiring a scene — which is exactly the kind of work
an agent can do reliably and a human cannot do quickly.
Each event type maps to one implementation. That mapping is the contract between the script and the engine:

 Type               Meaning                         Unity implementation                                     Built by

 PA                 Player action                   Trigger volume or interactable, gated on an input        Level Weaver
                                                    action

 SA                 System action                   A system event object invoked by the runner              Level Weaver

 D:@ / T:@ / SM     Dialogue, thought, system       Subtitle event through the Nani Novel adapter            Level Weaver
                    message

 HA                 Hand animation                  Animator trigger on the first-person rig                 Systems Smith

 WA / CA:@ / EA:@   World, character, enemy         Animator trigger on the named target                     Systems Smith
                    animation

 CB:B / MB:B        Camera and movement block       Sets or clears a control lock flag                       Systems Smith

 C                  Cutscene                        A Timeline asset driven by a playable director           Level Weaver

 VFX:UI             UI effect                       Canvas group or UI animator                              Systems Smith

 VFX:PV             Player-view effect              URP volume override on the camera                        Systems Smith

 SFX                Sound                           Audio manager cue, 2D or positioned                      Systems Smith

 PFX                Player effect                   Stat modifier applied to the player stats block          Systems Smith

 O:#:S / U / E      Objective start, update, end    Objective tracker entry                                  Level Weaver

 OL                 Outline — not a real type yet   Nothing. These 26 lines cannot be built until they are   Mustard, by hand
                                                    converted into real event types.




NOTE: The current script file in a txt engine will be obfuscated and stored within Unity run files.




                                                                                                                                      16
                                                                       MR. MOONLIGHT (MVP) ·        GAME DESIGN DOCUMENT               ·   V0.2




08 ENEMIES AND T HREATS


                  Enemy                                                                      Behaviour to build

                  Wolf                                                                       Roam · circle the player · bite · break off
                  E-W                                                                        when struck · flee when hurt · afraid of fire
                  Introduced at distance on the forest road, where it crosses the path
                  and ignores Tracey entirely — she is barefoot and cannot chase it. It
                  returns as a pack at the Glade, after the telescope, as the first real
                  fight.




                  Cultist Zealot                                                             Hidden · charge on sight · melee · follow at
                  E-Z                                                                        distance if the player escapes · low health
                  Branch A of the road to the cabin. Two of them ambush on the path if
                  the player avoided the bear trap. The fight must be winnable with the
                  pickaxe and nothing else.




                  Cultist Spotter                                                            Patrol with a lamp · ignore at distance ·
                  E-S                                                                        whistle to summon · never lose interest once
                  Branch B. If the player is caught in the trap, the zealots do not come.    alerted
                  Two spotters patrol at distance with flashlights instead, and stay non-
                  hostile unless approached. Fighting them while injured is meant to kill
                  you.




                  Furman                                                                     Charge · heavy bites · raises fear on approach
                  E-F                                                                        · large health pool · staggered by a heavy
                  Appears once, in the night escape, pursuing Tracey up the Hill of          blow
                  Crosses while the ground shakes and the sky turns red. It is a chase,
                  not an encounter — she is not expected to win it.




                  Bear trap                                                                  Trigger volume · one-shot · applies the
                  —                                                                          injured state · gates the branch
                  One trap, on the road to the cabin. It cannot kill, but it takes a large
                  amount of health and stamina and it decides which of the two
                  branches the player gets. It is the only real choice point in the level.




CUT FROM T HE ENEMY ROST ER
Stone totems, the Cultist Priest and punji traps appear in v0.1 but not in the Day 1 script. All three are removed from
the slice. The priest in particular carries ranged weapons, poison and later spellcasting — a whole combat category the
slice does not need.


                                                                                                                                             17
                                                             MR. MOONLIGHT (MVP) ·           GAME DESIGN DOCUMENT             ·    V0.2




 09 IT EMS


Seventeen objects. Every one of them is picked up, handed over or used somewhere in the Day 1 script.

                Item                       Role in Day 1

                Canteen                    The first thing Tracey wants. Drinking clears her vision and starts stamina recovery.
                CONSUMABLE, REFILLABLE     Teaches the interact button after the alarm.




                Walkie-talkie              Found in the red cooler behind the RV. Carrying it slows Tracey down while she talks.
                TOOL                       Later it is how Scott and Vernon reach her.




                Boots                      The entire first half of the level is about getting them back. Putting them on at the
                KEY ITEM                   Glade unlocks sprinting — and sprinting is loud.

                William's tent key         Under the rug beneath the RV, because Rylee says so. Opens the tent that holds the
                KEY ITEM                   compass.

                Map and compass pouch      Taken from inside a parka in William's tent. Enables navigation. Deploying it locks
                TOOL                       Tracey in place.



                Polaroid photograph        Lying near the table in the abandoned Glade. A picture of the whole group. Tracey
                KEY ITEM                   stows it in the compass pouch and says nothing.

                Inuit pickaxe              Buried in the telescope frame. Heavy, slow, medium reach, and the only weapon for
                MELEE WEAPON               the middle of the level.




                Matches                    In the red cooler with the radio. Emergency light source.
                LIGHT




                Beer                       Two of them in the blue cooler. Present as a pickup; no scripted use in Day 1. Part of
                CONSUMABLE                 the substance system from Day 2 onward.

                Soda can                   Two in the blue cooler, one at the Glade. Small heal and a stamina boost.
                CONSUMABLE




                                                                                                                                     18
                                                                  MR. MOONLIGHT (MVP) ·             GAME DESIGN DOCUMENT                  ·   V0.2



                Item                           Role in Day 1

                Crackers                       Three packets in the blue cooler. Small heal, slight stamina.
                CONSUMABLE




                Mining lamp                    Obtained at the mine entrance. Without it the tunnel is not navigable.
                LIGHT




                M1911 pistol                   Given by Vernon at the cabin. Reliable, high stopping power, and very loud in a forest
                FIREARM                        full of people listening.



                Morphine                       Given by Vernon alongside the pistol. Fast healing and damage reduction, at the cost
                SUBSTANCE                      of nausea and rising fear.

                Marijuana                      Given by Holly at the cabin. Reduces fear and hand shake; affects hearing.
                SUBSTANCE

                Arisaka rifle                  In the mine infirmary next to Scott. Long range, high damage, and awkward to use
                FIREARM                        while dragging a stretcher.




                Stretcher                      In the infirmary. Scott goes on it, and the last third of the level is spent pulling it.
                KEY ITEM




CUT FROM T HE IT EM LIST
Ka-Bar knife, double barrel, crossbow, Zippo, gas can, flashlight, D batteries and general ammunition all appear in v0.1
and none of them appear in the Day 1 script. They are out of the slice.




                                                                                                                                                19
                                                                       MR. MOONLIGHT (MVP) ·             GAME DESIGN DOCUMENT      ·   V0.2




  10 AI ARCHITECT URE


Eight agents, all of them development tools. None of them ships inside the game, and the player never talks to a
model.

10.1 HOW THIS WORKS

The project has three documents that never move: the format specification, the Day 1 level script, and this design
document. Every agent session begins by reading them. That is the whole trick — the agents are not asked to be
creative, they are asked to turn a document that already exists into a Unity project that matches it.
Work flows in one direction. Agents produce changes, I review and test every one of them in the editor, and I am the
only thing that commits. Build logs and bugs flow back the other way.




                                     Figure 4 — the crew. Five agents run daily; three runs on demand.


10.2 THE CREW

 Agent                What it does in development                        What the player ends up seeing            Hard boundary

 Script Warden        Checks every line of the level script against      Objectives that always close, cutscenes   Reports defects. Never
 HAIKU 4.5            the format specification and reports what is       that always hand the camera back, and     edits the script.
                      broken.                                            no dead entry left sitting in the pause
                                                                         menu.




                                                                                                                                         20
                                                                        MR. MOONLIGHT (MVP) ·          GAME DESIGN DOCUMENT            ·    V0.2



 Agent                What it does in development                        What the player ends up seeing             Hard boundary

 Slice Producer       Turns the validated script into an ordered task    One finished day instead of five half-     Plans only. Writes no
 HAIKU 4.5            list and picks what gets built today.              finished systems.                          game code.

 Level Weaver         Converts script lines into Unity event assets,     The level happening in the right order:    Only builds what a
 SONNET 5             timelines and objective entries.                   the alarm, then the water, then the        script line asks for.
                                                                         boots, then the dark.                      Invents no events.

 Systems Smith        Writes the gameplay C# — stamina, fear,            How the game feels in the hand: the        One system per
 SONNET 5             inventory, interaction, melee, locks and the       weight of a swing, the bar draining, the   change. No refactors
                      audio manager.                                     breathing getting worse.                   outside the named
                                                                                                                    files.

 Enemy Brain          Implements and tunes exactly four enemy            Wolves that circle instead of sprinting    No fifth enemy without
 SONNET 5             state machines and nothing else.                   straight at you, and spotters that         approval.
                                                                         genuinely do not notice you if you wait.

 QA Hunter            Runs compile checks and builds, classifies the     A build that starts, a level that can be   Fixes only trivial
 HAIKU 4.5            logs, and writes reproducible bug reports.         finished, and fewer things breaking on     isolated errors.
                                                                         release day.                               Escalates the rest.

 Package              Reads the purchased packages and maps their        Movement and shooting that keep the        Read-only. Cannot
 Cartographer         prefabs, events and extension points before        feel they were tuned with, instead of      modify a single file.
 SONNET 5             anything is touched.                               breaking after every edit.

 Scribe               Updates the architecture notes, the changed-       Nothing directly — it is what stops the    Documents decisions
 HAIKU 4.5            file log and this document's status after          other seven agents working from stale      already made.
                      approved changes.                                  information.


10.3 WHAT THEY SHARE

The agents do not talk to each other directly. They share four files in the repository, and that is the entire
coordination mechanism:
 • script-defects.md — written by the Script Warden, read by the Slice Producer and by me.
 • today.md — written by the Slice Producer. The task list, in order, with the event IDs each task covers.
 • package-map.md — written by the Package Cartographer. Which prefabs and events may be extended, and
   which files must not be touched.
 • build-report.md — written by the QA Hunter after every build attempt.
Keeping coordination in flat files rather than in a live framework means a failed run costs nothing: the file is either
there or it is not, and I can read it myself.

10.4 RULES THE AGENTS WORK UNDER

 1. Nothing gets invented. If a needed detail is not in the three source documents, the agent marks it TBD and
    stops.
 2. The format specification wins on format, the level script wins on Day 1 content, this document wins on
    everything else.
 3. Purchased packages are wrapped, not rewritten. Adapters go in our own namespace.
 4. One merged change per system per day. Anything larger cannot be reviewed honestly by one person.
 5. Every change arrives with the event IDs it implements, so it can be traced back to a line in the script.




                                                                                                                                              21
                                                               MR. MOONLIGHT (MVP) ·      GAME DESIGN DOCUMENT          ·   V0.2




  11 T OKEN BUDGET AND API CONST RAINT S


Pay-as-you-go pricing, verified against Anthropic's published rates on 30 July 2026.

11.1 ASSUMPTIONS

 • 22 active development days between 31 July and 31 August 2026. Not every calendar day is a working day.
 • A session is four to six hours with several tool calls, repeated file reads and a share of failed attempts.
 • Prompt caching is on for the three source documents, which are re-read constantly. Cache hits cost a tenth of
   standard input.
 • Rates used: Haiku 4.5 at $1 / $5 per million tokens in and out. Sonnet 5 at $2 / $10 under the introductory rate.
   Opus 5 at $5 / $25, used only for escalation.

11.2 COST PER ACTIVE DAY

 Agent                             Model               Input            Output          Cost per day

 Script Warden                     Haiku 4.5            60k                  8k         $0.10

 Slice Producer                    Haiku 4.5            40k                  6k         $0.07

 Level Weaver                      Sonnet 5             200k               30k          $0.70

 Systems Smith                     Sonnet 5             250k               40k          $0.90

 Enemy Brain                       Sonnet 5             120k               20k          $0.44

 QA Hunter                         Haiku 4.5            150k               15k          $0.23

 Scribe                            Haiku 4.5            40k                  8k         $0.08

 Package Cartographer              Sonnet 5             100k               10k          $0.30 amortised, twice a week

 Total                                                                                  $2.82 per active day


11.3 COST FOR THE WHOLE SLICE

 Line                                                                Basis                         Cost

 Daily crew                                                          22 days at $2.82              $62

 Opus 5 escalation for hard bugs                                     about 14 runs at $1.38        $19

 Subtotal                                                                                          $81

 Contingency for retries and wasted runs                             50%                           $122 ceiling



Call it eighty dollars expected and a hundred and twenty-five worst case, for a playable vertical slice. On a Claude Max
subscription these are not charges at all — plan usage limits apply instead, and the daily figures above sit comfortably
inside them.




                                                                                                                              22
                                                                  MR. MOONLIGHT (MVP) ·        GAME DESIGN DOCUMENT          ·   V0.2


11.4 THE FOUR CONSTRAINTS THAT ACTUALLY BITE

Constraint                       What it means for this project

The Sonnet 5 introductory rate   From 1 September the rate goes from $2 / $10 to $3 / $15. Sonnet does the heavy lifting here, so
ends on 31 August 2026           the same work costs about fifty per cent more the day after the slice is due. This is the single
                                 clearest reason the schedule in section 14 ends on 31 August rather than drifting into September.

Context, not price, is the       The FPS package and the terrain package are large. An agent that reads a whole repository burns
binding limit                    its window before it writes anything useful. Agents search and read targeted ranges; whole-folder
                                 dumps are forbidden in every agent prompt.

The reviewer is the bottleneck   One person can generate far more code with agents than one person can read, test in the editor
                                 and be honest about. The cap of one merged change per system per day is a real limit on
                                 throughput, and it is deliberate.

No network at runtime            The shipped build makes no API calls. That removes per-player cost, provider outages and key
                                 management from the release entirely, and it means the budget above is the whole budget — it
                                 does not scale with players.




                                                                                                                                     23
                                                                        MR. MOONLIGHT (MVP) ·            GAME DESIGN DOCUMENT            ·   V0.2




  12 FEEDBACK : CUT FROM THE VERTICAL SLICE


Everything here was in version 0.1. None of it appears in the Day 1 script, so none of it is in the slice.

 Cut                                   Why                                                                  Comes back

 Procedural island generation          Day 1 runs on one fixed route through eight locations. The           Full game. It is the headline
                                       generator is never exercised by the script, and at roughly ten       feature and it is not going
                                       days of work it is the largest single item in the old plan.          away.
                                       Building it now would consume a third of the schedule to
                                       produce something the slice cannot show.

 Manual save system                    Needs a UI, a slot system and serialisation of every stat and        Full game, if playtesting says it
                                       objective. Scene checkpoints cost an afternoon and cover the         is missed.
                                       same failure case.

 The seven-day structure               Days 2 and 3 were in the old MVP definition. One finished day        Days 2 and 3 immediately after
                                       demonstrates the game; three unfinished ones demonstrate             the slice ships.
                                       nothing.

 The 3:00 a.m. deadline as a live      Night arrives on script after the mine. The script has no clock      Day 2, where it becomes the
 clock                                 mechanic and no fail-by-time state anywhere in Day 1.                point.

 Shrooms                               Not present anywhere in Day 1. Marijuana and morphine are            Day 2, with the full substance
                                       handed over at the cabin; alcohol exists only as a pickup.           system.

 Stone totems, Cultist Priest, punji   Absent from the script. The priest alone brings ranged               Days 2 and 3.
 traps                                 combat, poison and hallucination effects.

 Dock, Radio station / Workshop        Never visited in Day 1.                                              Later days.

 Ka-Bar, double barrel, crossbow,      None appear in the script. The slice has one melee weapon            As their days require.
 Zippo, gas can, flashlight,           and two firearms.
 batteries

 Melee faint, telescope star           Already cut in v0.1 for scope and complexity. Still cut.             Full game, possibly never.
 minigame



Another point to mention here is what type of feedback I was able to really take for the MVP. Most of the cuts were
thanks to the feasibility check of the agent critique crew. And also me bitting the bullet to reduce as much as possible.
However after several rounds of evaluation, the agents can begin to loop into their own fixiations, this is the point
where you must take calls on how will your game really look like at the end. The following is a round of evaluations
from the agents in console:




                                                                                                                                                24
MR. MOONLIGHT (MVP) ·   GAME DESIGN DOCUMENT   ·   V0.2




                                                     25
                                                                  MR. MOONLIGHT (MVP) ·          GAME DESIGN DOCUMENT               ·   V0.2




 13 MVP Critical Route


13.1

CRITICAL FEATURES

Everything needed to build the slice, with the intended method in brackets. Where an owned asset can do the job, it
does the job.

A. Environment and level art
 Feature or asset                                                    How it gets built

 Day 1 terrain, one fixed route                                      Hand-sculpted Unity Terrain. Borrow the biome textures and scatter
                                                                     brushes from the terrain package; do not run the generator

 Trees, grass, rocks, soil textures                                  Terrain package assets, topped up with free Unity packs

 Fog and mist                                                        Unity VFX Graph, hand-authored per scene

 Water surface                                                       Terrain package shader

 Campsite set — RV, two tents, bonfire, table, two coolers, rug      Blender, base meshes via Meshy where it saves time, textures in
                                                                     Substance and Pixel8r

 Glade set — telescope, sleeping bags, scattered belongings          Blender and Substance

 Vernon's cabin, exterior and small interior                         Blender

 Mine entrance, linear tunnel, infirmary room                        ProBuilder greybox first, art pass second

 Flak tower, distance silhouette only                                Blender, low detail, far LOD

 Church exterior and entrance                                        Blender

 Hill of Crosses, Virgin Mary statue                                 Blender, kitbashed from one cross mesh

 Lighting sets: morning, dusk, night                                 Baked lightmaps, one per scene, hand-authored


B. Characters and creatures
 Feature or asset                                                    How it gets built

 Tracey first-person rig — arms and hands only                       FPS asset rig, retargeted

 Holly, Scott, Vernon                                                Meshy from the existing concept art, rigged in Mixamo

 Wolf                                                                Asset store quadruped, or Meshy plus Mixamo

 Cultist Zealot and Spotter                                          One base body, two material and prop variants

 Furman                                                              Meshy plus hand cleanup in Blender — highest art risk in the
                                                                     project

 Rylee                                                               Nothing to build. She is a voice on a radio


C. Animation
 Feature or asset                                                    How it gets built

 Eighteen first-person hand animations required by the script        GoPro POV footage through DeepMotion or QuickMagic, cleaned in
                                                                     Blender




                                                                                                                                          26
                                                                           MR. MOONLIGHT (MVP) ·             GAME DESIGN DOCUMENT         ·   V0.2



 Feature or asset                                                               How it gets built

 Enemy animation sets, one per state, four enemies                              Mixamo, retargeted

 NPC idle and talk for Holly and Vernon; Scott unconscious                      Mixamo

 Animation event blockers, player and enemy                                     Systems Smith agent


D. Audio
 Feature or asset                                                               How it gets built

 Ambience beds: forest day, forest night, mine, cabin                           Freesound library, edited in Audacity

 Three-stage breathing layer tied to fear                                       Recorded, processed in FL Studio

 Enemy signatures: wolf, zealot, spotter whistle, Furman charge                 Freesound and FL Studio

 Props: Seiko alarm, radio loop, drinking, pickaxe hit, trap snap, earthquake   Freesound and FL Studio
 bed

 Non-verbal vocalisations for Tracey — gasps, grunts, retching                  Recorded. This replaces full voice acting for the slice

 Audio manager driven by fear state and location                                Systems Smith agent, on the Unity audio mixer


E. User interface
 Feature or asset                                                               How it gets built

 Subtitle renderer, Silent Hill 1 style, typewriter and immediate               Nani Novel, adapted for first-person use

 Stamina bar with reveal and hide                                               Systems Smith agent

 Health indicator                                                               Systems Smith agent

 Interaction prompt icon                                                        FPS asset UI, restyled

 Backpack screen with discard                                                   Systems Smith agent

 Pause menu with the objective list                                             Level Weaver agent

 Map and compass overlay                                                        Systems Smith agent

 Title, pause and restart screens                                               Hand-built in Unity UI

 Post-processing: blur, chromatic aberration, blackout fade                     URP volume overrides, hand-tuned


F. Gameplay systems
 Feature or asset                                                               How it gets built

 Player controller adaptation                                                   Owned FPS asset, wrapped by the Systems Smith agent

 Camera and movement locks                                                      Systems Smith agent

 Interaction system                                                             Owned FPS asset

 Inventory with capacity limit and discard                                      Systems Smith agent

 Stamina, health and damage                                                     Systems Smith agent

 Fear state driving visuals and audio                                           Systems Smith agent

 Melee with the pickaxe                                                         FPS asset melee, extended

 Two firearms                                                                   FPS asset fire system




                                                                                                                                                27
                                                                  MR. MOONLIGHT (MVP) ·         GAME DESIGN DOCUMENT           ·   V0.2



 Feature or asset                                                    How it gets built

 Map and compass navigation with a deploy lock                       Systems Smith agent

 Light sources: lamp and matches                                     Systems Smith agent

 Morphine and marijuana effects                                      Systems Smith agent, minimal version

 Bear trap and the injured state                                     Systems Smith agent

 Stretcher escort                                                    Systems Smith agent

 Four enemy state machines                                           Enemy Brain agent

 Objective tracker for seven objectives                              Level Weaver agent

 Scene checkpoint and restart                                        Systems Smith agent

 SLDD parser and event runner                                        Level Weaver agent. This is the keystone — nothing else
                                                                     sequences without it


G. Level scripting and content
 Feature or asset                                                    How it gets built

 Write Scenes 08, 09 and 10 as real event lines                      Mustard, by hand. Twenty-six outline lines to convert

 Add the outline type to the format specification, or retire it      Mustard, decision needed first

 Fix objective 4, which is never started                             Mustard, flagged by the Script Warden

 Fix the objective 3 title mismatch at the closing line              Mustard, flagged by the Script Warden

 Add camera and movement block pairs around both cutscenes           Mustard, flagged by the Script Warden

 Split the lines that mix two concerns                               Mustard, flagged by the Script Warden

 Renumber the duplicated and zeroed event IDs                        Script Warden reports, Mustard applies

 Import the finished script into Unity as event assets               Level Weaver agent


H. Build and release
 Feature or asset                                                    How it gets built

 Windows x64 build pipeline                                          QA Hunter agent

 itch.io page, capsule art, screenshots, short gif                   Photoshop

 Controls readme and content warning                                 Scribe agent, reviewed

 Playtest pass with three outside players                            Mustard. Non-negotiable before release




                                                                                                                                     28
                                                                          MR. MOONLIGHT (MVP) ·          GAME DESIGN DOCUMENT                   ·   V0.2




 14 T ECHNICAL ST RAT EGY AND T IMELINE


14.1 SEVEN STEPS

          Step                                                                                         Done when

 1        Finish the Claude tutorial and set up the crew                                               Eight agent files exist and one crew run
          Before anything else. The workflow is the part I am weakest on, and every day after this     produces a usable task list
          one is cheaper if this one is done properly. Write the eight agent prompt files, fix the
          repository conventions, and do one full run end to end.

 2        Clean the level script                                                                       The Script Warden reports zero defects on
          The script is the contract every agent reads. Fix the objective that is never started, fix   L01.txt
          the title mismatch, decide what happens to the outline type, and write Scenes 08 to 10
          as real event lines. Nothing downstream can be trusted until this is done.

 3        Map what I already own                                                                       package-map.md exists and I have read it
          A read-only pass over the FPS package and the terrain package. Find the extension
          points, the prefabs that matter and the files that must not be touched. Decide wrap or
          modify for each one, in writing.

 4        Build the script runner                                                                      Scene 01 plays start to finish, driven
          The parser and the event system that turns the text file into a playing sequence. This is    entirely from the text file
          the keystone and the single highest-risk piece of the project. Prove it on Scene 01
          before going wide.

 5        Greybox the whole route                                                                      I can walk Day 1 end to end in the editor
          Every location, in blocks, walkable from the campsite to the church. Ugly is fine.
          Playable before pretty, because a level that is beautiful and unfinished proves nothing.

 6        Layer in the systems and the enemies                                                         All seven objectives fire and both bear-
          Stamina, fear, inventory, navigation, combat, the bear trap branch, the escort. Then the     trap branches are survivable
          four enemies. Against the greybox, so failures are obvious.

 7        Art, audio, build, ship                                                                      A build a stranger can finish without me in
          Replace blocks with models, lay in the audio, bake the lighting, build, playtest with        the room
          three people who did not make it, and put it on itch.io.


14.2 CHRONOGRAM

Thirty-two days, 31 July to 31 August 2026. Two tracks running in parallel, because the agents write code while I make
art — that is the only way this fits.

 Dates                     Agent track — code                                             My track — art, audio, writing

 Fri 31 Jul – Sun 2        Step 1. Claude tutorial. Write the eight agent prompts.        Collect reference for the campsite and the Glade.
 Aug                       Repository conventions. One full crew run.

 Mon 3 – Sun 9 Aug         Steps 2 and 3. Script Warden runs clean. Package map           Write Scenes 08 to 10 as real event lines. Campsite
                           written. Runner started.                                       and Glade blockout.

 Mon 10 – Sun 16           Step 4. Runner finished. Scenes 01 to 04 play from the         Forest, cabin and mine greybox. Eighteen hand
 Aug                       text file.                                                     animations captured.

 Mon 17 – Sun 23           Steps 5 and 6a. Full route walkable. Inventory, stamina,       Enemy models and animation sets. Lighting sets
 Aug                       fear, navigation, melee.                                       baked.




                                                                                                                                                      29
                                                                       MR. MOONLIGHT (MVP) ·          GAME DESIGN DOCUMENT               ·   V0.2



Dates                  Agent track — code                                             My track — art, audio, writing

Mon 24 – Sun 30        Step 6b. Four enemies live. Bear-trap branches. Escort.        Audio pass. UI pass. Church, Hill of Crosses, flak tower
Aug                    Night escape.                                                  silhouette.

Mon 31 Aug             Step 7. First full build. QA Hunter pass. Fix blockers only.   Playtest with three people. itch.io page assets.



WHERE T HIS SCHEDULE BREAKS, AND WHAT I DO ABOUT IT
The pressure valve is the mine. Scenes 08 to 10 are outline only today. If they are not written as real event lines by 9
August, the mine gets cut to a single short corridor with one encounter, and the night escape loses the circle-of-fire
ambush. The route still runs camp to church, and the slice still ends where it should.
The art risk is the Furman. It is the only creature with no close equivalent to buy. If it is not working by 23 August, the
night escape becomes a pursuit by sound and light with the creature never fully seen — which is arguably better horror
and is certainly cheaper.
The date is fixed by more than pride. Sonnet 5 pricing rises on 1 September. Slipping the slice into September raises
the cost of the remaining work by about half.




                                                                                                                                               30
