# Coasts v2 -- Wattle Bay coastal manager (Year 7 Geography). DATA LAYER (edit this).
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
  "title": "Wattle Bay -- coastal manager",
  "subtitle": "Year 7 Geography · Coasts · a living coastline",
  "intro": ("You manage Wattle Bay, a fictional Victorian-style coast. The waves roll in from the open "
            "ocean (the arrows). Where they hit square-on, like the headland, they hammer it; "
            "where the bay shelters them, they drop their sand. Listen to the stakeholders, decide "
            "which housing proposals to approve, place your protection measures where the coast needs them, "
            "then run the decades and watch the coastline change."),
  "driftNote": "Waves drive sand left to right along the shore (longshore drift). The headland and the bay change how hard the waves hit.",
}

# Nodes left -> right. bx,by = base position on a 960x560 map (sea above, land below).
#  soft : rock softness 0..1 (cliff retreat speed)   energy : base exposure 0..1 (modulated by shape)
#  sand : starting beach volume 0..1                 dune : dune+veg 0..1
#  asset: None/"road"/"houses"/"town"                cliff: erodes by retreat (vs sandy)
SEGMENTS = [
  {"id":0, "name":"Wattle Head",        "bx":55, "by":132,"soft":0.05,"energy":0.95,"sand":0.00,"dune":0.0,"asset":None,    "cliff":True, "kind":"headland"},
  {"id":1, "name":"The Shoulder",       "bx":138,"by":190,"soft":0.50,"energy":0.82,"sand":0.03,"dune":0.0,"asset":None,    "cliff":True, "kind":"cliff"},
  {"id":2, "name":"Cliff Road",         "bx":215,"by":238,"soft":0.80,"energy":0.78,"sand":0.05,"dune":0.0,"asset":"road",  "cliff":True, "kind":"cliff"},
  {"id":3, "name":"Clifftop houses",    "bx":300,"by":255,"soft":0.85,"energy":0.75,"sand":0.05,"dune":0.0,"asset":"houses","cliff":True, "kind":"cliff"},
  {"id":4, "name":"The Steps",          "bx":378,"by":228,"soft":0.40,"energy":0.68,"sand":0.02,"dune":0.0,"asset":None,    "cliff":True, "kind":"headland"},
  {"id":5, "name":"Main Beach",         "bx":455,"by":328,"soft":0.20,"energy":0.28,"sand":0.72,"dune":0.3,"asset":None,    "cliff":False,"kind":"beach"},
  {"id":6, "name":"Dune Reserve",       "bx":545,"by":362,"soft":0.20,"energy":0.22,"sand":0.82,"dune":0.7,"asset":None,    "cliff":False,"kind":"dune"},
  {"id":7, "name":"Wattle Bay township","bx":635,"by":338,"soft":0.30,"energy":0.32,"sand":0.52,"dune":0.1,"asset":"town",  "cliff":False,"kind":"town"},
  {"id":8, "name":"River mouth",        "bx":725,"by":294,"soft":0.30,"energy":0.25,"sand":0.34,"dune":0.2,"asset":None,    "cliff":False,"kind":"estuary"},
  {"id":9, "name":"The Spit",           "bx":822,"by":252,"soft":0.20,"energy":0.30,"sand":0.62,"dune":0.4,"asset":None,    "cliff":False,"kind":"spit"},
  {"id":10,"name":"Far Beach",          "bx":910,"by":228,"soft":0.25,"energy":0.58,"sand":0.42,"dune":0.2,"asset":None,    "cliff":False,"kind":"beach"},
]

# Four strategies plus do-nothing. cost = one-off placement budget units.
STRATEGIES = {
  "none":    {"name":"Do nothing",        "letter":"·","cost":0,  "adv":"Lets natural processes run; no cost.","dis":"The coast keeps eroding where the waves are strong."},
  "seawall": {"name":"Sea wall",          "letter":"W","cost":20, "adv":"Protects the base of cliffs, land and buildings; can stop coastal flooding.","dis":"Reflects wave energy so the waves stay powerful, scouring the beach in front and starving the coast downdrift. Expensive. High upkeep."},
  "groyne":  {"name":"Groynes",           "letter":"G","cost":12, "adv":"Traps sand moving by longshore drift, building a beach on the updrift side.","dis":"Starves the beach downdrift. Costly to build and maintain."},
  "nourish": {"name":"Beach nourishment", "letter":"N","cost":8,  "adv":"Rebuilds a natural, protective, tourist-friendly beach.","dis":"The new sand washes away and needs topping up every few years."},
  "retreat": {"name":"Managed retreat",   "letter":"M","cost":10, "adv":"Steps assets back; lets beaches and dunes build; low cost; draws wildlife and visitors.","dis":"People must be compensated for lost buildings or land."},
}

