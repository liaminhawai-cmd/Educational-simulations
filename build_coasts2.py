#!/usr/bin/env python3
# Build the v2 offline Coasts sim from data_coasts2.py.  Run: python3 build_coasts2.py
# Out: /mnt/user-data/outputs/Coasts-Interactive.html
import json, os
import data_coasts2 as DC

OUT = "/mnt/user-data/outputs/Coasts-Interactive.html"
DATA = {"META":DC.META,"SWELL":DC.SWELL,"SEG":DC.SEGMENTS,"STRAT":DC.STRATEGIES,
        "APPS":DC.APPLICATIONS,"VOICES":DC.VOICES,"VLINES":DC.VOICE_LINES,
        "Q":DC.QUESTIONS,"C":DC.CONST}
DATA_JSON = json.dumps(DATA, ensure_ascii=False)

CSS = r"""
:root{--ink:#23202b;--muted:#6f6a78;--line:#e3e0e8;--paper:#fff;--bg:#f3f1f5;
--amber:#cf8336;--blue:#3d7fb8;--ok:#3a8a4e;--okb:#e7f1e8;--no:#b1492f;--nob:#f6e3de;--accent:#3a566b;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);line-height:1.55;font-family:"Iowan Old Style",Palatino,Georgia,serif;font-size:15.5px}
.wrap{max-width:1040px;margin:0 auto;padding:0 16px 90px}
header{background:#1d2a33;color:#fff;margin:0 -16px 16px;padding:18px 22px;border-bottom:4px solid var(--amber)}
header h1{margin:0;font-size:23px}
header .sub{font-family:ui-sans-serif,system-ui,sans-serif;font-size:11.5px;color:#a9c2d0;text-transform:uppercase;letter-spacing:.09em;margin-top:4px}
.intro{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:12px 15px;margin-bottom:12px;font-size:14.5px}
.panel{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:14px;margin-bottom:12px}
.lead{font-family:ui-sans-serif,system-ui,sans-serif;color:var(--muted);font-size:13px;margin:0 0 10px}
h2.sec{font-size:18px;margin:0 0 8px}
h2.sec .stepn{display:inline-block;background:var(--accent);color:#fff;font-size:12px;font-weight:700;border-radius:99px;padding:1px 9px;margin-right:8px;vertical-align:middle;font-family:ui-sans-serif,system-ui,sans-serif}
.mapwrap{width:100%;border:1px solid var(--line);border-radius:6px;overflow:hidden;background:#cfe2ec}
svg{display:block;width:100%;height:auto}
.legend{display:flex;flex-wrap:wrap;gap:9px 15px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;color:var(--muted);margin-top:8px}
.legend span{display:inline-flex;align-items:center;gap:5px}.sw{width:13px;height:13px;border-radius:3px;display:inline-block;border:1px solid #0002}
.chooser{margin-top:6px;border:1px dashed var(--accent);border-radius:7px;padding:11px 13px;background:#f7fafb;display:none}.chooser.show{display:block}
.chooser h3{font-family:ui-sans-serif,system-ui,sans-serif;font-size:14px;margin:0 0 6px}
.stratgrid{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.sbtn{cursor:pointer;font-family:ui-sans-serif,system-ui,sans-serif;border:1px solid var(--line);background:#fff;border-radius:16px;padding:6px 11px;font-size:12.5px}
.sbtn.on{background:#fbf1e4;border-color:var(--amber);font-weight:600}.sbtn.locked{opacity:.45;cursor:not-allowed}
.advdis{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;margin-top:4px}.advdis .a{color:var(--ok)}.advdis .d{color:var(--no)}
@keyframes stampDown{
  0%{transform:rotate(-22deg) scale(3.2);opacity:0}
  55%{transform:rotate(5deg) scale(0.92);opacity:1}
  75%{transform:rotate(-2deg) scale(1.05);opacity:1}
  100%{transform:rotate(-5deg) scale(1);opacity:0.9}
}
.app-card{position:relative;background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:14px 16px;margin-bottom:14px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.07)}
.app-title{font-family:ui-sans-serif,system-ui,sans-serif;font-size:15px;font-weight:700;margin:0 0 5px}
.app-brief{font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;color:var(--muted);margin:0 0 10px}
.app-bonus{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;color:var(--ok);font-weight:600;margin-bottom:10px}
.stamp-mark{position:absolute;top:14px;right:14px;transform-origin:top right;pointer-events:none;font-family:ui-sans-serif,system-ui,sans-serif;font-size:19px;font-weight:900;letter-spacing:.13em;padding:4px 13px;border-radius:3px;border:3px solid;animation:stampDown .4s cubic-bezier(.2,.6,.3,1) forwards}
.stamp-mark.approved{color:var(--ok);border-color:var(--ok);background:rgba(58,138,78,.07)}
.stamp-mark.rejected{color:var(--no);border-color:var(--no);background:rgba(177,73,47,.07)}
.toggle{display:inline-flex;border:1px solid var(--line);border-radius:18px;overflow:hidden}
.toggle button{cursor:pointer;border:none;background:#fff;font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;padding:6px 16px;color:var(--muted)}
.toggle button.approve.on{background:var(--okb);color:var(--ok);font-weight:600}.toggle button.reject.on{background:var(--nob);color:var(--no);font-weight:600}.toggle button.locked{opacity:.5;cursor:not-allowed}
button.run{font-family:ui-sans-serif,system-ui,sans-serif;cursor:pointer;border:1px solid var(--accent);background:var(--accent);color:#fff;border-radius:7px;padding:11px 18px;font-size:14.5px;font-weight:600}button.run:disabled{opacity:.4;cursor:not-allowed}
.voice{border-left:3px solid var(--line);padding:8px 12px;margin-bottom:9px;background:#fafafa}
.voice.eng{border-left-color:var(--accent)}.voice.good{border-left-color:var(--ok)}.voice.mixed{border-left-color:var(--amber)}.voice.bad{border-left-color:var(--no)}
.voice .who{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}.voice p{margin:3px 0 0;font-size:14px}
.stamp{font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;font-weight:700;color:var(--accent);margin:4px 0 10px}
.note{font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;color:var(--muted);margin-top:8px}
textarea{width:100%;min-height:64px;font:inherit;font-size:14px;padding:8px;border:1px solid var(--line);border-radius:6px;resize:vertical;margin-top:6px}
.stakebar{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}
.skbtn{cursor:pointer;font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;border:1px solid var(--line);background:#fff;border-radius:16px;padding:6px 11px;color:var(--muted)}
.skbtn.on{font-weight:700}
.concern{font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;color:var(--ink);min-height:18px;margin:0 0 8px}
.btn2{font-family:ui-sans-serif,system-ui,sans-serif;cursor:pointer;border:1px solid var(--accent);background:#fff;color:var(--accent);border-radius:7px;padding:9px 14px;font-size:13.5px;font-weight:600;margin-top:10px}
.stakeview{border-left:3px solid var(--line);padding:10px 13px;background:#fafafa;margin-top:10px;border-radius:0 6px 6px 0}
.stakeview .sv-name{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.03em}
.stakeview p{margin:5px 0 6px;font-size:14px}
.stakeview .gh{font-family:ui-sans-serif,system-ui,sans-serif;font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);margin:2px 0 3px}
.stakeview ul{margin:0;padding-left:18px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:13.5px}
.stakeview li{margin-bottom:2px}
.budget-row{display:flex;align-items:center;gap:10px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;padding:8px 10px;background:#f7fafb;border:1px solid var(--line);border-radius:6px;margin-top:10px}
.budget-bar-wrap{flex:1;height:8px;background:#e3e0e8;border-radius:4px;overflow:hidden}
.budget-bar-fill{height:100%;border-radius:4px;transition:width .25s}
.saq{border:1px solid var(--line);border-radius:7px;padding:12px 14px;margin-bottom:11px;background:#fff}
.saq .tie{font-family:ui-sans-serif,system-ui,sans-serif;font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--accent);margin-bottom:4px}
.saq .q{font-size:15px;margin:0 0 6px}
.saq textarea{margin-top:0}
.saqrow{display:flex;align-items:center;gap:10px;margin-top:7px}
.cbtn{font-family:ui-sans-serif,system-ui,sans-serif;cursor:pointer;background:#eef1f4;border:1px solid var(--line);border-radius:6px;padding:7px 13px;font-size:12.5px;font-weight:600;color:var(--ink)}
.wc{font-family:ui-sans-serif,system-ui,sans-serif;font-size:11.5px;color:var(--muted)}
.sc{font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;margin-top:9px;padding:10px 12px;border-radius:6px;background:#f7fafb;border:1px solid var(--line);display:none}
.sc.show{display:block}.sc.warn{background:#fdeccd}
.sc .miss{color:var(--no);margin-top:3px}.sc .ok{color:var(--ok)}
"""

