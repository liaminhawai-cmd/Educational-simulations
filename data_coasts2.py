# Coasts v2 — Wattle Bay coastal manager (Year 7 Geography). DATA LAYER (edit this).
# 2D coastline: each segment is a NODE with a base position (bx,by) on the map. Sea is up (small y),
# land is down (large y). The coast wiggles: a headland that juts seaward, soft cliffs, a sheltered
# concave bay, a river mouth and a spit. Wave energy and longshore drift at each node are DERIVED from
# how the node faces the incoming swell (orientation), so the shape drives the physics. The shoreline
# then DEFORMS: beaches build seaward, cliffs retreat landward, the spit grows. Same emergent 1D
# sediment budget underneath, now wrapped on honest 2D geometry.
#
# Cultural safety: fictional place, real framework; the river mouth is a protected significant site
# that must be consulted on; no invented sacred story or words for a real community.

# Deep-water swell travels toward the coast from the upper-left (down and to the right).
SWELL = [0.45, 0.89]

META = {
  "title": "Wattle Bay — coastal manager",
  "subtitle": "Year 7 Geography · Coasts · a living coastline",
  "intro": ("You manage Wattle Bay, a fictional Victorian-style coast. The waves roll in from the open "
            "ocean (the arrows). Where they hit the coast square-on, like the headland, they hammer it; "
            "where the bay shelters them, they drop their sand. Listen to the stakeholders, rule "
            "on the development applications, place your measures where the site calls for them, then "
            "run the decades and watch the coastline change."),
  "driftNote": "Waves drive sand left to right along the shore. The headland and the bay change how hard the waves hit.",
}

# Nodes left -> right. bx,by = base position on a 960x560 map (sea above, land below).
#  soft : rock softness 0..1 (cliff retreat speed)   energy : base exposure 0..1 (modulated by shape)
#  sand : starting beach volume 0..1                 dune : dune+veg 0..1
#  asset: None/"road"/"houses"/"town"                cliff: erodes by retreat (vs sandy)
SEGMENTS = [
  {"id":0, "name":"Wattle Head",        "bx":70, "by":150,"soft":0.05,"energy":0.95,"sand":0.00,"dune":0.0,"asset":None,    "cliff":True, "kind":"headland"},
  {"id":1, "name":"The Shoulder",       "bx":150,"by":200,"soft":0.50,"energy":0.85,"sand":0.04,"dune":0.0,"asset":None,    "cliff":True, "kind":"cliff"},
  {"id":2, "name":"Cliff Road",         "bx":240,"by":236,"soft":0.80,"energy":0.80,"sand":0.05,"dune":0.0,"asset":"road",  "cliff":True, "kind":"cliff"},
  {"id":3, "name":"Clifftop houses",    "bx":330,"by":252,"soft":0.85,"energy":0.78,"sand":0.05,"dune":0.0,"asset":"houses","cliff":True, "kind":"cliff"},
  {"id":4, "name":"The Steps",          "bx":410,"by":292,"soft":0.55,"energy":0.52,"sand":0.28,"dune":0.1,"asset":None,    "cliff":True, "kind":"transition"},
  {"id":5, "name":"Main Beach",         "bx":492,"by":338,"soft":0.20,"energy":0.30,"sand":0.72,"dune":0.3,"asset":None,    "cliff":False,"kind":"beach"},
  {"id":6, "name":"Dune Reserve",       "bx":575,"by":356,"soft":0.20,"energy":0.24,"sand":0.82,"dune":0.7,"asset":None,    "cliff":False,"kind":"dune"},
  {"id":7, "name":"Wattle Bay township","bx":660,"by":336,"soft":0.30,"energy":0.33,"sand":0.52,"dune":0.1,"asset":"town",  "cliff":False,"kind":"town"},
  {"id":8, "name":"River mouth",        "bx":742,"by":300,"soft":0.30,"energy":0.26,"sand":0.34,"dune":0.2,"asset":None,    "cliff":False,"kind":"estuary"},
  {"id":9, "name":"The Spit",           "bx":830,"by":258,"soft":0.20,"energy":0.30,"sand":0.62,"dune":0.4,"asset":None,    "cliff":False,"kind":"spit"},
  {"id":10,"name":"Far Beach",          "bx":910,"by":236,"soft":0.25,"energy":0.58,"sand":0.42,"dune":0.2,"asset":None,    "cliff":False,"kind":"beach"},
]

