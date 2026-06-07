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
  {"id":"trawl",  "name":"Expand the trawling fleet",
   "brief":"More boats, more catch, more jobs for the town now. But heavy trawling and bycatch pressure the fish stocks and the river-mouth nursery the whole fishery depends on."},
  {"id":"marina", "name":"Marina with a dredged channel",
   "brief":"A marina and dredged channel at the township brings boating money and visitors. The dredging pulls sand out of the system and cuts the longshore drift that feeds the river mouth and the spit."},
  {"id":"oyster", "name":"Oyster lease in the river mouth",
   "brief":"A small aquaculture lease in the estuary: local food and steady jobs. It only works if the river mouth stays clean and healthy, and because the estuary is a significant site the Traditional Owners must be consulted."},
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
  "owners":{"good":"The river mouth was kept clean and undisturbed, and we were consulted before any work. Stepping back where it made sense respects how this Country has always been cared for. This is what good process looks like.",
            "mixed":"Some of the work near the river mouth concerns us, and we were not always brought in early enough. The site is holding for now, but keep us at the table before the next round of decisions.",
            "bad":"Dredging and pollution have reached a site that should have been protected, and the decisions were made without our consent or our knowledge. This is exactly the harm we asked you to avoid, and money cannot undo it."},
  "eco":{"good":"The dune vegetation is holding the sand, the estuary nursery is healthy and the beach is doing its natural job as a sea defence. Wildlife still has somewhere to live. This is a coast working with nature, not against it.",
         "mixed":"It is a mixed picture. Some habitat is hanging on, but a few of your choices are straining the dunes or the river mouth, and the system is less resilient than it was.",
         "bad":"The dunes are breaking down and the estuary is in serious trouble. Hard walls and heavy industry have cut the natural sand supply and stripped the life out of this coast. Recovery here will take decades, if it comes at all."},
  "town":{"good":"The beach is still wide and inviting, the road and the homes are safe, and the coast looks like somewhere people want to come. That is good for business and good for the people who live here.",
          "mixed":"We are safe enough, but the beach has thinned or the coast is turning into a wall of rock and concrete. Visitors notice, and a thin beach is a poorer draw than a wide one.",
          "bad":"We have lost beach, or buildings, or both. The shoreline is either washing away or buried in hard defences, and the visitors who keep this town alive are starting to go elsewhere."},
  "fish":{"good":"There is a living to be made here and the fish stocks are holding up. You left room for the town's economy without wrecking the nursery the catch depends on. That is the balance we need.",
          "mixed":"We are getting by, but the catch is sliding, or there was barely any room left for industry at all. A coast locked up tight is as hard on us as one that has been overfished.",
          "bad":"The fishery has been hammered and there is not enough work to keep families here. A short-term catch or a dead estuary is no future. Short-term thinking has cost us the long-term living."},
}

# Reflection questions. lookFor = keywords for a coverage self-check (not a correctness check).
QUESTIONS = [
  {"n":1, "tie":"Erosion and deposition (4.2 / 4.3)",
   "q":"Explain why Wattle Head (the headland) is worn back hard while Main Beach in the bay builds up. Use the words wave energy, refraction and deposition.",
   "lookFor":["headland","bay","wave energy","refraction","deposition","longshore","drift","sheltered","erosion"],
   "selfcheck":"A strong answer links the headland facing the swell (high wave energy, refraction focusing the waves) to fast erosion, and the sheltered bay (low energy) to deposition and a wider beach."},
  {"n":2, "tie":"Management strategies (4.2)",
   "q":"Pick one measure you placed. Explain why that site needed it, and name one disadvantage of that measure.",
   "lookFor":["sea wall","seawall","groyne","nourish","managed retreat","retreat","beach","downdrift","starve","scour","cost","expensive"],
   "selfcheck":"A strong answer names the measure, the problem at that site (eroding cliff, thin beach, asset at risk), and an honest downside such as cost, scouring, or starving the coast downdrift."},
  {"n":3, "tie":"Cultural value and consultation",
   "q":"The river mouth is a significant site for the Traditional Owners. How did your decisions respect that, and why does consultation matter before any work?",
   "lookFor":["river mouth","estuary","traditional owners","consult","protect","significant","culture","cultural","dredge","marina"],
   "selfcheck":"A strong answer says whether the estuary was protected from dredging and pollution, and explains that the Traditional Owners must be consulted because it is their Country and a significant site."},
  {"n":4, "tie":"Threats and weighing it up (4.5)",
   "q":"Some clifftop houses sit close to an eroding, soft-rock cliff. Using what happened, what advice would you give planners and buyers about building near this coast?",
   "lookFor":["erosion","retreat","setback","soft rock","limestone","cliff","managed retreat","risk","monitor","build","distance"],
   "selfcheck":"A strong answer uses the erosion you saw to argue for setbacks from the cliff edge, caution on soft rock, and planning for a coast that keeps moving."},
]

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
