# Prop List by Scene

Low poly, PS1 and N64 era. Pixelated textures, strong silhouettes,
cold high contrast palette. `explicit` means the script or GDD names it;
`inferred` means the prop master is proposing it.

_87 props across 10 scenes; 77 named in source, 10 proposed._

## Scene 01 — Waking At The Campsite

| Prop | Category | Source | Why | Modelling |
|---|---|---|---|---|
| Two-person canvas tent, period | `environment` | `explicit` | The space Tracey wakes in; frames the opening shot | Low poly shell, interior and exterior, one shared texture |
| Sleeping bag, unzipped | `set_dressing` | `explicit` | Sells that she went down where she fell | Single mesh, cloth baked in |
| Seiko wristwatch with alarm | `interactable` | `explicit` | The first interaction in the game | Small hero prop, needs a readable face |
| Canteen, aluminium | `interactable` | `explicit` | First pickup and the water she is desperate for | Reused across the level |
| Blue cooler | `interactable` | `explicit` | Where the carry limit is taught | Box mesh, lid opens, reused as red cooler |
| Red cooler | `interactable` | `explicit` | Second cooler for the fifth-item refusal | Material swap on the blue cooler |
| Bonfire, extinguished | `set_dressing` | `explicit` | Cold camp reads as morning-after | Stone ring plus charred log kit |
| Beer bottles, scattered | `set_dressing` | `explicit` | Last night, told without dialogue | One bottle mesh, scattered instances |
| Camping chairs, folding | `set_dressing` | `inferred` | Fills the camp silhouette cheaply | One mesh, two rotations |
| First-person hands and forearms | `environment` | `explicit` | Carries the whole frame per the GDD | FPS rig, retargeted, highest priority |
| Vomit decal | `set_dressing` | `explicit` | The opening beat lands physically | Decal, not geometry |
| RV exterior | `environment` | `explicit` | Landmark that anchors the campsite | Exterior only, no interior needed |

## Scene 02 — The Missing Boots

| Prop | Category | Source | Why | Modelling |
|---|---|---|---|---|
| Hiking boots, Tracey's | `interactable` | `explicit` | The object the whole scene is about | Hero prop, seen close in hand |
| Wet wool socks | `set_dressing` | `explicit` | Sells barefoot without changing the rig | Texture variant on the hands rig |
| Muddy ground, footprint decals | `environment` | `explicit` | Someone took them and left a trail | Decal set, four variants |
| Tent flap, animated | `interactable` | `explicit` | Opens and closes across the level | Single hinge mesh, reused |
| Clothes line with hanging laundry | `set_dressing` | `inferred` | Camp habitation and cheap silhouette | Plane cards plus rope spline |
| Backpack, Tracey's | `interactable` | `explicit` | The carry limit made visible | Hero prop, seen in inventory UI |
| Pine tree kit, three variants | `environment` | `explicit` | Bulk of the forest | LOD'd instances, single atlas |
| Rock kit, five variants | `environment` | `inferred` | Ground variation and hazard for bare feet | One atlas, heavy reuse |

## Scene 03 — Radio Conversation With Rylee

| Prop | Category | Source | Why | Modelling |
|---|---|---|---|---|
| Walkie talkie handset | `interactable` | `explicit` | The scene is this object | Hero prop, held close to camera |
| RV interior rug | `interactable` | `explicit` | Hides the tent key beneath it | Plane with lifted-corner animation |
| Tent key, small brass | `interactable` | `explicit` | Opens William's tent | Tiny mesh, needs a strong silhouette |
| Camp table, folding | `set_dressing` | `explicit` | Surface for the Polaroid and drinks | Simple box construction |
| Soda can, period | `set_dressing` | `explicit` | 1978 dressing, cheap | One mesh, decal label |
| Radio antenna, extended | `set_dressing` | `inferred` | Explains reception at the camp | Cylinder, no detail needed |
| Ash and cold firepit | `set_dressing` | `explicit` | Reused from scene 01 | Direct reuse |