# Four strategies plus do-nothing. cost = one-off placement budget units.
STRATEGIES = {
  "none":    {"name":"Do nothing",        "letter":"·","cost":0,  "adv":"Lets natural processes run; no cost.","dis":"The coast keeps eroding where the waves are strong."},
  "seawall": {"name":"Sea wall",          "letter":"W","cost":22, "adv":"Protects the base of cliffs, land and buildings; can stop coastal flooding.","dis":"Expensive. Reflects wave energy so the waves stay powerful, scouring the beach in front and starving the coast downdrift. High upkeep."},
  "groyne":  {"name":"Groynes",           "letter":"G","cost":14, "adv":"Traps sand moving by longshore drift, building a beach on the updrift side.","dis":"Starves the beach downdrift. Unattractive; costly to build and maintain."},
  "nourish": {"name":"Beach nourishment", "letter":"N","cost":10, "adv":"Rebuilds a natural, protective, tourist-friendly beach.","dis":"The new sand washes away, so it needs topping up every few years."},
  "retreat": {"name":"Managed retreat",   "letter":"M","cost":12, "adv":"Steps assets back; lets beaches and salt marsh build; low cost; draws wildlife and tourists.","dis":"People must be compensated for lost buildings or land."},
}

APPLICATIONS = [
  {"id":"trawl",  "name":"Expand the trawling fleet","econ":"high",
   "brief":"More boats, more catch, more jobs. Heavy trawling and bycatch pressure the fish stocks and the river-mouth nursery."},
  {"id":"marina", "name":"Marina with a dredged channel (township)","econ":"high",
   "brief":"A marina and dredged channel at the township. Boating money, but dredging pulls sand out and cuts the drift feeding the river mouth and spit."},
  {"id":"housing","name":"Clifftop housing estate","econ":"high",
   "brief":"New homes along the soft limestone clifftop. Strong rates, but far more property in the path of an eroding cliff."},
  {"id":"caravan","name":"Caravan park behind the dunes","econ":"med",
   "brief":"A tourist park behind the Dune Reserve. Steady income, but foot traffic flattens the dune vegetation unless the dunes are protected."},
  {"id":"oyster", "name":"Oyster lease in the river mouth","econ":"med",
   "brief":"A small aquaculture lease in the estuary. Local food and jobs, but only if the river mouth stays clean and healthy, and the area is culturally significant."},
]