JS = r"""
const D=__DATA__, C=D.C, SW=norm(D.SWELL), $=id=>document.getElementById(id);
const BEACH_SEGS=[5,6,7,9,10];
const START_BEACH = BEACH_SEGS.reduce((a,i)=>a+D.SEG[i].sand,0)/BEACH_SEGS.length;
function norm(v){const m=Math.hypot(v[0],v[1])||1;return [v[0]/m,v[1]/m];}
function dot(a,b){return a[0]*b[0]+a[1]*b[1];}

/* ===== geometry from base positions (sea is up; seaward normal points to smaller y) ===== */
function geom(){
  const P=D.SEG.map(s=>[s.bx,s.by]), N=P.length, g=[];
  for(let i=0;i<N;i++){
    const a=P[Math.max(0,i-1)], b=P[Math.min(N-1,i+1)];
    let t=norm([b[0]-a[0], b[1]-a[1]]);
    let n=[-t[1],t[0]]; if(n[1]>0) n=[-n[0],-n[1]];     // seaward = up (y<0)
    const inward=[-n[0],-n[1]];
    const facing=Math.max(0, dot(SW, inward));           // faces the incoming swell?
    // curvature: node more seaward than neighbours -> convex headland -> focus; set back -> bay -> defocus
    const avgBy=(a[1]+b[1])/2, d=avgBy-P[i][1];
    const focus=clamp(C.FOCUS_LO + (d+40)/80*(C.FOCUS_HI-C.FOCUS_LO), C.FOCUS_LO, C.FOCUS_HI);
    g.push({t,n,inward,facing,focus});
  }
  return g;
}
function energyOf(st,i,emult){
  const s=st.seg[i], gg=st.g[i];
  let e=s.energyBase*(0.55+0.45*gg.facing)*gg.focus*emult;
  if(st.meas[i]==="armour") e*=0.55;
  return e;
}

/* ===== app helpers ===== */
function appDec(st,id){return st.apps[id];}
function appLvl(st,id){return st.apps[id]==="approve"?1:0;}

/* ===== pure sim ===== */
function clamp(v,a,b){return v<a?a:v>b?b:v;}
function initState(){
  return {seg:D.SEG.map(s=>({...s,energyBase:s.energy,sand:s.sand,dune:s.dune,retreat:0,lost:false})),
          g:geom(), meas:D.SEG.map(()=> "none"),
          apps:{clifftop:null,beachfront:null,township:null}, stake:null,
          spend:0, year:0};
}
function applyApprovals(st){
  // clifftop estate: new houses on The Shoulder above the eroding cliff
  if(appDec(st,'clifftop')==='approve') st.seg[1].asset='houses';
  // beachfront park: development damages the dune vegetation at Dune Reserve
  if(appDec(st,'beachfront')==='approve') st.seg[6].dune=Math.max(0,st.seg[6].dune-0.30);
}
function stepYear(st, stormR){
  const N=st.seg.length, s=st.seg, m=st.meas, P=s.map(x=>[x.bx,x.by]);
  const storm=stormR<C.STORM_P, emult=storm?C.STORM_MULT:1;
  const E=[]; for(let i=0;i<N;i++) E[i]=energyOf(st,i,emult);
  for(let i=0;i<N;i++) if(m[i]==="seawall"){const nb=i+1; if(nb<N) E[nb]+=0.18*emult;}
  // longshore flux across each boundary i..i+1 (signed; sign from coast orientation vs swell)
  const move=s.map(()=>0);
  for(let i=0;i<N-1;i++){
    const dir=norm([P[i+1][0]-P[i][0], P[i+1][1]-P[i][1]]);
    const along=dot(SW,dir), Eb=(E[i]+E[i+1])/2;
    let Q=C.KFLUX*Eb*along;
    if(Q>0 && m[i]==="groyne") Q*=0.2;            // traps updrift, starves downdrift
    if(Q<0 && m[i+1]==="groyne") Q*=0.2;
    if(Q>0){const amt=Math.min(Q, s[i].sand*C.MOVEFRAC); move[i]-=amt; move[i+1]+=amt;}
    else   {const amt=Math.min(-Q, s[i+1].sand*C.MOVEFRAC); move[i+1]-=amt; move[i]+=amt;}
  }
  // ends: new sand in at updrift end, loss out at downdrift end
  move[0]+=C.KFLUX*E[0]*C.SUPPLY;
  move[N-1]-=Math.min(C.KFLUX*E[N-1]*Math.max(dot(SW,norm([P[N-1][0]-P[N-2][0],P[N-1][1]-P[N-2][1]])),0), s[N-1].sand*C.MOVEFRAC);
  // apply + extras
  for(let i=0;i<N;i++){
    s[i].sand+=move[i];
    if(m[i]==="nourish") s[i].sand+=C.NOURISH-C.NOURISH*C.NOURISH_WEAR;
    if(storm && !s[i].cliff && E[i]>0.4) s[i].sand-=C.STORM_LOSS;
    if(m[i]==="seawall") s[i].sand=Math.min(s[i].sand,0.05);    // reflected energy scours the beach
    const cap=s[i].kind==="spit"?1.25:1.0;
    s[i].sand=clamp(s[i].sand,0,cap);
  }
  // cliff retreat
  for(let i=0;i<N;i++){ if(s[i].cliff && s[i].soft>0.1){
    const excess=Math.max(0, E[i]*(1-C.BEACH_BUFFER*Math.min(s[i].sand,1)));
    let add=C.CLIFF_K*excess*s[i].soft;
    if(m[i]==="seawall") add=0; if(m[i]==="armour") add*=0.35;
    s[i].retreat+=add;
    if(s[i].asset && !s[i].lost && m[i]!=="retreat" && s[i].retreat>=C.ASSET_LIMIT) s[i].lost=true;
  }}
  st.year++;
}
function run(st,years,rng){ for(let y=0;y<years;y++) stepYear(st,rng()); }
function outcome(st){
  const s=st.seg;
  const beach=BEACH_SEGS.reduce((a,i)=>a+s[i].sand,0)/BEACH_SEGS.length;
  const dunes=(s[5].dune+s[6].dune)/2, assetsLost=s.filter(x=>x.lost).length;
  const estuary=clamp((s[8].sand/0.34)*0.55+(s[9].sand/0.62)*0.45,0,1);
  const walled=st.meas.filter(x=>x==="seawall"||x==="groyne").length;
  return {beach,dunes,assetsLost,estuary,walled,startBeach:START_BEACH};
}
function voiceStates(st,o){return{
  owners:(o.estuary>=0.28)?"good":(o.estuary<0.15)?"bad":"mixed",
  eco:(o.dunes>=0.45&&o.estuary>=0.28)?"good":(o.dunes<0.25||o.estuary<0.15)?"bad":"mixed",
  town:(o.beach>=0.8*o.startBeach&&o.assetsLost===0&&o.walled<=2)?"good":(o.beach<0.5*o.startBeach||o.assetsLost>0)?"bad":"mixed",
};}
function engineerText(st,o){
  const s=st.seg, b=[];
  const dB=o.beach-o.startBeach;
  b.push(dB>0.06?"The sheltered bay has built out, beaches widening.":dB<-0.06?"The beaches have thinned overall.":"The beaches have roughly held.");
  const lost=s.filter(x=>x.lost).map(x=>x.asset);
  if(lost.length) b.push("The "+lost.join(" and the ")+" "+(lost.length>1?"have":"has")+" gone over the eroding cliff.");
  if(st.meas.includes("seawall")) b.push("Where sea walls were built the cliff is held, but the beach in front has been scoured down.");
  if((st.meas.includes("groyne")||st.meas.includes("seawall")) && s[10].sand<0.30)
    b.push("Starved of sand by the structures updrift, Far Beach has worn away.");
  if(st.meas.includes("nourish")) b.push("The nourished beaches are wider, though that sand keeps washing away and needs topping up.");
  if(st.meas.includes("retreat")) b.push("Where assets were stepped back, the shore was left to find its own line.");
  if(s[9].sand>0.85) b.push("The spit has grown as longshore drift drops its load past the river mouth.");
  return b.join(" ");
}
const Sim={initState,stepYear,run,outcome,voiceStates,engineerText,applyApprovals,geom,energyOf,START_BEACH,appDec,appLvl};
if(typeof window!=="undefined"){ window.Sim=Sim; window._drawSVG=drawSVG; }

/* ===== MAP (pure: state -> SVG) ===== */
const MW=960, MH=560;
function coastPts(st){           // current shoreline point per node (deformed along seaward normal)
  return st.seg.map((s,i)=>{
    const off=(s.sand-D.SEG[i].sand)*C.OFF_SAND - s.retreat*C.OFF_RET;
    return [s.bx+st.g[i].n[0]*off, s.by+st.g[i].n[1]*off];
  });
}
function coastYat(pts,x){
  for(let i=0;i<pts.length-1;i++){ if(x>=pts[i][0]&&x<=pts[i+1][0]){
    const t=(x-pts[i][0])/((pts[i+1][0]-pts[i][0])||1); return pts[i][1]+t*(pts[i+1][1]-pts[i][1]); }}
  return x<pts[0][0]?pts[0][1]:pts[pts.length-1][1];
}
function nearest(st,pt){let bi=0,bd=1e9; st.seg.forEach((s,i)=>{const d=Math.hypot(s.bx-pt[0],s.by-pt[1]); if(d<bd){bd=d;bi=i;}}); return {i:bi,d:bd};}
function fx(n){return (+n).toFixed(1);}
function house(cx,gy,w,h,wall,opa){   // little house: body + pitched roof, base at gy, grows upward
  const x=cx-w/2;
  return `<rect x="${fx(x)}" y="${fx(gy-h)}" width="${fx(w)}" height="${fx(h)}" fill="${wall}" opacity="${opa}"/>`+
         `<path d="M${fx(x-2)} ${fx(gy-h)} L${fx(cx)} ${fx(gy-h-w*0.55)} L${fx(x+w+2)} ${fx(gy-h)} Z" fill="#6e3522" opacity="${opa}"/>`+
         `<rect x="${fx(cx-1.6)}" y="${fx(gy-h*0.62)}" width="3.2" height="${fx(h*0.5)}" fill="#5a4636" opacity="${opa}"/>`;
}
function alabel(cx,y,txt,col){return `<text x="${fx(cx)}" y="${fx(y)}" font-size="10.5" text-anchor="middle" font-weight="600" fill="${col||'#3a3226'}">${txt}</text>`;}
function drawSVG(st, sel, stake){
  const pts=coastPts(st), N=st.seg.length;
  let o=`<svg viewBox="0 0 ${MW} ${MH}" xmlns="http://www.w3.org/2000/svg" font-family="ui-sans-serif,system-ui,sans-serif">`;
  o+=`<rect x="0" y="0" width="${MW}" height="${MH}" fill="#bcd9e6"/>`;            // sea
  // wave-vector field (refraction: deep swell bends toward facing the shore near the coast)
  for(let gx=24;gx<MW;gx+=52){ for(let gy=24;gy<MH;gy+=46){
    const cy=coastYat(pts,gx); if(gy>cy-14) continue;                              // only in the sea
    const nr=nearest(st,[gx,gy]); const t=clamp(1-nr.d/200,0,1);
    const inw=st.g[nr.i].inward; let v=norm([SW[0]*(1-t)+inw[0]*t, SW[1]*(1-t)+inw[1]*t]);
    const en=clamp(st.seg[nr.i].energyBase*(0.55+0.45*st.g[nr.i].facing)*st.g[nr.i].focus,0,1.1);
    const L=7+en*9, op=(0.25+en*0.5).toFixed(2);
    const ex=gx+v[0]*L, ey=gy+v[1]*L;
    o+=`<g stroke="#2f6f93" stroke-width="1.4" opacity="${op}"><line x1="${gx}" y1="${gy}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}"/>`+
       `<path d="M${ex.toFixed(1)} ${ey.toFixed(1)} l${(-v[0]*4-v[1]*3).toFixed(1)} ${(-v[1]*4+v[0]*3).toFixed(1)} m0 0 l${(-v[0]*4+v[1]*3).toFixed(1)} ${(-v[1]*4-v[0]*3).toFixed(1)}"/></g>`;
  }}
  // land polygon (top edge = coastline)
  let land=`M 0 ${pts[0][1].toFixed(1)} `;
  pts.forEach(p=>land+=`L ${p[0].toFixed(1)} ${p[1].toFixed(1)} `);
  land+=`L ${MW} ${pts[N-1][1].toFixed(1)} L ${MW} ${MH} L 0 ${MH} Z`;
  o+=`<path d="${land}" fill="#d7cfb8"/>`;
  // grassy band just inland for a bit of texture
  let grass=`M 0 ${(pts[0][1]+24).toFixed(1)} `;
  pts.forEach(p=>grass+=`L ${p[0].toFixed(1)} ${(p[1]+24).toFixed(1)} `);
  grass+=`L ${MW} ${(pts[N-1][1]+24).toFixed(1)} L ${MW} ${MH} L 0 ${MH} Z`;
  o+=`<path d="${grass}" fill="#cdc9ac" opacity="0.55"/>`;
  // beach band (sand) seaward of the coastline
  let beachOuter=[];
  for(let i=0;i<N;i++){const bp=3+st.seg[i].sand*38; beachOuter.push([pts[i][0]+st.g[i].n[0]*bp, pts[i][1]+st.g[i].n[1]*bp]);}
  let bp=`M ${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)} `;
  for(let i=1;i<N;i++) bp+=`L ${pts[i][0].toFixed(1)} ${pts[i][1].toFixed(1)} `;
  for(let i=N-1;i>=0;i--) bp+=`L ${beachOuter[i][0].toFixed(1)} ${beachOuter[i][1].toFixed(1)} `;
  o+=`<path d="${bp} Z" fill="#e9d8a6"/>`;
  // dunes (green) just landward at dune-bearing nodes
  for(let i=0;i<N;i++){ if(st.seg[i].dune>0.25){const x=pts[i][0], y=pts[i][1];
    o+=`<circle cx="${x.toFixed(1)}" cy="${(y+16).toFixed(1)}" r="${(7+st.seg[i].dune*9).toFixed(1)}" fill="#7a9b5e" opacity="0.9"/>`;}}
  // river mouth channel
  const ex8=pts[8][0];
  o+=`<path d="M ${(ex8-16)} ${pts[8][1].toFixed(1)} q 18 60 6 120 l 22 0 q 10 -60 4 -120 z" fill="#3d7fb8"/>`;
  // ===== assets (drawn landward) with clearer art + labels =====
  st.seg.forEach((s,i)=>{ if(!s.asset) return;
    const cx=pts[i][0], gy=pts[i][1]+42, lost=s.lost, opa=lost?0.4:1;
    if(s.asset==="road"){
      const tg=st.g[i].t, hw=44, ly=pts[i][1]+20;
      const ax=cx-tg[0]*hw, ay=ly-tg[1]*hw, bxr=cx+tg[0]*hw, byr=ly+tg[1]*hw;
      o+=`<line x1="${fx(ax)}" y1="${fx(ay)}" x2="${fx(bxr)}" y2="${fx(byr)}" stroke="${lost?'#b3a99a':'#6b6258'}" stroke-width="9" stroke-linecap="round" opacity="${opa}"/>`;
      o+=`<line x1="${fx(ax)}" y1="${fx(ay)}" x2="${fx(bxr)}" y2="${fx(byr)}" stroke="#f2e9d0" stroke-width="1.4" stroke-dasharray="6 6" opacity="${opa}"/>`;
      o+=alabel(cx, gy, lost?"Cliff Road (lost)":"Cliff Road", lost?'#b1492f':'#3a3226');
      if(lost) o+=`<text x="${fx(cx)}" y="${fx(pts[i][1]+4)}" font-size="14" text-anchor="middle" fill="#b1492f">&#10005;</text>`;
    }
    if(s.asset==="houses"){
      for(let k=-1;k<2;k++) o+=house(cx+k*21, gy, 16, 13, lost?'#c9b7a8':'#c46a4a', opa);
      o+=alabel(cx, gy+12, lost?"Clifftop houses (lost)":"Clifftop houses", lost?'#b1492f':'#3a3226');
      if(lost) o+=`<text x="${fx(cx)}" y="${fx(gy-26)}" font-size="15" text-anchor="middle" fill="#b1492f">&#10005;</text>`;
    }
    if(s.asset==="town"){
      // jetty out into the sea, with a moored boat
      const n=st.g[i].n, jx=pts[i][0], jy=pts[i][1];
      const exj=jx+n[0]*48, eyj=jy+n[1]*48;
      o+=`<line x1="${fx(jx)}" y1="${fx(jy)}" x2="${fx(exj)}" y2="${fx(eyj)}" stroke="#8a6d4b" stroke-width="4"/>`;
      for(let p=1;p<=3;p++){const px=jx+n[0]*12*p, py=jy+n[1]*12*p;
        o+=`<line x1="${fx(px-3)}" y1="${fx(py)}" x2="${fx(px+3)}" y2="${fx(py)}" stroke="#6f5538" stroke-width="2"/>`;}
      o+=`<ellipse cx="${fx(exj)}" cy="${fx(eyj-2)}" rx="9" ry="3.6" fill="#33414b"/>`;
      o+=`<line x1="${fx(exj)}" y1="${fx(eyj-2)}" x2="${fx(exj)}" y2="${fx(eyj-15)}" stroke="#33414b" stroke-width="1.4"/>`;
      o+=`<path d="M${fx(exj)} ${fx(eyj-14)} L${fx(exj+8)} ${fx(eyj-6)} L${fx(exj)} ${fx(eyj-5)} Z" fill="#e7e2d6"/>`;
      // township cluster: varied buildings, a hall with a steeple, lit windows
      const hh=[15,22,13,18,14,20], wl=['#7d7787','#9a6440','#646f78','#86745c','#74707c','#8a5a3c'];
      for(let k=0;k<6;k++){ const bxk=cx+(k-2.5)*16, h=hh[k];
        o+=`<rect x="${fx(bxk-6)}" y="${fx(gy-h)}" width="12" height="${fx(h)}" fill="${wl[k]}"/>`;
        o+=`<path d="M${fx(bxk-7)} ${fx(gy-h)} L${fx(bxk)} ${fx(gy-h-6)} L${fx(bxk+7)} ${fx(gy-h)} Z" fill="#46414c"/>`;
        o+=`<rect x="${fx(bxk-3.2)}" y="${fx(gy-h+3)}" width="2.4" height="2.4" fill="#ffe7a8"/><rect x="${fx(bxk+0.8)}" y="${fx(gy-h+3)}" width="2.4" height="2.4" fill="#ffe7a8"/>`;
      }
      // town hall steeple in the middle
      o+=`<line x1="${fx(cx-0.5)}" y1="${fx(gy-22)}" x2="${fx(cx-0.5)}" y2="${fx(gy-34)}" stroke="#46414c" stroke-width="2"/>`;
      o+=`<rect x="${fx(cx-3)}" y="${fx(gy-39)}" width="5" height="5" fill="#cf8336"/>`;
      o+=alabel(cx, gy+12, "Wattle Bay township", '#3a3226');
    }
  });
  // small dock at The Steps headland (node 4 -- the secondary headland poking into the bay)
  {const dk=pts[4], dn=st.g[4].n;
    const dex=dk[0]+dn[0]*38, dey=dk[1]+dn[1]*38;
    o+=`<line x1="${fx(dk[0])}" y1="${fx(dk[1])}" x2="${fx(dex)}" y2="${fx(dey)}" stroke="#7a6448" stroke-width="4" stroke-linecap="round"/>`;
    for(let p=1;p<=3;p++){const px=dk[0]+dn[0]*12*p, py=dk[1]+dn[1]*12*p;
      o+=`<line x1="${fx(px-3)}" y1="${fx(py)}" x2="${fx(px+3)}" y2="${fx(py)}" stroke="#5e4d38" stroke-width="2.5"/>`;}
    o+=`<ellipse cx="${fx(dex)}" cy="${fx(dey)}" rx="8" ry="3" fill="#2d3a42" opacity="0.9"/>`;
    o+=`<line x1="${fx(dex)}" y1="${fx(dey-3)}" x2="${fx(dex)}" y2="${fx(dey-14)}" stroke="#2d3a42" stroke-width="1.2"/>`;
    o+=`<path d="M${fx(dex)} ${fx(dey-13)} L${fx(dex+8)} ${fx(dey-7)} L${fx(dex)} ${fx(dey-6)} Z" fill="#e0dbd0"/>`;
    o+=alabel(dk[0]+6, dk[1]+48, "Steps dock", '#3a566b');}
  // measure badges + click hotspots + node labels
  st.seg.forEach((s,i)=>{const x=pts[i][0], y=pts[i][1];
    if(st.meas[i]!=="none"){o+=`<circle cx="${x.toFixed(1)}" cy="${(y-16).toFixed(1)}" r="11" fill="#cf8336" stroke="#fff" stroke-width="2"/>`+
       `<text x="${x.toFixed(1)}" y="${(y-12).toFixed(1)}" font-size="12" text-anchor="middle" fill="#fff" font-weight="700">${D.STRAT[st.meas[i]].letter}</text>`;}
    if(sel===i) o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="17" fill="none" stroke="#cf8336" stroke-width="2.5"/>`;
    o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="18" fill="#000" opacity="0" style="cursor:pointer" onclick="selectSeg(${i})"/>`;
    o+=`<text x="${x.toFixed(1)}" y="${(y+ (s.cliff?-30:-26)).toFixed(1)}" font-size="9.5" text-anchor="middle" fill="#3a566b">${i}</text>`;
  });
  // stakeholder focus highlight
  if(stake){const v=D.VOICES.find(x=>x.id===stake);
    if(v&&v.focus) v.focus.forEach(i=>{const x=pts[i][0],y=pts[i][1];
      o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="21" fill="${v.colour}" opacity="0.14"/>`+
         `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="21" fill="none" stroke="${v.colour}" stroke-width="2.5" opacity="0.9"/>`;});}
  // north + scale
  o+=`<g stroke="#1d2a33" stroke-width="1.5" fill="#1d2a33"><line x1="${MW-30}" y1="42" x2="${MW-30}" y2="18"/><path d="M${MW-30} 18 l-4 7 l4 -2 l4 2 z"/><text x="${MW-34}" y="56" font-size="10">N</text></g>`;
  o+=`<rect x="24" y="${MH-26}" width="72" height="5" fill="#1d2a33"/><text x="24" y="${MH-30}" font-size="10" fill="#1d2a33">0&#160;&#160;&#160;&#160;1 km</text>`;
  return o+`</svg>`;
}

/* ===== UI ===== */
let st, phase=1, sel=null;
function redraw(){ $("map").innerHTML=drawSVG(st, sel, st.stake); }

function availBudget(){
  // base budget + developer levy from approved coastal housing
  return C.BUDGET + D.APPS.reduce((a,app)=>{
    return a + (appDec(st,app.id)==="approve" ? (app.budgetBonus||0) : 0);
  }, 0);
}
function computeSpend(meas){
  return (meas||st.meas).reduce((a,k)=>a+((D.STRAT[k]&&D.STRAT[k].cost)||0),0);
}
function renderBudget(){
  const avail=availBudget(), spent=computeSpend(), rem=avail-spent;
  const pct=Math.min(Math.round(spent/avail*100),100);
  const col=pct>=90?"#b1492f":pct>=65?"#cf8336":"#3a8a4e";
  $("budgetRow").innerHTML=`<span><strong>Budget:</strong> ${rem} of ${avail} remaining</span><div class="budget-bar-wrap"><div class="budget-bar-fill" style="width:${pct}%;background:${col}"></div></div>`;
}

function renderStake(){
  $("stakeBar").innerHTML=D.VOICES.map(v=>`<button class="skbtn${st.stake===v.id?' on':''}" style="${st.stake===v.id?`border-color:${v.colour};color:${v.colour}`:''}" onclick="setStake('${v.id}')">${v.name}</button>`).join("");
  const v=D.VOICES.find(x=>x.id===st.stake);
  $("stakeConcern").innerHTML = v? `<span style="color:${v.colour}">&#9679;</span> ${v.concern}` : "";
  const sp=$("stakePanel");
  if(!v){ sp.innerHTML=`<p class="lead" style="margin:10px 0 0">Pick a stakeholder above to see the coast through their eyes, and what they want from your plan.</p>`; return; }
  const goalItems=v.goals.map(g=>`<li>${g}</li>`).join("");
  sp.innerHTML=`<div class="stakeview" style="border-left-color:${v.colour}"><div class="sv-name" style="color:${v.colour}">${v.name}: ${v.role}</div><p>${v.view}</p><div class="gh">What they want</div><ul>${goalItems}</ul></div>`;
}
function setStake(id){ st.stake = st.stake===id? null : id; renderStake(); redraw(); }

function downloadReport(){
  const o=Sim.outcome(st), vs=Sim.voiceStates(st,o);
  const spent=computeSpend();
  const dec=D.APPS.map(a=>`  ${a.name}: ${st.apps[a.id]||"undecided"}`).join("\n");
  const mez=st.seg.map((s,i)=>st.meas[i]!=="none"?`  ${i} ${s.name}: ${D.STRAT[st.meas[i]].name}`:null).filter(Boolean).join("\n")||"  (none)";
  const vlines=D.VOICES.filter(v=>v.id!=="engineer").map(v=>`  ${v.name}: ${D.VLINES[v.id][vs[v.id]]}`).join("\n");
  const txt=`WATTLE BAY COASTAL PLAN, year ${st.year}\n\nBUDGET: ${spent} of ${availBudget()} spent\n\nHOUSING DECISIONS\n${dec}\n\nMANAGEMENT MEASURES\n${mez}\n\nWHAT HAPPENED\n  Coastal engineer: ${Sim.engineerText(st,o)}\n${vlines}\n`;
  const b=new Blob([txt],{type:"text/plain"}); const u=URL.createObjectURL(b);
  const a=document.createElement("a"); a.href=u; a.download="wattle-bay-plan.txt"; a.click(); URL.revokeObjectURL(u);
}
function selectSeg(i){ sel=i; renderChooser(); redraw(); }
function energyWord(e){return e>0.7?"high":e>0.4?"moderate":"low";}
function renderChooser(){
  const ch=$("chooser"); if(sel===null){ch.classList.remove("show");return;}
  const s=st.seg[sel]; ch.classList.add("show");
  const eff=energyWord(s.energyBase*(0.55+0.45*st.g[sel].facing)*st.g[sel].focus);
  const built=(phase===2 && ["seawall","groyne"].includes(st.meas[sel]));
  const opts=Object.keys(D.STRAT).map(k=>{
    const on=st.meas[sel]===k?" on":"";
    const lock=built&&k!==st.meas[sel]?" locked":"";
    const cost=D.STRAT[k].cost>0?` (${D.STRAT[k].cost})`:"";
    return `<button class="sbtn${on}${lock}" onclick="${built&&k!==st.meas[sel]?'':`setMeasure('${k}')`}">${D.STRAT[k].name}${cost}</button>`;
  }).join("");
  const cur=D.STRAT[st.meas[sel]];
  ch.innerHTML=`<h3>${sel} &middot; ${s.name}</h3>
    <div class="lead" style="margin:0 0 4px">${s.cliff?"Cliff":"Sandy coast"} &middot; wave energy ${eff} &middot; ${s.soft>0.5?"soft rock (erodes fast)":s.soft<0.2?"hard rock":"medium rock"}${s.asset?` &middot; protects the ${s.asset}`:""}</div>
    <div class="stratgrid">${opts}</div>
    <div class="advdis"><span class="a">+ ${cur.adv}</span><br><span class="d">&minus; ${cur.dis}</span></div>
    <div id="budgetMsg" style="color:var(--no);font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;min-height:16px;margin-top:3px"></div>
    ${built?'<div class="note">A hard structure is built here and cannot be removed cheaply.</div>':''}`;
}
function setMeasure(k){
  const test=[...st.meas]; test[sel]=k;
  if(computeSpend(test)>availBudget()){ const msg=$("budgetMsg"); if(msg) msg.textContent="Over budget. Remove or swap a measure first."; return; }
  st.meas[sel]=k; st.spend=computeSpend();
  renderChooser(); redraw(); renderBudget();
}

function renderApps(){
  const lim=C.APP_LIMIT||2;
  const nAp=D.APPS.filter(a=>appDec(st,a.id)==="approve").length, atLim=nAp>=lim;
  const rem=lim-nAp;
  let out=`<p class="note" style="margin:0 0 14px">Approve at most <strong>${lim} of ${D.APPS.length}</strong> proposals. Approving closer-to-coast housing gives the council more money to spend on protection (developer levy) -- but puts those buildings at greater risk. You must reject at least one. ${atLim?"Limit reached.":rem+" approval"+(rem===1?"":"s")+" remaining."}</p>`;
  D.APPS.forEach(a=>{
    const dec=appDec(st,a.id);
    const locked=phase===2, appBlk=dec!=="approve"&&atLim;
    out+=`<div class="app-card" id="acard-${a.id}">`;
    out+=`<div class="app-title">${a.name}</div>`;
    out+=`<p class="app-brief">${a.brief}</p>`;
    out+=`<div class="app-bonus">If approved: +${a.budgetBonus} budget (developer coastal levy)</div>`;
    if(!locked){
      const aOnclick=appBlk?'':`setApp('${a.id}','approve')`;
      const rOnclick=`setApp('${a.id}','reject')`;
      out+=`<div class="toggle">`;
      out+=`<button class="approve${dec==="approve"?" on":""}${appBlk?" locked":""}" onclick="${aOnclick}">Approve</button>`;
      out+=`<button class="reject${dec==="reject"?" on":""}" onclick="${rOnclick}">Reject</button>`;
      out+=`</div>`;
    } else {
      out+=`<div class="note" style="margin:0">Decision locked: <strong>${dec||"none"}</strong></div>`;
    }
    if(dec){
      const cls=dec==="approve"?"approved":"rejected";
      const txt=dec==="approve"?"APPROVED":"REJECTED";
      out+=`<div class="stamp-mark ${cls}">${txt}</div>`;
    }
    out+=`</div>`;
  });
  $("apps").innerHTML=out;
}

function setApp(id,val){
  if(phase===2)return;
  st.apps[id]=val;
  renderApps();
  renderBudget();
}

function mkRng(seed){let s=seed>>>0;return ()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function doRun(years,label){
  if(phase===1) Sim.applyApprovals(st);
  Sim.run(st,years,mkRng(4242+st.year));
  const o=Sim.outcome(st), vs=Sim.voiceStates(st,o);
  let h=`<div class="stamp">${label} (year ${st.year})</div>`;
  h+=`<div class="voice eng"><div class="who">Coastal engineer</div><p>${Sim.engineerText(st,o)}</p></div>`;
  D.VOICES.filter(v=>v.id!=="engineer").forEach(v=>{const stt=vs[v.id];
    if(!stt) return;
    h+=`<div class="voice ${stt}"><div class="who">${v.name}</div><p>${D.VLINES[v.id][stt]}</p></div>`;});
  $("review").innerHTML=h; redraw(); renderChooser(); renderApps();
}
function runPhase1(){
  if(Object.values(st.apps).some(v=>!v)){ $("phaseNote").textContent="Rule on every proposal first (approve or reject each one), then run."; return; }
  doRun(10,"After the first decade"); phase=2; $("p1btn").style.display="none"; $("p2wrap").style.display="block";
  $("phaseNote").textContent="Phase 2: adjust your measures and run on. Approvals are locked, and hard structures already built cannot be removed."; renderApps(); renderChooser();}
function runPhase2(){doRun(20,"After thirty years"); $("p2btn").disabled=true;}
function drawQs(){
  $("qArea").innerHTML=D.Q.map(q=>
    `<div class="saq"><div class="tie">${q.tie}</div><p class="q">${q.n}. ${q.q}</p>`+
    `<textarea id="ta${q.n}" placeholder="Write your answer..."></textarea>`+
    `<div class="saqrow"><button class="cbtn" onclick="checkA(${q.n})">Check my answer</button><span class="wc" id="wc${q.n}">0 words</span></div>`+
    `<div class="sc" id="sc${q.n}"></div></div>`).join("");
  D.Q.forEach(q=>{const ta=$("ta"+q.n); if(ta) ta.addEventListener('input',()=>{const t=ta.value.trim();const n=t?t.split(/\s+/).length:0;$("wc"+q.n).textContent=n+" word"+(n===1?"":"s");});});
}
function checkA(n){
  const q=D.Q.find(x=>x.n===n), t=($("ta"+n).value||"").toLowerCase(), box=$("sc"+n);
  box.classList.add("show");
  if(t.trim().length<30){ box.className="sc show warn"; box.innerHTML="Have a proper go first, then press Check and I will tell you which ideas you have used."; return; }
  box.className="sc show";
  const hit=q.lookFor.filter(k=>t.includes(k)), miss=q.lookFor.filter(k=>!t.includes(k));
  let h=`<div>${q.selfcheck}</div><div style="margin-top:6px"><span class="ok">Ideas you used:</span> ${hit.length?hit.join(", "):"none of the key ideas yet"}.</div>`;
  if(miss.length) h+=`<div class="miss">You could also bring in: ${miss.slice(0,6).join(", ")}.</div>`;
  else h+=`<div class="ok" style="margin-top:3px">Good range of ideas. Now make sure each one is explained, not just named.</div>`;
  h+=`<div style="margin-top:6px;color:var(--muted)">This checks which ideas you used, not whether your reasoning is correct.</div>`;
  box.innerHTML=h;
}
function init(){st=Sim.initState(); redraw(); renderStake(); renderApps(); renderBudget(); drawQs();}
if(typeof document!=="undefined") init();
"""

HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{DATA['META']['title']}</title><style>{CSS}</style></head><body>
<header><h1>{DATA['META']['title']}</h1><div class="sub">{DATA['META']['subtitle']}</div></header>
<div class="wrap">
<div class="intro">{DATA['META']['intro']}</div>

<div class="panel">
<h2 class="sec"><span class="stepn">1</span>Read the coast through each stakeholder</h2>
<p class="lead">{DATA['META']['driftNote']} The arrows are the waves; they bend toward the coast and hit the headland hardest. Pick a stakeholder to see the coast through their eyes, then tap a point on the coast to read it and place a measure.</p>
<div id="stakeBar" class="stakebar"></div>
<div id="stakeConcern" class="concern"></div>
<div class="mapwrap"><div id="map"></div></div>
<div class="legend">
<span><i class="sw" style="background:#bcd9e6"></i>sea (arrows = waves)</span>
<span><i class="sw" style="background:#e9d8a6"></i>beach / spit</span>
<span><i class="sw" style="background:#7a9b5e"></i>dunes</span>
<span><i class="sw" style="background:#d7cfb8"></i>land / cliff</span>
<span><i class="sw" style="background:#3d7fb8"></i>river mouth</span>
<span><i class="sw" style="background:#8a5a3c"></i>town and buildings</span>
<span><i class="sw" style="background:#cf8336"></i>your measure</span>
</div>
<div id="stakePanel"></div>
<div id="budgetRow" class="budget-row"></div>
<div class="chooser" id="chooser"></div>
</div>