## Scene 04 — Will'S Tent And The Compass

| Prop | Category | Source | Why | Modelling |
|---|---|---|---|---|
| William's tent, exterior and interior | `environment` | `explicit` | The only interior in the first act | Interior needed — budget for it |
| Padlock, broken | `interactable` | `explicit` | The lock the key opens | Small mesh, two states |
| Compass, brass, period | `interactable` | `explicit` | Core navigation item | Hero prop, readable needle, UI-facing |
| Paper map, folded and unfolded | `interactable` | `explicit` | Locks Tracey in place when deployed | Two meshes plus a high-res texture |
| Neck pouch, canvas | `interactable` | `explicit` | Holds the compass and map | Small mesh, worn on rig |
| Parka, hanging | `set_dressing` | `explicit` | Where the pouch is found | Cloth mesh, no simulation |
| Scattered clothing | `set_dressing` | `explicit` | Optional examine beat | Three flat meshes, reused |
| Camp lantern, unlit | `set_dressing` | `inferred` | Foreshadows the light system | Reused as the mine lamp later |

## Scene 05 — The Forest Road To The Glade

| Prop | Category | Source | Why | Modelling |
|---|---|---|---|---|
| Forest road, dirt path mesh | `environment` | `explicit` | The authored route itself | Spline-based, hand-placed |
| Wolf | `environment` | `explicit` | First enemy sighting, at distance | Asset store quadruped or Meshy plus Mixamo |
| Fog volume and particles | `environment` | `explicit` | Draw distance and dread, cheaply | Particle system, no geometry |
| Undergrowth and fern cards | `environment` | `explicit` | Fills forest floor | Billboard cards, one atlas |
| Fallen log, mossy | `set_dressing` | `inferred` | Breaks sightlines along the path | Two variants, heavy reuse |
| Distant flak tower silhouette | `environment` | `explicit` | Landmark visible from the road | Far LOD only, no detail |

## Scene 06 — The Empty Glade

| Prop | Category | Source | Why | Modelling |
|---|---|---|---|---|
| Telescope on tripod | `interactable` | `explicit` | Holds the pickaxe and sets up the cabin reveal | Hero prop, two-part mesh |
| Pickaxe | `weapon` | `explicit` | The player's only melee weapon | Hero prop, seen constantly in first person |
| Polaroid photograph of the group | `interactable` | `explicit` | The emotional beat of the scene | Plane with a hand-painted texture |
| Sleeping bags, empty and disarrayed | `set_dressing` | `explicit` | Tells the story without dialogue | Reused from scene 01, re-posed |
| Scattered belongings kit | `set_dressing` | `explicit` | Sells sudden abandonment | Kitbash from existing camp props |
| Bonfire, extinguished | `set_dressing` | `explicit` | Long cold; time has passed | Direct reuse from scene 01 |
| Beer bottle and soda can on table | `set_dressing` | `explicit` | Interrupted, not packed up | Direct reuse |
| Wolf pack, three instances | `environment` | `explicit` | First real fight | Same wolf mesh, instanced |
| Night sky dome with visible stars | `environment` | `explicit` | Set up for the North Star navigation later | Skybox, not geometry |

## Scene 07 — The Road To Vernon'S Cabin

| Prop | Category | Source | Why | Modelling |
|---|---|---|---|---|
| Bear trap, open and sprung | `interactable` | `explicit` | Branching hazard that decides the encounter | Two-state mesh, hinge animation |
| Cultist Zealot | `environment` | `explicit` | Branch A ambush | One base body, material and prop variant |
| Cultist Spotter with lamp | `environment` | `explicit` | Branch B patrol | Same base body, second variant |
| Handheld oil lamp, lit | `light_source` | `explicit` | How the player locates a patrol in the dark | Reused for the mine lamp |
| Knife and scythe | `weapon` | `explicit` | Zealot armament | Two small meshes, held only |
| Roadside altar with candles | `set_dressing` | `explicit` | Plants the religion theme without exposition | Stone kit plus candle instances |
| Cabin exterior with crosses | `environment` | `explicit` | The destination silhouette | Crosses kitbashed from one mesh |
| Blood decals | `set_dressing` | `inferred` | Aftermath of the encounter | Decal set, four variants |

