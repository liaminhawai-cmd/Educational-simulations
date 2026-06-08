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
  "intro": ("You look after Wattle Bay, a made-up coast. Waves roll in from the open ocean (the arrows). "
            "Where they hit straight on, like the headland, they wear it away fast. Where the bay shelters "
            "them, they drop their sand and the beach grows. Decide where new houses can go, protect the "
            "coast, then run the years ten at a time and watch what your three advisers think."),
  "driftNote": "Waves push sand left to right along the shore (longshore drift). The headland and the bay change how hard the waves hit.",
  "consultPrompt": "Real consultation happens before any work, not after. Begin consultation with the Traditional Owners now, while there is still a genuine say to be had.",
  "consultDone": "Consultation has begun. You will work with the Traditional Owners, keep hard structures off the river mouth, and keep the estuary healthy.",
}

# Nodes left -> right. bx,by = base position on a 960x560 map (sea above, land below).
#  soft : rock softness 0..1 (cliff retreat speed)   energy : base exposure 0..1 (modulated by shape)
#  sand : starting beach volume 0..1                 dune : dune+veg 0..1
#  asset: None/"road"/"houses"/"town"                cliff: erodes by retreat (vs sandy)
SEGMENTS = [
  {"id":0, "name":"Wattle Head",        "bx":55, "by":132,"soft":0.05,"energy":0.95,"sand":0.00,"dune":0.0,"asset":None,    "cliff":True, "kind":"headland"},
  {"id":1, "name":"The Shoulder",       "bx":138,"by":190,"soft":0.72,"energy":0.82,"sand":0.03,"dune":0.0,"asset":None,    "cliff":True, "kind":"cliff"},
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
  "none":    {"name":"Do nothing",        "letter":"·","cost":0,  "adv":"Lets nature take its course; no cost.","dis":"The coast keeps wearing away where the waves are strong."},
  "seawall": {"name":"Sea wall",          "letter":"W","cost":16, "adv":"Protects the cliff, land and buildings behind it; can stop the sea flooding in.","dis":"Bounces wave energy back, so the waves stay strong and wash the beach in front away. Costs a lot."},
  "groyne":  {"name":"Groynes",           "letter":"G","cost":10, "adv":"Catches sand moving along the shore, building up the beach on one side.","dis":"Starves the beach further along the coast. Costs money to build and keep up."},
  "nourish": {"name":"Beach nourishment", "letter":"N","cost":6,  "adv":"Adds new sand to make a wide, natural, tourist-friendly beach.","dis":"The new sand washes away, so you have to top it up every few years."},
  "retreat": {"name":"Managed retreat",   "letter":"M","cost":8,  "adv":"Moves buildings back and lets the beach and dunes grow; cheap; good for wildlife.","dis":"People have to be paid for the buildings or land they give up."},
}

# Three housing sites the council can approve. The student clicks them on the map.
# Closer to the water = more money (a developer levy adds to your budget) but more risk of
# being lost to erosion. You can approve at most 2 of 3 (APP_LIMIT).
#   node  : which coast node the houses sit on
#   bonus : budget units added if approved
#   risk  : "cliff" (lost if the cliff retreats), "beach" (lost if the beach washes away), "safe"
HOUSING = [
  {"id":"clifftop",   "name":"Clifftop homes",  "node":1, "bonus":22, "risk":"cliff",
   "blurb":"Right on the cliff edge. Best views and the most money, but the soft cliff is wearing back fast."},
  {"id":"beachfront", "name":"Beachfront homes","node":5, "bonus":12, "risk":"beach",
   "blurb":"Just behind the beach. Good money. Safe only while the beach and dunes stay wide."},
  {"id":"setback",    "name":"Set-back homes",  "node":7, "bonus":5,  "risk":"safe",
   "blurb":"Back from the shore near the town. Less money, but well away from the wearing coast."},
]

# Each voice has: concern (short line above map), view (paragraph), goals (list shown in panel).
VOICES = [
  {"id":"engineer","name":"Coastal engineer","role":"explains what the waves and the sand did","colour":"#146c94",
   "focus":[0,1,2,3,4],
   "concern":"Watch where the waves hit hardest -- the headland and the soft cliffs. A thin beach there means the coast wears away fast.",
   "view":"My job is to explain how this coast works, not to take a side. The headland is hard rock taking the full force of the waves; the soft cliffs next to it wear back quickly wherever the beach in front of them gets thin. The sheltered bay collects sand and the beach grows; the spit builds up from sand carried along the shore past the river mouth. Anything hard you build changes how the sand moves, which can help one spot and starve another further along."},
  {"id":"owners","name":"Traditional Owners","person":"Wattle Bay Traditional Owners","avatar":"country","colour":"#7c3aed",
   "focus":[8],
   "concern":"This is our Country. The river mouth is a significant site -- talk with us before any work begins, not after. Tap us, then begin consultation.",
   "view":"This place has been known and cared for by our community for a very long time. The river mouth is a significant site, and any work near it requires genuine consultation with us from the start -- not a notification after decisions are already made. We are not against the coast being managed; we need to be part of that conversation. In real life this is called Free, Prior and Informed Consent: we are spoken with early, given the full picture, and have a real say.",
   "goals":["Be consulted before any work begins, with a genuine say","Protect the river-mouth significant site from disturbance","Keep hard walls and structures away from the estuary","Keep the river and estuary healthy for future generations"]},
  {"id":"eco","name":"Marine ecologist","person":"Dr Hannah Cole","avatar":"eco","colour":"#237a3b",
   "focus":[6,8,9],
   "concern":"The dunes, the estuary and the spit are habitat and natural defence -- not empty space waiting to be developed. Keep them intact.",
   "view":"I look at this coast as a living system. The dune plants hold the sand in place; strip them and the dunes collapse. The estuary is a nursery for young fish and a feeding ground for birds; it depends on clean water and the sand brought in by longshore drift. Hard walls are the fastest way to break this system -- they cut off the natural sand supply and scrape the life out of the shore.",
   "goals":["Protect the dune plants at the Dune Reserve","Keep the river-mouth estuary healthy","Avoid hard walls that cut off natural sand movement","Maintain the spit as shorebird habitat"]},
  {"id":"town","name":"Tourism and residents","person":"Sam Doyle","avatar":"town","colour":"#b35a1f",
   "focus":[3,5,7],
   "concern":"I run the beach cafe. The wide beach is what brings people here, but the road and the houses have to stay safe too. It is a real balancing act.",
   "view":"The beach is what makes this town. Visitors come for the sand, the water, and the feel of a working coast -- that is my livelihood and everyone else's here. Locals also need the road and the clifftop houses to stay safe. A sea wall protects what sits behind it, but it scours the beach in front, and a beach without sand is not what anyone came here for. Save the buildings, yes, but do not bury the coast in concrete.",
   "goals":["Keep Main Beach wide and attractive for visitors and locals","Protect Cliff Road and the clifftop houses from the eroding cliff","Avoid turning the coast into a wall of concrete","Keep the town somewhere people want to live and visit"]},
]