<div class="panel">
<h2 class="sec"><span class="stepn">2</span>Rule on the housing proposals</h2>
<p class="lead">Coastal views fetch a premium. Approving housing closer to the water raises more money for the council -- but puts those buildings at greater risk from erosion. You have to reject at least one proposal.</p>
<div id="apps"></div>
</div>

<div class="panel">
<h2 class="sec"><span class="stepn">3</span>Run the decades</h2>
<p class="note" id="phaseNote">Phase 1: rule on the housing proposals, place your measures, then run the first decade.</p>
<button class="run" id="p1btn" onclick="runPhase1()">Run the first decade (10 years)</button>
<div id="p2wrap" style="display:none"><button class="run" id="p2btn" onclick="runPhase2()">Run to thirty years</button></div>
<div class="review" id="review"></div>
<button class="btn2" onclick="downloadReport()">Download the plan</button>
</div>

<div class="panel">
<h2 class="sec"><span class="stepn">4</span>Explain your plan like a geographer</h2>
<p class="lead">Use the evidence you explored and what happened when you ran the decades. The check button tells you which ideas you used, not whether your reasoning is right.</p>
<div id="qArea"></div>
</div>

</div><script>{JS.replace('__DATA__', DATA_JSON)}</script></body></html>"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT,"w",encoding="utf-8").write(HTML)
print("wrote",OUT,len(HTML),"bytes")