# Three housing proposals. Approving closer-to-coast proposals gives more council budget
# (developers pay a coastal levy) but puts buildings at greater risk from erosion.
# budgetBonus: extra units added to the spending pool if approved.
# Sim effects applied in applyApprovals().
APPLICATIONS = [
  {"id":"clifftop",   "name":"Clifftop Estate",
   "budgetBonus": 22,
   "brief":"20 homes right on the clifftop above the soft limestone -- premium ocean views and strong council rates. The cliff edge is already retreating."},
  {"id":"beachfront", "name":"Beachfront Holiday Park",
   "budgetBonus": 12,
   "brief":"40 holiday units tucked behind Main Beach. The dunes between the buildings and the waves are the only natural buffer."},
  {"id":"township",   "name":"Coastal Heights Subdivision",
   "budgetBonus": 5,
   "brief":"30 homes set back from the shore near the township. Lower views, lower council revenue -- but sheltered from the cliff edge and direct wave action."},
]

# Each voice has: concern (short line above map), view (paragraph), goals (list shown in panel).
VOICES = [
  {"id":"engineer","name":"Coastal engineer","role":"explains what the waves and drift did","colour":"#146c94",
   "focus":[0,1,2,3,4],
   "concern":"Watch where the waves hit hardest -- the headland and the soft cliffs. Thin beaches there mean fast erosion.",
   "view":"I read this coast through wave energy, longshore drift and how fast the cliffs retreat. The headland is hard rock taking the full force of the swell; the soft limestone cliffs next to it move back quickly wherever the beach in front of them thins out. The sheltered bay collects sand by deposition; the spit grows from what longshore drift drops past the river mouth. Every hard structure you place changes the drift, with knock-on effects for everything further along the coast.",
   "goals":["Track wave energy at the headland and cliffs: they face the swell directly","Watch beach width as a buffer that slows cliff retreat","Follow sand moving left-to-right along the shore (longshore drift)","Think about how each measure changes the drift for the coast further along"]},
  {"id":"owners","name":"Traditional Owners","role":"river-mouth significant site, consultation","colour":"#7c3aed",
   "focus":[8],
   "concern":"The river mouth is a significant site. It needs protection and genuine consultation before any work -- not just an engineering decision made without us.",
   "view":"This place has been known and cared for by our community for a very long time. The river mouth is a significant site, and any work near it requires genuine consultation with us from the start -- not a notification after decisions are already made. We are not against the coast being managed; we need to be part of that conversation.",
   "goals":["Protect the river-mouth significant site from disturbance","Be consulted before any work near the estuary begins","Keep the river and estuary clean and healthy for future generations"]},
  {"id":"eco","name":"Marine ecologist","role":"dunes, estuary, beach habitat","colour":"#237a3b",
   "focus":[6,8,9],
   "concern":"The dunes, the estuary and the spit are habitat and natural defence -- not empty space waiting to be developed. Keep them intact.",
   "view":"I look at this coast as a living system. The dune plants hold the sand in place; strip them and the dunes collapse. The estuary is a nursery for young fish and a feeding ground for birds; it depends on clean water and the sand brought in by longshore drift. Hard walls are the fastest way to break this system.",
   "goals":["Protect the dune plants at the Dune Reserve","Keep the river-mouth estuary healthy","Avoid hard walls that cut off natural sand movement and damage habitat","Maintain the spit as shorebird habitat"]},
  {"id":"town","name":"Tourism and residents","role":"the beach, the look of the coast, safe homes","colour":"#b35a1f",
   "focus":[3,5,7],
   "concern":"The beach draws visitors and shields the town, but the houses and the road have to stay safe. Hard walls can save assets and wreck the beach.",
   "view":"The beach is what makes this town. Visitors come for the sand, the water, and the feel of a working coast. Locals need the road and the clifftop houses to stay safe. A sea wall protects what sits behind it, but it scours the beach in front -- and a beach without sand is not what anyone came here for.",
   "goals":["Keep Main Beach wide and attractive for visitors and locals","Protect Cliff Road and the clifftop houses from the eroding cliff","Avoid turning the coast into a wall of concrete that drives visitors away","Maintain the town as somewhere people want to live and visit"]},
]