VOICE_LINES = {
  "owners":{"good":"The river mouth was kept healthy, with sand still reaching it and no hard walls forced onto the significant site. Caring for this place this way respects how this Country has always been looked after.",
            "mixed":"The river mouth is holding on, but the natural sand reaching it has thinned. Keep the significant site in mind before the next round of work, and keep hard structures away from it.",
            "bad":"The river mouth, a significant site, has been damaged -- starved of its sand or walled off. This is the harm we asked you to avoid, and it cannot simply be undone."},
  "eco":{"good":"The dune plants are holding the sand, the estuary is healthy and the beach is doing its natural job as a defence. Wildlife still has somewhere to live. This is a coast working with nature, not against it.",
         "mixed":"It is a mixed picture. Some habitat is hanging on, but a few choices are putting pressure on the dunes or the estuary, and the system is less resilient than it was.",
         "bad":"The dunes are breaking down and the estuary is in trouble. Hard structures have cut the natural sand supply and stripped the life out of this coast. Recovery will take decades, if it comes at all."},
  "town":{"good":"The beach is still wide and inviting, the road and the homes are safe, and the coast looks like somewhere people want to come. That is good for business and good for the people who live here.",
          "mixed":"We are safe enough, but the beach has thinned or the coast is turning into concrete. Visitors notice, and a thin beach is a poorer draw than a wide one.",
          "bad":"We have lost beach, or buildings, or both. The shoreline is either washing away or buried in hard defences, and the visitors who keep this town alive are starting to go elsewhere."},
}

# Situational one-liners. A reaction is built from any that apply, then the overall mood line above.
VOICE_DETAIL = {
  "owners":{
    "notConsulted":"And we still were not properly consulted before the work began.",
    "consulted":"Thank you for consulting with us before you started -- that is how it should be done.",
    "wallOnSite":"A hard wall has been put right on the river mouth, our significant site. That should never have happened.",
    "starved":"The sand that keeps the estuary alive has been cut off up the coast, and the river mouth is suffering for it."},
  "eco":{
    "dunesStripped":"The dune plants have been cleared, so the dunes can no longer hold their sand.",
    "estuaryStarved":"The estuary is being starved of the sand that longshore drift should bring it.",
    "hardWalls":"Too much hard concrete -- every wall and groyne breaks the natural movement of sand a little more.",
    "natural":"You have mostly let the coast keep working the way it naturally does, and the habitat shows it."},
  "town":{
    "assetLost":"And we lost a building to the sea -- exactly what we were afraid of.",
    "beachWide":"The beach is wider than ever, and the visitors love it.",
    "beachThin":"The beach in front has worn thin, and a thin beach keeps the crowds away.",
    "tooManyWalls":"The whole front is turning into a wall of concrete, which is not the seaside people come for."},
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
  "STORM_P":0.18, "STORM_MULT":1.7,
  "CLIFF_K":0.048, "BEACH_BUFFER":0.85, "ASSET_LIMIT":0.62,
  "STORM_LOSS":0.05,
  "NOURISH":0.06, "NOURISH_WEAR":0.5,
  "SUPPLY":0.30,      # fraction of updrift-end capacity entering as new sand
  "EXPORT_SCALE":0.35,  # how much sand actually leaves the downdrift end each year (lower = estuary stays fed)
  "DRIFT_FLOOR":0.18,   # minimum along-coast drift where the shore turns away from the swell (keeps sand reaching the estuary)
  "FOCUS_LO":0.75, "FOCUS_HI":1.30,  # curvature focusing range (concave bay defocuses, convex head focuses)
  "OFF_SAND":34, "OFF_RET":70,       # render: pixels the shoreline moves per unit sand / retreat
  "BEACH_LOST":0.12,  # beachfront homes are lost if beach sand drops below this
  "BUDGET":60,        # base spending pool; approving coastal housing adds budget (developer levy)
  "APP_LIMIT":2,      # can approve at most 2 of 3 housing sites
}