## Scene 08 — Vernon'S Cabin

| Prop | Category | Source | Why | Modelling |
|---|---|---|---|---|
| Vernon's cabin interior | `environment` | `explicit` | The only warm space in the level | Interior build — not in the v0.1 budget |
| Fireplace with live fire | `light_source` | `explicit` | The only warm light source per the art direction | Particle fire plus baked light |
| M1911 pistol | `weapon` | `explicit` | First firearm handed to the player | Hero prop, first-person and held |
| Morphine syrettes in a tin | `interactable` | `explicit` | Vernon's handoff; plants the drug system | Small mesh, tin opens |
| Marijuana, rolled | `interactable` | `explicit` | Holly's handoff | Tiny mesh, held only |
| Orthodox icon on the wall | `set_dressing` | `explicit` | Religion theme, no exposition | Plane with painted texture |
| Wooden crosses, nailed | `set_dressing` | `explicit` | Exterior and interior both | One cross mesh, many instances |
| Vernon's cot and blankets | `set_dressing` | `explicit` | A sick man lives here | Simple mesh, cloth baked |
| Radio set, larger than the handset | `interactable` | `explicit` | Scott's transmission comes through it | Hero prop, period dials |
| Oil lamp, interior | `light_source` | `explicit` | Secondary warm source | Reused from scene 07 |

## Scene 09 — 

| Prop | Category | Source | Why | Modelling |
|---|---|---|---|---|
| Mine entrance and headframe | `environment` | `explicit` | The exterior the GDD budgets | Timber kit, low poly |
| Mine interior tunnel kit | `environment` | `explicit` | Interior route — NOT in the v0.1 budget | Modular tunnel pieces, heavy reuse |
| Mining lamp, handheld | `light_source` | `explicit` | The player's only light in the mine | Reused from scene 07 lamp |
| Infirmary room dressing | `environment` | `explicit` | Where Scott is found | Small room, kitbashed |
| Stretcher, canvas and wood | `interactable` | `explicit` | Drag mechanic — not in the v0.1 budget | Hero prop, deforms under drag |
| Arisaka rifle | `weapon` | `explicit` | Second firearm, found here | Hero prop, first-person |
| Rotted timber supports | `set_dressing` | `explicit` | Claustrophobia and threat | Three variants, instanced |
| Mine cart, derailed | `set_dressing` | `inferred` | Silhouette interest in a dark tunnel | One mesh, two placements |
| Medical supplies, period | `set_dressing` | `inferred` | Sells the infirmary | Small kitbash set |

## Scene 10 — 

| Prop | Category | Source | Why | Modelling |
|---|---|---|---|---|
| Hill of Crosses | `environment` | `explicit` | The final approach silhouette | One cross mesh, kitbashed into a field |
| Virgin Mary statue | `environment` | `explicit` | Landmark on the night route | Single sculpt, low poly |
| Church exterior and entrance | `environment` | `explicit` | The shelter that ends Day 1 | Exterior plus entrance only |
| Circle of fire | `environment` | `explicit` | The ambush set piece | Particle ring plus baked light |
| Night sky with North Star | `environment` | `explicit` | Navigation without the compass | Skybox with a placed hero star |
| Flare, fired | `light_source` | `explicit` | Cultists calling reinforcements | Particle plus dynamic light |
| Furman | `environment` | `explicit` | Highest art risk per the GDD | Meshy plus hand cleanup in Blender |
| Cracked and shifting ground | `environment` | `explicit` | The island transforming | Displacement on terrain, decal cracks |
| Scott on the stretcher, dragged | `interactable` | `explicit` | Carried through the whole sequence | Reuse of the scene 09 stretcher |
| Cultist torches | `light_source` | `inferred` | Reads pursuit at distance in the dark | Reused lamp mesh, fire particle |