# Each voice has: concern (short line above map), view (paragraph), goals (list shown in panel).
VOICES = [
  {"id":"engineer","name":"Coastal engineer","role":"explains what the waves and drift did","colour":"#146c94",
   "focus":[0,1,2,3,4],
   "concern":"Watch where the waves hit hardest, the headland and the soft cliffs. Thin beaches there mean fast erosion.",
   "view":"I read this coast through wave energy, sediment budgets and erosion rates. The headland is hard rock taking the full swell; the soft limestone cliffs beside it retreat fast wherever the beach in front of them thins. The bay gathers sand by deposition; the spit grows from what the drift drops past the river mouth. Every hard structure you place changes the drift, with consequences for everything downdrift.",
   "goals":["Track wave energy at the headland and cliffs: they face the swell directly","Monitor beach width as a buffer against cliff retreat","Follow sand moving left-to-right along the shore (longshore drift)","Anticipate how each measure changes the drift for the coast downdrift"]},
  {"id":"owners","name":"Traditional Owners","role":"river-mouth significant site, consultation","colour":"#7c3aed",
   "focus":[8],
   "concern":"The river mouth is a significant site. It needs protection and genuine consultation before any work, not just engineering or development logic.",
   "view":"This place has been known and cared for by our community for a very long time. The river mouth is a significant site, and any work near it requires genuine consultation with us from the start, not a notification after decisions are made. We are not against the coast being managed; we need to be part of that conversation.",
   "goals":["Protect the river-mouth significant site from disturbance or pollution","Be consulted before any work or development near the estuary begins","Keep the river and estuary clean and healthy for future generations"]},
  {"id":"eco","name":"Marine ecologist","role":"dunes, estuary, fish, pollution","colour":"#237a3b",
   "focus":[6,8,9],
   "concern":"The dunes, the estuary and the spit are habitat and natural defence, not empty space. Keep them intact.",
   "view":"I look at this coast as a living system. The dune vegetation holds the sand; strip it and the dunes collapse. The estuary is a fish nursery and bird feeding ground that depends on clean water and sand brought in by the drift. Hard walls and heavy dredging are the fastest ways to break this system.",
   "goals":["Protect the dune vegetation at the Dune Reserve","Keep the river-mouth fish nursery and estuary healthy","Avoid hard walls that block natural sand movement and kill habitat","Maintain the spit as nesting shorebird habitat"]},
  {"id":"town","name":"Tourism & residents","role":"the beach, the look of the coast, safe homes","colour":"#b35a1f",
   "focus":[3,5,7],
   "concern":"The beach draws visitors and shields the town, but the houses and the road have to stay safe too. Hard walls can save assets and wreck the amenity.",
   "view":"The beach is what makes this town. Visitors come for the sand, the water, and the look of a working coast. Locals need the road and the clifftop houses to stay safe. A seawall protects what sits behind it, but it scours the beach, and a beach-less coast is not what anyone came here for.",
   "goals":["Keep Main Beach wide and attractive for visitors and locals","Protect Cliff Road and the clifftop houses from the eroding cliff","Avoid turning the coast into a wall of concrete that drives visitors away","Maintain the town as somewhere people want to live and visit"]},
  {"id":"fish","name":"Fishing co-op","role":"jobs and a living from the sea","colour":"#b42318",
   "focus":[7,8],
   "concern":"There has to be a living here: a working fishery and room for the town's economy, not the whole coast locked up.",
   "view":"The sea is a workplace for the co-op and a lot of local families. We need a healthy estuary as a fish nursery, room to run our boats, and enough jobs to keep the town alive. Locking up the whole coast or wrecking the river mouth with heavy dredging both end the same way for us.",
   "goals":["Keep a working fishery and local jobs on the water","Protect the estuary as a fish nursery for local stocks","Balance economic development with the long-term health of the fishery","Avoid dredging or pollution that collapses the river-mouth nursery"]},
]

VOICE_LINES = {
  "owners":{"good":"The river mouth is healthy and we were consulted. Stepping back where it made sense respects how this place has always worked.",
            "mixed":"Some of the work near the river mouth worries us. Keep us at the table before the next round.",
            "bad":"Dredging and pollution have reached a site that should have been protected. This needed our consent and our knowledge, and it did not happen."},
  "eco":{"good":"The dunes and the estuary are holding and the beach is doing its natural job. Wildlife has somewhere to live.",
         "mixed":"Mixed. Some habitat hangs on, but a few choices are straining the dunes or the river mouth.",
         "bad":"The dunes are breaking down and the estuary is in trouble. Hard walls and heavy industry have stripped the life out of this coast."},
  "town":{"good":"The beach is wide, the town and homes are safe, and the coast still looks like somewhere people want to visit.",
          "mixed":"Safe enough, but the beach has thinned or the coast is turning into a wall. Visitors notice.",
          "bad":"We have lost beach or buildings, or both. The coast is washing away or buried in concrete, and visitors are going elsewhere."},
  "fish":{"good":"There is a living to be made here and the stocks are holding. Good balance.",
          "mixed":"Getting by, but the catch is sliding or there was little room for industry at all.",
          "bad":"The fishery has been hammered and there is not enough work. Short-term catch is not worth a dead coast."},
}

CONST = {
  "KFLUX":0.13,       # longshore transport coefficient (per boundary)
  "MOVEFRAC":0.9,     # most of a node's drift-driven sand can leave in a year
  "STORM_P":0.20, "STORM_MULT":1.8,
  "CLIFF_K":0.060, "BEACH_BUFFER":0.85, "ASSET_LIMIT":0.55,
  "STORM_LOSS":0.05,
  "NOURISH":0.06, "NOURISH_WEAR":0.5,
  "FISH_TRAWL":0.045, "FISH_RECOVER":0.015,
  "SUPPLY":0.30,      # fraction of updrift-end capacity entering as new sand
  "FOCUS_LO":0.75, "FOCUS_HI":1.30,  # curvature focusing range (concave bay defocuses, convex head focuses)
  "OFF_SAND":34, "OFF_RET":70,       # render: pixels the shoreline moves per unit sand / retreat
  "BUDGET":50,        # one-off placement budget; forces prioritisation across the coast
}