VOICE_LINES = {
  "owners":{"good":"The river mouth was kept clean and undisturbed, and we were consulted before any work. Stepping back where it made sense respects how this Country has always been cared for. This is what good process looks like.",
            "mixed":"Some of the work near the river mouth concerns us, and we were not always brought in early enough. The site is holding for now, but keep us at the table before the next round of decisions.",
            "bad":"Disturbance has reached a site that should have been protected, and decisions were made without our consent or knowledge. This is exactly the harm we asked you to avoid, and money cannot undo it."},
  "eco":{"good":"The dune plants are holding the sand, the estuary is healthy and the beach is doing its natural job as a defence. Wildlife still has somewhere to live. This is a coast working with nature, not against it.",
         "mixed":"It is a mixed picture. Some habitat is hanging on, but a few choices are putting pressure on the dunes or the estuary, and the system is less resilient than it was.",
         "bad":"The dunes are breaking down and the estuary is in trouble. Hard structures have cut the natural sand supply and stripped the life out of this coast. Recovery will take decades, if it comes at all."},
  "town":{"good":"The beach is still wide and inviting, the road and the homes are safe, and the coast looks like somewhere people want to come. That is good for business and good for the people who live here.",
          "mixed":"We are safe enough, but the beach has thinned or the coast is turning into concrete. Visitors notice, and a thin beach is a poorer draw than a wide one.",
          "bad":"We have lost beach, or buildings, or both. The shoreline is either washing away or buried in hard defences, and the visitors who keep this town alive are starting to go elsewhere."},
}

# Reflection questions. lookFor = keywords for a coverage self-check (not a correctness check).
QUESTIONS = [
  {"n":1, "tie":"Erosion and deposition (4.2 / 4.3)",
   "q":"Explain why Wattle Head (the headland) erodes quickly while Main Beach in the bay builds up. Use the words wave energy and deposition in your answer.",
   "lookFor":["headland","bay","wave energy","deposition","longshore","drift","sheltered","erosion","beach"],
   "selfcheck":"A strong answer links the headland facing the waves (high wave energy) to fast erosion, and the sheltered bay (low energy) to sand being dropped (deposition) and a wider beach."},
  {"n":2, "tie":"Management strategies (4.2)",
   "q":"Pick one measure you placed. Explain why that site needed it, and name one disadvantage of that measure.",
   "lookFor":["sea wall","seawall","groyne","nourish","managed retreat","retreat","beach","downdrift","cost","expensive","sand"],
   "selfcheck":"A strong answer names the measure, explains the problem at that site (eroding cliff, thin beach, asset at risk), and gives an honest downside -- cost, scouring the beach in front, or starving the coast further along."},
  {"n":3, "tie":"Cultural value and consultation",
   "q":"The river mouth is a significant site for the Traditional Owners. How did your decisions respect that, and why does consultation matter before any coastal work?",
   "lookFor":["river mouth","estuary","traditional owners","consult","protect","significant","culture","cultural"],
   "selfcheck":"A strong answer says whether the estuary was protected from disturbance, and explains that the Traditional Owners must be consulted because it is their Country and a significant site -- not just an engineering question."},
  {"n":4, "tie":"Planning and risk (4.5)",
   "q":"One housing proposal put buildings right on the eroding cliff. Using what happened in the simulation, what advice would you give planners about building near this coast?",
   "lookFor":["erosion","retreat","setback","soft rock","cliff","risk","build","safe","distance","wave"],
   "selfcheck":"A strong answer uses what the simulation showed to argue for keeping buildings well back from the cliff edge, and explains why the cliff retreat rate matters to planning decisions."},
]

CONST = {
  "KFLUX":0.13,       # longshore transport coefficient (per boundary)
  "MOVEFRAC":0.9,     # most of a node's drift-driven sand can leave in a year
  "STORM_P":0.20, "STORM_MULT":1.8,
  "CLIFF_K":0.060, "BEACH_BUFFER":0.85, "ASSET_LIMIT":0.55,
  "STORM_LOSS":0.05,
  "NOURISH":0.06, "NOURISH_WEAR":0.5,
  "SUPPLY":0.30,      # fraction of updrift-end capacity entering as new sand
  "FOCUS_LO":0.75, "FOCUS_HI":1.30,  # curvature focusing range (concave bay defocuses, convex head focuses)
  "OFF_SAND":34, "OFF_RET":70,       # render: pixels the shoreline moves per unit sand / retreat
  "BUDGET":55,        # base spending pool; approving coastal housing adds budget (developer levy)
  "APP_LIMIT":2,      # can approve at most 2 of 3 proposals; must reject at least one
}
