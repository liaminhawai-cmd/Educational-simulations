#!/usr/bin/env python3
# Build the v2 offline Coasts sim from data_coasts2.py.  Run: python3 build_coasts2.py
# Out: /mnt/user-data/outputs/Coasts-Interactive.html
import json, os
import data_coasts2 as DC

OUT = "/mnt/user-data/outputs/Coasts-Interactive.html"
DATA = {"META":DC.META,"SWELL":DC.SWELL,"SEG":DC.SEGMENTS,"STRAT":DC.STRATEGIES,
        "HOUSING":DC.HOUSING,"VOICES":DC.VOICES,"VLINES":DC.VOICE_LINES,
        "Q":DC.QUESTIONS,"C":DC.CONST}
DATA_JSON = json.dumps(DATA, ensure_ascii=False)

CSS = r"""
:root{--ink:#23202b;--muted:#6f6a78;--line:#e3e0e8;--paper:#fff;--bg:#f3f1f5;
--amber:#cf8336;--blue:#3d7fb8;--ok:#3a8a4e;--okb:#e7f1e8;--no:#b1492f;--nob:#f6e3de;--accent:#3a566b;}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);line-height:1.5;font-family:"Iowan Old Style",Palatino,Georgia,serif;font-size:15px;display:flex;flex-direction:column;overflow:hidden}
header{background:#1d2a33;color:#fff;padding:9px 18px;display:flex;align-items:baseline;gap:14px;flex:0 0 auto}
header h1{margin:0;font-size:18px}
header .sub{font-family:ui-sans-serif,system-ui,sans-serif;font-size:10.5px;color:#a9c2d0;text-transform:uppercase;letter-spacing:.08em}
.tabbar{display:flex;gap:4px;background:#13202a;padding:0 12px;flex:0 0 auto;border-bottom:4px solid var(--amber)}
.tab{cursor:pointer;font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;font-weight:600;color:#9fb6c4;background:none;border:none;padding:10px 16px;border-radius:8px 8px 0 0}
.tab:hover{color:#fff}
.tab.on{background:var(--bg);color:var(--ink)}
.stage{flex:1 1 auto;display:flex;gap:12px;padding:12px;min-height:0;overflow:hidden}
.mapcol{flex:1.55 1 0;min-width:0;min-height:0;display:flex;flex-direction:column;gap:6px}
.concern{font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;color:var(--ink);min-height:17px;flex:0 0 auto}
.mapwrap{flex:1 1 auto;min-height:0;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#bcd9e6;display:flex}
svg{display:block;width:100%;height:100%}
.legend{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:6px 13px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:11px;color:var(--muted)}
.legend span{display:inline-flex;align-items:center;gap:4px}.sw{width:12px;height:12px;border-radius:3px;display:inline-block;border:1px solid #0002}
.sidecol{flex:1 1 0;min-width:330px;max-width:440px;min-height:0;overflow-y:auto;background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:14px}
.stage.full .mapcol{display:none}
.stage.full .sidecol{max-width:none}
h2.sec{font-size:17px;margin:0 0 4px}
.lead{font-family:ui-sans-serif,system-ui,sans-serif;color:var(--muted);font-size:12.5px;margin:0 0 10px}
.stratgrid{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}
.sbtn{cursor:pointer;font-family:ui-sans-serif,system-ui,sans-serif;border:1px solid var(--line);background:#fff;border-radius:16px;padding:6px 11px;font-size:12.5px}
.sbtn.on{background:#fbf1e4;border-color:var(--amber);font-weight:600}.sbtn.locked{opacity:.45;cursor:not-allowed}
.advdis{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;margin-top:4px}.advdis .a{color:var(--ok)}.advdis .d{color:var(--no)}
@keyframes stampDown{0%{transform:rotate(-20deg) scale(2.6);opacity:0}55%{transform:rotate(5deg) scale(.92);opacity:1}78%{transform:rotate(-2deg) scale(1.05)}100%{transform:rotate(-5deg) scale(1);opacity:.92}}
.house-row{position:relative;border:1px solid var(--line);border-radius:8px;padding:11px 13px;margin-bottom:10px;overflow:hidden}
.house-row.on{border-color:var(--ok);background:#f4faf5}
.house-row h3{font-family:ui-sans-serif,system-ui,sans-serif;font-size:14px;margin:0 0 3px}
.house-row p{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;color:var(--muted);margin:0 0 8px}
.house-row .bonus{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;color:var(--ok);font-weight:700;margin-bottom:8px}
.hbtn{cursor:pointer;font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;font-weight:600;border:1px solid var(--accent);background:var(--accent);color:#fff;border-radius:7px;padding:7px 14px}
.hbtn.off{background:#fff;color:var(--accent)}
.hbtn.locked{opacity:.4;cursor:not-allowed}
.stamp-mark{position:absolute;top:10px;right:12px;transform-origin:top right;pointer-events:none;font-family:ui-sans-serif,system-ui,sans-serif;font-size:16px;font-weight:900;letter-spacing:.12em;padding:3px 10px;border-radius:3px;border:3px solid var(--ok);color:var(--ok);background:rgba(58,138,78,.07);animation:stampDown .4s cubic-bezier(.2,.6,.3,1) forwards}
button.run{font-family:ui-sans-serif,system-ui,sans-serif;cursor:pointer;border:1px solid var(--accent);background:var(--accent);color:#fff;border-radius:7px;padding:10px 16px;font-size:14px;font-weight:600}button.run:disabled{opacity:.4;cursor:not-allowed}
.voice{border-left:3px solid var(--line);padding:7px 11px;margin-bottom:8px;background:#fafafa}
.voice.eng{border-left-color:var(--accent)}.voice.good{border-left-color:var(--ok)}.voice.mixed{border-left-color:var(--amber)}.voice.bad{border-left-color:var(--no)}
.voice .who{font-family:ui-sans-serif,system-ui,sans-serif;font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}.voice p{margin:2px 0 0;font-size:13.5px}
.bigtrouble{border:2px solid var(--no);background:var(--nob);color:var(--no);border-radius:8px;padding:9px 12px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;font-weight:600;margin-bottom:9px}
.stamp{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;font-weight:700;color:var(--accent);margin:2px 0 8px}
.note{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;color:var(--muted);margin-top:6px}
textarea{width:100%;min-height:60px;font:inherit;font-size:13.5px;padding:8px;border:1px solid var(--line);border-radius:6px;resize:vertical;margin-top:6px}
.stakebar{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.skbtn{cursor:pointer;font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;border:1px solid var(--line);background:#fff;border-radius:16px;padding:6px 11px;color:var(--muted)}
.skbtn.on{font-weight:700}
.stakeview{border-left:3px solid var(--line);padding:9px 12px;background:#fafafa;margin-top:8px;border-radius:0 6px 6px 0}
.stakeview .sv-name{font-family:ui-sans-serif,system-ui,sans-serif;font-size:11.5px;font-weight:700;text-transform:uppercase;letter-spacing:.03em}
.stakeview p{margin:5px 0 6px;font-size:13.5px}
.stakeview .gh{font-family:ui-sans-serif,system-ui,sans-serif;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);margin:2px 0 3px}
.stakeview ul{margin:0;padding-left:18px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px}
.stakeview li{margin-bottom:2px}
.budget-row{display:flex;align-items:center;gap:10px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;padding:7px 10px;background:#f7fafb;border:1px solid var(--line);border-radius:6px;margin:8px 0}
.budget-bar-wrap{flex:1;height:8px;background:#e3e0e8;border-radius:4px;overflow:hidden}
.budget-bar-fill{height:100%;border-radius:4px;transition:width .25s}
.chooser{border:1px dashed var(--accent);border-radius:7px;padding:11px 13px;background:#f7fafb;margin-bottom:8px}
.chooser h3{font-family:ui-sans-serif,system-ui,sans-serif;font-size:14px;margin:0 0 6px}
.saq{border:1px solid var(--line);border-radius:7px;padding:11px 13px;margin-bottom:10px;background:#fff}
.saq .tie{font-family:ui-sans-serif,system-ui,sans-serif;font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--accent);margin-bottom:4px}
.saq .q{font-size:14px;margin:0 0 6px}
.saqrow{display:flex;align-items:center;gap:10px;margin-top:7px}
.cbtn{font-family:ui-sans-serif,system-ui,sans-serif;cursor:pointer;background:#eef1f4;border:1px solid var(--line);border-radius:6px;padding:7px 13px;font-size:12.5px;font-weight:600;color:var(--ink)}
.wc{font-family:ui-sans-serif,system-ui,sans-serif;font-size:11.5px;color:var(--muted)}
.sc{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;margin-top:9px;padding:9px 11px;border-radius:6px;background:#f7fafb;border:1px solid var(--line);display:none}
.sc.show{display:block}.sc.warn{background:#fdeccd}
.sc .miss{color:var(--no);margin-top:3px}.sc .ok{color:var(--ok)}
.btn2{font-family:ui-sans-serif,system-ui,sans-serif;cursor:pointer;border:1px solid var(--accent);background:#fff;color:var(--accent);border-radius:7px;padding:8px 13px;font-size:13px;font-weight:600;margin-top:10px}
@media(max-width:860px){
  body{overflow:auto}
  .stage{flex-direction:column;overflow:visible;height:auto}
  .mapcol{min-height:60vh}
  .sidecol{max-width:none;overflow:visible}
  .stage.full .mapcol{display:flex}
}
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
    const avgBy=(a[1]+b[1])/2, d=avgBy-P[i][1];
    const focus=clamp(C.FOCUS_LO + (d+40)/80*(C.FOCUS_HI-C.FOCUS_LO), C.FOCUS_LO, C.FOCUS_HI);
    g.push({t,n,inward,facing,focus});
  }
  return g;
}
function energyOf(st,i,emult){
  const s=st.seg[i], gg=st.g[i];
  let e=s.energyBase*(0.55+0.45*gg.facing)*gg.focus*emult;
  return e;
}

/* ===== housing helpers ===== */
function houseOn(st,id){return st.apps[id]==="approve";}
function approvedCount(st){return D.HOUSING.filter(h=>houseOn(st,h.id)).length;}

/* ===== pure sim ===== */
function clamp(v,a,b){return v<a?a:v>b?b:v;}
function initState(){
  return {seg:D.SEG.map(s=>({...s,energyBase:s.energy,sand:s.sand,dune:s.dune,retreat:0,lost:false})),
          g:geom(), meas:D.SEG.map(()=> "none"),
          apps:{clifftop:null,beachfront:null,setback:null}, houseLost:{}, stake:null,
          spend:0, year:0};
}
function applyApprovals(st){
  // clifftop homes: built on the soft cliff at The Shoulder, at risk from cliff retreat
  if(houseOn(st,'clifftop')) st.seg[1].asset='houses';
  // beachfront homes: clearing the land thins the dune vegetation buffer
  if(houseOn(st,'beachfront')) st.seg[6].dune=Math.max(0,st.seg[6].dune-0.25);
}
function stepYear(st, stormR){
  const N=st.seg.length, s=st.seg, m=st.meas, P=s.map(x=>[x.bx,x.by]);
  const storm=stormR<C.STORM_P, emult=storm?C.STORM_MULT:1;
  const E=[]; for(let i=0;i<N;i++) E[i]=energyOf(st,i,emult);
  for(let i=0;i<N;i++) if(m[i]==="seawall"){const nb=i+1; if(nb<N) E[nb]+=0.18*emult;}
  const move=s.map(()=>0);
  for(let i=0;i<N-1;i++){
    const dir=norm([P[i+1][0]-P[i][0], P[i+1][1]-P[i][1]]);
    const along=dot(SW,dir), Eb=(E[i]+E[i+1])/2;
    let Q=C.KFLUX*Eb*along;
    if(Q>0 && m[i]==="groyne") Q*=0.2;
    if(Q<0 && m[i+1]==="groyne") Q*=0.2;
    if(Q>0){const amt=Math.min(Q, s[i].sand*C.MOVEFRAC); move[i]-=amt; move[i+1]+=amt;}
    else   {const amt=Math.min(-Q, s[i+1].sand*C.MOVEFRAC); move[i+1]-=amt; move[i]+=amt;}
  }
  move[0]+=C.KFLUX*E[0]*C.SUPPLY;
  move[N-1]-=Math.min(C.KFLUX*E[N-1]*Math.max(dot(SW,norm([P[N-1][0]-P[N-2][0],P[N-1][1]-P[N-2][1]])),0), s[N-1].sand*C.MOVEFRAC);
  for(let i=0;i<N;i++){
    s[i].sand+=move[i];
    if(m[i]==="nourish") s[i].sand+=C.NOURISH-C.NOURISH*C.NOURISH_WEAR;
    if(storm && !s[i].cliff && E[i]>0.4) s[i].sand-=C.STORM_LOSS;
    if(m[i]==="seawall") s[i].sand=Math.min(s[i].sand,0.05);
    const cap=s[i].kind==="spit"?1.25:1.0;
    s[i].sand=clamp(s[i].sand,0,cap);
  }
  for(let i=0;i<N;i++){ if(s[i].cliff && s[i].soft>0.1){
    const excess=Math.max(0, E[i]*(1-C.BEACH_BUFFER*Math.min(s[i].sand,1)));
    let add=C.CLIFF_K*excess*s[i].soft;
    if(m[i]==="seawall") add=0;
    s[i].retreat+=add;
    if(s[i].asset && !s[i].lost && m[i]!=="retreat" && s[i].retreat>=C.ASSET_LIMIT) s[i].lost=true;
  }}
  // beachfront homes are flooded if the beach in front washes away
  if(houseOn(st,'beachfront') && s[5].sand < C.BEACH_LOST) st.houseLost.beachfront=true;
  st.year++;
}
function run(st,years,rng){ for(let y=0;y<years;y++) stepYear(st,rng()); }
function outcome(st){
  const s=st.seg;
  const beach=BEACH_SEGS.reduce((a,i)=>a+s[i].sand,0)/BEACH_SEGS.length;
  const dunes=(s[5].dune+s[6].dune)/2, assetsLost=s.filter(x=>x.lost).length;
  const estuary=clamp((s[8].sand/0.34)*0.55+(s[9].sand/0.62)*0.45,0,1);
  const walled=st.meas.filter(x=>x==="seawall"||x==="groyne").length;
  const clifftopLost=houseOn(st,'clifftop')&&s[1].lost, beachLost=!!st.houseLost.beachfront;
  const housesLost=(clifftopLost?1:0)+(beachLost?1:0);
  return {beach,dunes,assetsLost,estuary,walled,startBeach:START_BEACH,clifftopLost,beachLost,housesLost};
}
function voiceStates(st,o){return{
  owners:(o.estuary>=0.28)?"good":(o.estuary<0.15)?"bad":"mixed",
  eco:(o.dunes>=0.45&&o.estuary>=0.28)?"good":(o.dunes<0.25||o.estuary<0.15)?"bad":"mixed",
  town:(o.beach>=0.8*o.startBeach&&o.assetsLost===0&&o.walled<=2)?"good":(o.beach<0.5*o.startBeach||o.assetsLost>0)?"bad":"mixed",
};}
function engineerText(st,o){
  const s=st.seg, b=[];
  const dB=o.beach-o.startBeach;
  b.push(dB>0.06?"The sheltered bay has built out and the beaches are wider.":dB<-0.06?"The beaches have got thinner overall.":"The beaches have roughly held their own.");
  const lost=s.filter(x=>x.lost && x.asset!=="houses").map(x=>x.asset);
  if(lost.length) b.push("The "+lost.join(" and the ")+" "+(lost.length>1?"have":"has")+" gone over the wearing cliff.");
  if(o.clifftopLost) b.push("The new clifftop homes have fallen over the cliff -- a costly mistake.");
  if(o.beachLost) b.push("The beachfront homes have been flooded after the beach in front washed away.");
  if(st.meas.includes("seawall")) b.push("Where sea walls were built the cliff is held, but the beach in front has been washed down.");
  if((st.meas.includes("groyne")||st.meas.includes("seawall")) && s[10].sand<0.30)
    b.push("Starved of sand by the structures up the coast, Far Beach has worn away.");
  if(st.meas.includes("nourish")) b.push("The added sand makes the beaches wider, but it keeps washing away and needs topping up.");
  if(st.meas.includes("retreat")) b.push("Where buildings were moved back, the shore was left to find its own line.");
  if(s[9].sand>0.85) b.push("The spit has grown as sand drifting along the shore drops past the river mouth.");
  return b.join(" ");
}
const Sim={initState,stepYear,run,outcome,voiceStates,engineerText,applyApprovals,geom,energyOf,START_BEACH,houseOn,approvedCount};
if(typeof window!=="undefined"){ window.Sim=Sim; window._drawSVG=drawSVG; }

/* ===== MAP (pure: state -> SVG) ===== */
const MW=960, MH=560;
function coastPts(st){
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
function house(cx,gy,w,h,wall,opa){
  const x=cx-w/2;
  return `<rect x="${fx(x)}" y="${fx(gy-h)}" width="${fx(w)}" height="${fx(h)}" fill="${wall}" opacity="${opa}"/>`+
         `<path d="M${fx(x-2)} ${fx(gy-h)} L${fx(cx)} ${fx(gy-h-w*0.55)} L${fx(x+w+2)} ${fx(gy-h)} Z" fill="#6e3522" opacity="${opa}"/>`+
         `<rect x="${fx(cx-1.6)}" y="${fx(gy-h*0.62)}" width="3.2" height="${fx(h*0.5)}" fill="#5a4636" opacity="${opa}"/>`;
}
function alabel(cx,y,txt,col){return `<text x="${fx(cx)}" y="${fx(y)}" font-size="10.5" text-anchor="middle" font-weight="600" fill="${col||'#3a3226'}">${txt}</text>`;}
function drawSVG(st, sel, stake){
  const pts=coastPts(st), N=st.seg.length, ran=st.year>0;
  let o=`<svg viewBox="0 0 ${MW} ${MH}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" font-family="ui-sans-serif,system-ui,sans-serif">`;
  o+=`<rect x="0" y="0" width="${MW}" height="${MH}" fill="#bcd9e6"/>`;            // sea
  // wave arrows (refraction: deep swell bends toward facing the shore near the coast)
  for(let gx=24;gx<MW;gx+=52){ for(let gy=24;gy<MH;gy+=46){
    const cy=coastYat(pts,gx); if(gy>cy-14) continue;
    const nr=nearest(st,[gx,gy]); const t=clamp(1-nr.d/200,0,1);
    const inw=st.g[nr.i].inward; let v=norm([SW[0]*(1-t)+inw[0]*t, SW[1]*(1-t)+inw[1]*t]);
    const en=clamp(st.seg[nr.i].energyBase*(0.55+0.45*st.g[nr.i].facing)*st.g[nr.i].focus,0,1.1);
    const L=7+en*9, op=(0.25+en*0.5).toFixed(2);
    const ex=gx+v[0]*L, ey=gy+v[1]*L;
    o+=`<g stroke="#2f6f93" stroke-width="1.4" fill="none" opacity="${op}"><line x1="${gx}" y1="${gy}" x2="${ex.toFixed(1)}" y2="${ey.toFixed(1)}"/>`+
       `<path d="M${ex.toFixed(1)} ${ey.toFixed(1)} l${(-v[0]*4-v[1]*3).toFixed(1)} ${(-v[1]*4+v[0]*3).toFixed(1)} m0 0 l${(-v[0]*4+v[1]*3).toFixed(1)} ${(-v[1]*4-v[0]*3).toFixed(1)}"/></g>`;
  }}
  // land polygon (top edge = coastline)
  let land=`M 0 ${pts[0][1].toFixed(1)} `;
  pts.forEach(p=>land+=`L ${p[0].toFixed(1)} ${p[1].toFixed(1)} `);
  land+=`L ${MW} ${pts[N-1][1].toFixed(1)} L ${MW} ${MH} L 0 ${MH} Z`;
  o+=`<path d="${land}" fill="#d7cfb8"/>`;
  let grass=`M 0 ${(pts[0][1]+24).toFixed(1)} `;
  pts.forEach(p=>grass+=`L ${p[0].toFixed(1)} ${(p[1]+24).toFixed(1)} `);
  grass+=`L ${MW} ${(pts[N-1][1]+24).toFixed(1)} L ${MW} ${MH} L 0 ${MH} Z`;
  o+=`<path d="${grass}" fill="#cdc9ac" opacity="0.55"/>`;
  // beach band (sand) seaward of the coastline -- strong sand colour
  let beachOuter=[];
  for(let i=0;i<N;i++){const bp=3+st.seg[i].sand*38; beachOuter.push([pts[i][0]+st.g[i].n[0]*bp, pts[i][1]+st.g[i].n[1]*bp]);}
  let bp=`M ${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)} `;
  for(let i=1;i<N;i++) bp+=`L ${pts[i][0].toFixed(1)} ${pts[i][1].toFixed(1)} `;
  for(let i=N-1;i>=0;i--) bp+=`L ${beachOuter[i][0].toFixed(1)} ${beachOuter[i][1].toFixed(1)} `;
  o+=`<path d="${bp} Z" fill="#f2c543"/>`;
  // dunes (green) just landward at dune-bearing nodes
  for(let i=0;i<N;i++){ if(st.seg[i].dune>0.25){const x=pts[i][0], y=pts[i][1];
    o+=`<circle cx="${x.toFixed(1)}" cy="${(y+16).toFixed(1)}" r="${(7+st.seg[i].dune*9).toFixed(1)}" fill="#7a9b5e" opacity="0.9"/>`;}}
  // river mouth channel
  const ex8=pts[8][0];
  o+=`<path d="M ${(ex8-16)} ${pts[8][1].toFixed(1)} q 18 60 6 120 l 22 0 q 10 -60 4 -120 z" fill="#3d7fb8"/>`;
  // ===== old coastline as a dotted shadow (only after the years have run) =====
  if(ran){
    let op0=`M ${D.SEG[0].bx} ${D.SEG[0].by} `;
    D.SEG.forEach(s=>op0+=`L ${s.bx} ${s.by} `);
    o+=`<path d="${op0}" fill="none" stroke="#3a2f22" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round" opacity="0.55"/>`;
    o+=`<path d="${op0}" fill="none" stroke="#3a2f22" stroke-width="2.4" stroke-dasharray="9 7" opacity="0.7"/>`;
    o+=`<text x="${D.SEG[2].bx+6}" y="${D.SEG[2].by-34}" font-size="11" font-weight="700" fill="#3a2f22" opacity="0.85">- - - where the coast started</text>`;
  }
  // ===== assets (drawn landward) =====
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
      const label=i===1?(lost?"Clifftop homes (lost!)":"Clifftop homes"):(lost?"Clifftop houses (lost)":"Clifftop houses");
      for(let k=-1;k<2;k++) o+=house(cx+k*21, gy, 16, 13, lost?'#c9b7a8':'#c46a4a', opa);
      o+=alabel(cx, gy+12, label, lost?'#b1492f':'#3a3226');
      if(lost) o+=`<text x="${fx(cx)}" y="${fx(gy-26)}" font-size="15" text-anchor="middle" fill="#b1492f">&#10005;</text>`;
    }
    if(s.asset==="town"){
      const n=st.g[i].n, jx=pts[i][0], jy=pts[i][1];
      const exj=jx+n[0]*48, eyj=jy+n[1]*48;
      o+=`<line x1="${fx(jx)}" y1="${fx(jy)}" x2="${fx(exj)}" y2="${fx(eyj)}" stroke="#8a6d4b" stroke-width="4"/>`;
      for(let p=1;p<=3;p++){const px=jx+n[0]*12*p, py=jy+n[1]*12*p;
        o+=`<line x1="${fx(px-3)}" y1="${fx(py)}" x2="${fx(px+3)}" y2="${fx(py)}" stroke="#6f5538" stroke-width="2"/>`;}
      o+=`<ellipse cx="${fx(exj)}" cy="${fx(eyj-2)}" rx="9" ry="3.6" fill="#33414b"/>`;
      o+=`<line x1="${fx(exj)}" y1="${fx(eyj-2)}" x2="${fx(exj)}" y2="${fx(eyj-15)}" stroke="#33414b" stroke-width="1.4"/>`;
      o+=`<path d="M${fx(exj)} ${fx(eyj-14)} L${fx(exj+8)} ${fx(eyj-6)} L${fx(exj)} ${fx(eyj-5)} Z" fill="#e7e2d6"/>`;
      const hh=[15,22,13,18,14,20], wl=['#7d7787','#9a6440','#646f78','#86745c','#74707c','#8a5a3c'];
      for(let k=0;k<6;k++){ const bxk=cx+(k-2.5)*16, h=hh[k];
        o+=`<rect x="${fx(bxk-6)}" y="${fx(gy-h)}" width="12" height="${fx(h)}" fill="${wl[k]}"/>`;
        o+=`<path d="M${fx(bxk-7)} ${fx(gy-h)} L${fx(bxk)} ${fx(gy-h-6)} L${fx(bxk+7)} ${fx(gy-h)} Z" fill="#46414c"/>`;
        o+=`<rect x="${fx(bxk-3.2)}" y="${fx(gy-h+3)}" width="2.4" height="2.4" fill="#ffe7a8"/><rect x="${fx(bxk+0.8)}" y="${fx(gy-h+3)}" width="2.4" height="2.4" fill="#ffe7a8"/>`;
      }
      o+=`<line x1="${fx(cx-0.5)}" y1="${fx(gy-22)}" x2="${fx(cx-0.5)}" y2="${fx(gy-34)}" stroke="#46414c" stroke-width="2"/>`;
      o+=`<rect x="${fx(cx-3)}" y="${fx(gy-39)}" width="5" height="5" fill="#cf8336"/>`;
      o+=alabel(cx, gy+12, "Wattle Bay township", '#3a3226');
    }
  });
  // small dock at The Steps headland
  {const dk=pts[4], dn=st.g[4].n;
    const dex=dk[0]+dn[0]*38, dey=dk[1]+dn[1]*38;
    o+=`<line x1="${fx(dk[0])}" y1="${fx(dk[1])}" x2="${fx(dex)}" y2="${fx(dey)}" stroke="#7a6448" stroke-width="4" stroke-linecap="round"/>`;
    for(let p=1;p<=3;p++){const px=dk[0]+dn[0]*12*p, py=dk[1]+dn[1]*12*p;
      o+=`<line x1="${fx(px-3)}" y1="${fx(py)}" x2="${fx(px+3)}" y2="${fx(py)}" stroke="#5e4d38" stroke-width="2.5"/>`;}
    o+=`<ellipse cx="${fx(dex)}" cy="${fx(dey)}" rx="8" ry="3" fill="#2d3a42" opacity="0.9"/>`;
    o+=`<line x1="${fx(dex)}" y1="${fx(dey-3)}" x2="${fx(dex)}" y2="${fx(dey-14)}" stroke="#2d3a42" stroke-width="1.2"/>`;
    o+=`<path d="M${fx(dex)} ${fx(dey-13)} L${fx(dex+8)} ${fx(dey-7)} L${fx(dex)} ${fx(dey-6)} Z" fill="#e0dbd0"/>`;}
  // ===== feature name labels on the coast =====
  // sea label + wave hint
  o+=`<text x="80" y="62" font-size="13" font-weight="700" fill="#1e5a7a" opacity="0.7">Open ocean</text>`;
  o+=`<text x="80" y="77" font-size="10.5" fill="#1e5a7a" opacity="0.6">Waves travel this way  --&gt;</text>`;
  // headland
  o+=`<text x="${fx(pts[0][0]+4)}" y="${fx(pts[0][1]-46)}" font-size="12" font-weight="700" text-anchor="middle" fill="#3a2a1a">Wattle Head</text>`;
  o+=`<text x="${fx(pts[0][0]+4)}" y="${fx(pts[0][1]-33)}" font-size="10" text-anchor="middle" fill="#7a5238">(hard rock headland)</text>`;
  // cliffs
  o+=`<text x="${fx((pts[1][0]+pts[3][0])/2)}" y="${fx(pts[2][1]-42)}" font-size="11.5" font-weight="700" text-anchor="middle" fill="#8b3a1f">Soft limestone cliffs</text>`;
  o+=`<text x="${fx((pts[1][0]+pts[3][0])/2)}" y="${fx(pts[2][1]-29)}" font-size="10" text-anchor="middle" fill="#8b3a1f">(wear back fast)</text>`;
  // main beach
  o+=`<text x="${fx(pts[5][0])}" y="${fx(pts[5][1]+58)}" font-size="12" font-weight="700" text-anchor="middle" fill="#3a566b">Main Beach</text>`;
  // dune reserve
  o+=`<text x="${fx(pts[6][0])}" y="${fx(pts[6][1]+70)}" font-size="11" font-weight="700" text-anchor="middle" fill="#2a6b2a">Dune Reserve</text>`;
  o+=`<text x="${fx(pts[6][0])}" y="${fx(pts[6][1]+83)}" font-size="9.5" text-anchor="middle" fill="#2a6b2a">(plants hold the sand)</text>`;
  // river mouth -- significant site callout
  {const rx=pts[8][0], ry=pts[8][1];
    o+=`<rect x="${fx(rx-52)}" y="${fx(ry+36)}" width="104" height="36" rx="5" fill="#7c3aed" opacity="0.1" stroke="#7c3aed" stroke-width="1.5"/>`;
    o+=`<text x="${fx(rx)}" y="${fx(ry+51)}" font-size="11" font-weight="700" text-anchor="middle" fill="#7c3aed">River mouth</text>`;
    o+=`<text x="${fx(rx)}" y="${fx(ry+63)}" font-size="9.5" text-anchor="middle" fill="#7c3aed">significant site</text>`;}
  // spit
  o+=`<text x="${fx(pts[9][0])}" y="${fx(pts[9][1]-24)}" font-size="11" font-weight="700" text-anchor="middle" fill="#3a566b">The Spit</text>`;
  o+=`<text x="${fx(pts[9][0])}" y="${fx(pts[9][1]-12)}" font-size="9.5" text-anchor="middle" fill="#3a566b">(sand builds up here)</text>`;
  // longshore drift arrow label across the bay
  {const bx=(pts[5][0]+pts[7][0])/2, by=pts[6][1]-10;
    o+=`<text x="${fx(bx)}" y="${fx(by)}" font-size="10" text-anchor="middle" fill="#3a566b" opacity="0.7">--&gt; sand moves this way (longshore drift) --&gt;</text>`;}

  // ===== housing plot markers (tap to approve) =====
  D.HOUSING.forEach(h=>{
    const node=h.node, off=h.risk==='cliff'?74:h.risk==='beach'?78:90;
    const mx=D.SEG[node].bx, my=D.SEG[node].by+off, on=houseOn(st,h.id);
    const col=h.risk==='cliff'?'#b1492f':h.risk==='beach'?'#cf8336':'#3a8a4e';
    const W=72, H=60, bgFill=on?"#f4fff6":"#fffef2";
    // shadow
    o+=`<rect x="${fx(mx-W/2+2)}" y="${fx(my-6)}" width="${W}" height="${H}" rx="7" fill="#0002"/>`;
    // main box
    o+=`<rect x="${fx(mx-W/2)}" y="${fx(my-8)}" width="${W}" height="${H}" rx="7" fill="${bgFill}" stroke="${col}" stroke-width="${on?3:2}" stroke-dasharray="${on?'':'6 4'}"/>`;
    // house art inside
    if(on){o+=house(mx-12,my+32,15,12,'#c46a4a',1)+house(mx+5,my+32,14,12,'#7d7787',1)+house(mx+20,my+32,13,11,'#9a6440',1);}
    else  {o+=house(mx-8,my+32,14,11,'#b9b2a6',0.7)+house(mx+8,my+32,14,11,'#b9b2a6',0.7);}
    // money badge
    o+=`<rect x="${fx(mx-22)}" y="${fx(my-4)}" width="44" height="16" rx="4" fill="${col}"/>`;
    o+=`<text x="${fx(mx)}" y="${fx(my+8)}" font-size="11" font-weight="800" text-anchor="middle" fill="#fff">+${h.bonus} money</text>`;
    // status text
    if(on){ o+=`<text x="${fx(mx)}" y="${fx(my+48)}" font-size="11.5" font-weight="800" text-anchor="middle" fill="${col}">&#10003; APPROVED</text>`; }
    else  { o+=`<text x="${fx(mx)}" y="${fx(my+48)}" font-size="10.5" font-weight="700" text-anchor="middle" fill="${col}">tap to approve</text>`; }
    // site name label below box
    o+=alabel(mx, my+H+4, h.name, col);
    // big invisible click target
    o+=`<rect x="${fx(mx-W/2)}" y="${fx(my-8)}" width="${W}" height="${H}" rx="7" fill="#000" opacity="0" style="cursor:pointer" onclick="toggleHouse('${h.id}')"/>`;
  });
  // measure badges + click hotspots on coast nodes
  st.seg.forEach((s,i)=>{const x=pts[i][0], y=pts[i][1];
    if(st.meas[i]!=="none"){o+=`<circle cx="${x.toFixed(1)}" cy="${(y-16).toFixed(1)}" r="11" fill="#cf8336" stroke="#fff" stroke-width="2"/>`+
       `<text x="${x.toFixed(1)}" y="${(y-12).toFixed(1)}" font-size="12" text-anchor="middle" fill="#fff" font-weight="700">${D.STRAT[st.meas[i]].letter}</text>`;}
    if(sel===i) o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="17" fill="none" stroke="#cf8336" stroke-width="2.5"/>`;
    o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="16" fill="#000" opacity="0" style="cursor:pointer" onclick="clickCoast(${i})"/>`;
  });
  // stakeholder focus highlight
  if(stake){const v=D.VOICES.find(x=>x.id===stake);
    if(v&&v.focus) v.focus.forEach(i=>{const x=pts[i][0],y=pts[i][1];
      o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="21" fill="${v.colour}" opacity="0.14"/>`+
         `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="21" fill="none" stroke="${v.colour}" stroke-width="2.5" opacity="0.9"/>`;});}
  o+=`<g stroke="#1d2a33" stroke-width="1.5" fill="#1d2a33"><line x1="${MW-30}" y1="42" x2="${MW-30}" y2="18"/><path d="M${MW-30} 18 l-4 7 l4 -2 l4 2 z"/><text x="${MW-34}" y="56" font-size="10">N</text></g>`;
  o+=`<rect x="24" y="${MH-26}" width="72" height="5" fill="#1d2a33"/><text x="24" y="${MH-30}" font-size="10" fill="#1d2a33">0&#160;&#160;&#160;&#160;1 km</text>`;
  return o+`</svg>`;
}

/* ===== UI ===== */
let st, phase=1, sel=null, tab="coast";
function redraw(){ $("map").innerHTML=drawSVG(st, sel, st.stake); }
function setTab(t){
  tab=t;
  document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('on', b.dataset.t===t));
  $("stage").classList.toggle('full', t==='explain');
  renderSide();
}
function renderSide(){
  if(tab==='coast') renderCoastTab();
  else if(tab==='houses') renderHousesTab();
  else if(tab==='protect') renderProtectTab();
  else if(tab==='explain') renderExplainTab();
}

function availBudget(){
  return C.BUDGET + D.HOUSING.reduce((a,h)=>a+(houseOn(st,h.id)?(h.bonus||0):0),0);
}
function computeSpend(meas){return (meas||st.meas).reduce((a,k)=>a+((D.STRAT[k]&&D.STRAT[k].cost)||0),0);}
function budgetRowHTML(){
  const avail=availBudget(), spent=computeSpend(), rem=avail-spent;
  const pct=Math.min(Math.round(spent/avail*100),100);
  const col=pct>=90?"#b1492f":pct>=65?"#cf8336":"#3a8a4e";
  return `<div class="budget-row"><span><strong>Money:</strong> ${rem} of ${avail} left</span><div class="budget-bar-wrap"><div class="budget-bar-fill" style="width:${pct}%;background:${col}"></div></div></div>`;
}

/* ---- Tab 1: stakeholders ---- */
function renderCoastTab(){
  const bar=D.VOICES.map(v=>`<button class="skbtn${st.stake===v.id?' on':''}" style="${st.stake===v.id?`border-color:${v.colour};color:${v.colour}`:''}" onclick="setStake('${v.id}')">${v.name}</button>`).join("");
  const v=D.VOICES.find(x=>x.id===st.stake);
  let body;
  if(!v){ body=`<p class="lead">Tap a person above to see the coast through their eyes. The matching places light up on the map.</p>`; }
  else{
    const goals = (v.goals&&v.goals.length)? `<div class="gh">What they want</div><ul>${v.goals.map(g=>`<li>${g}</li>`).join("")}</ul>` : "";
    body=`<div class="stakeview" style="border-left-color:${v.colour}"><div class="sv-name" style="color:${v.colour}">${v.name}: ${v.role}</div><p>${v.view}</p>${goals}</div>`;
  }
  $("side").innerHTML=`<h2 class="sec">Who cares about this coast?</h2><p class="lead">Read each person before you decide anything. They do not all want the same thing.</p><div class="stakebar">${bar}</div>${body}`;
  updateConcern();
}
function setStake(id){ st.stake = st.stake===id? null : id; renderCoastTab(); redraw(); }
function updateConcern(){
  const v=D.VOICES.find(x=>x.id===st.stake);
  $("stakeConcern").innerHTML = v? `<span style="color:${v.colour}">&#9679;</span> ${v.concern}` : "Tip: tap a person, then look at where their places light up on the map.";
}

/* ---- Tab 2: houses ---- */
function renderHousesTab(){
  const lim=C.APP_LIMIT, n=Sim.approvedCount(st), atLim=n>=lim;
  let out=`<h2 class="sec">Where can new houses go?</h2>`;
  out+=`<p class="lead">Tap a house plot on the map (or the buttons below) to approve it. Closer to the water means more money for the council, but more danger of being lost to the waves. You can approve <strong>${lim} of ${D.HOUSING.length}</strong> sites. ${atLim?"You have used both.":(lim-n)+" left."}</p>`;
  out+=budgetRowHTML();
  D.HOUSING.forEach(h=>{
    const on=houseOn(st,h.id), locked=phase===2, blk=!on&&atLim;
    out+=`<div class="house-row${on?' on':''}">`;
    out+=`<h3>${h.name}</h3><p>${h.blurb}</p><div class="bonus">+${h.bonus} money if approved</div>`;
    if(locked){ out+=`<div class="note" style="margin:0">Locked in: ${on?'approved':'not approved'}</div>`; }
    else if(on){ out+=`<button class="hbtn" onclick="toggleHouse('${h.id}')">Approved &middot; tap to cancel</button>`; }
    else if(blk){ out+=`<button class="hbtn off locked">Approve (no slots left)</button>`; }
    else { out+=`<button class="hbtn off" onclick="toggleHouse('${h.id}')">Approve this site</button>`; }
    if(on) out+=`<div class="stamp-mark">APPROVED</div>`;
    out+=`</div>`;
  });
  $("side").innerHTML=out;
}
function toggleHouse(id){
  if(phase===2) return;
  if(houseOn(st,id)){ st.apps[id]=null; }
  else{
    if(Sim.approvedCount(st)>=C.APP_LIMIT){ setTab('houses'); return; }
    st.apps[id]="approve";
  }
  setTab('houses');   // always show the houses panel so students see the change
  redraw();
}

/* ---- Tab 3: protect & run ---- */
function energyWord(e){return e>0.7?"high":e>0.4?"medium":"low";}
function renderProtectTab(){
  let out=`<h2 class="sec">Protect the coast, then run the years</h2>`;
  out+=`<p class="lead">Tap a spot on the map to see what it is like, then choose a way to protect it. Watch your money.</p>`;
  out+=budgetRowHTML();
  // chooser
  if(sel===null){ out+=`<div class="chooser"><p class="lead" style="margin:0">No spot chosen yet. Tap the coast on the map.</p></div>`; }
  else{
    const s=st.seg[sel];
    const eff=energyWord(s.energyBase*(0.55+0.45*st.g[sel].facing)*st.g[sel].focus);
    const built=(phase===2 && ["seawall","groyne"].includes(st.meas[sel]));
    const opts=Object.keys(D.STRAT).map(k=>{
      const on=st.meas[sel]===k?" on":"";
      const lock=built&&k!==st.meas[sel]?" locked":"";
      const cost=D.STRAT[k].cost>0?` (${D.STRAT[k].cost})`:"";
      return `<button class="sbtn${on}${lock}" onclick="${built&&k!==st.meas[sel]?'':`setMeasure('${k}')`}">${D.STRAT[k].name}${cost}</button>`;
    }).join("");
    const cur=D.STRAT[st.meas[sel]];
    out+=`<div class="chooser"><h3>${s.name}</h3>
      <div class="lead" style="margin:0 0 4px">${s.cliff?"Cliff":"Sandy coast"} &middot; waves hit ${eff}${s.soft>0.5?" &middot; soft rock (wears fast)":s.soft<0.2?" &middot; hard rock":" &middot; medium rock"}${s.asset?` &middot; has the ${s.asset}`:""}</div>
      <div class="stratgrid">${opts}</div>
      <div class="advdis"><span class="a">+ ${cur.adv}</span><br><span class="d">&minus; ${cur.dis}</span></div>
      <div id="budgetMsg" style="color:var(--no);font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;min-height:15px;margin-top:3px"></div>
      ${built?'<div class="note">A hard wall is built here and cannot be taken out cheaply.</div>':''}</div>`;
  }
  // run controls
  out+=`<p class="note" id="phaseNote">${phase===1?"When you are ready, run the first ten years.":"Adjust your measures, then run on. Houses are locked in now."}</p>`;
  if(phase===1) out+=`<button class="run" id="p1btn" onclick="runPhase1()">Run 10 years &#9654;</button>`;
  else out+=`<button class="run" id="p2btn" onclick="runPhase2()"${st.year>=30?' disabled':''}>Run to 30 years &#9654;</button>`;
  out+=`<div class="review" id="review">${st._reviewHTML||""}</div>`;
  if(st.year>0) out+=`<button class="btn2" onclick="downloadReport()">Download the plan</button>`;
  $("side").innerHTML=out;
}
function clickCoast(i){ sel=i; if(tab!=='protect'){ setTab('protect'); } else { renderProtectTab(); } redraw(); }
function setMeasure(k){
  const test=[...st.meas]; test[sel]=k;
  if(computeSpend(test)>availBudget()){ const msg=$("budgetMsg"); if(msg) msg.textContent="Not enough money. Take out or change another measure first."; return; }
  st.meas[sel]=k; st.spend=computeSpend();
  renderProtectTab(); redraw();
}

/* ---- run logic ---- */
function mkRng(seed){let s=seed>>>0;return ()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function doRun(years,label){
  if(phase===1) Sim.applyApprovals(st);
  Sim.run(st,years,mkRng(4242+st.year));
  const o=Sim.outcome(st), vs=Sim.voiceStates(st,o);
  let h="";
  if(o.housesLost>0){ h+=`<div class="bigtrouble">Big trouble: ${o.housesLost===1?"a set of new homes has":"new homes have"} been lost to the sea. Building too close to the water has cost the council dearly.</div>`; }
  h+=`<div class="stamp">${label} (year ${st.year})</div>`;
  h+=`<div class="voice eng"><div class="who">Coastal engineer</div><p>${Sim.engineerText(st,o)}</p></div>`;
  D.VOICES.filter(v=>v.id!=="engineer").forEach(v=>{const stt=vs[v.id]; if(!stt) return;
    h+=`<div class="voice ${stt}"><div class="who">${v.name}</div><p>${D.VLINES[v.id][stt]}</p></div>`;});
  st._reviewHTML=h;
  redraw();
}
function runPhase1(){
  doRun(10,"After the first ten years"); phase=2;
  renderProtectTab();
}
function runPhase2(){ doRun(20,"After thirty years"); renderProtectTab(); }

/* ---- Tab 4: explain ---- */
function renderExplainTab(){
  let out=`<h2 class="sec">Explain your plan like a geographer</h2><p class="lead">Use what you saw on the map. The check button tells you which ideas you used, not whether your reasoning is right.</p><div id="qArea"></div>`;
  $("side").innerHTML=out;
  $("qArea").innerHTML=D.Q.map(q=>
    `<div class="saq"><div class="tie">${q.tie}</div><p class="q">${q.n}. ${q.q}</p>`+
    `<textarea id="ta${q.n}" placeholder="Write your answer...">${st._ans&&st._ans[q.n]||""}</textarea>`+
    `<div class="saqrow"><button class="cbtn" onclick="checkA(${q.n})">Check my answer</button><span class="wc" id="wc${q.n}">0 words</span></div>`+
    `<div class="sc" id="sc${q.n}"></div></div>`).join("");
  D.Q.forEach(q=>{const ta=$("ta"+q.n); if(ta){const upd=()=>{const t=ta.value.trim();const n=t?t.split(/\s+/).length:0;$("wc"+q.n).textContent=n+" word"+(n===1?"":"s");st._ans=st._ans||{};st._ans[q.n]=ta.value;};ta.addEventListener('input',upd);upd();}});
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

function downloadReport(){
  const o=Sim.outcome(st), vs=Sim.voiceStates(st,o);
  const dec=D.HOUSING.map(h=>`  ${h.name}: ${houseOn(st,h.id)?"approved":"not approved"}`).join("\n");
  const mez=st.seg.map((s,i)=>st.meas[i]!=="none"?`  ${s.name}: ${D.STRAT[st.meas[i]].name}`:null).filter(Boolean).join("\n")||"  (none)";
  const vlines=D.VOICES.filter(v=>v.id!=="engineer").map(v=>`  ${v.name}: ${D.VLINES[v.id][vs[v.id]]}`).join("\n");
  const txt=`WATTLE BAY COASTAL PLAN, year ${st.year}\n\nMONEY: ${computeSpend()} of ${availBudget()} spent\n\nHOUSING DECISIONS\n${dec}\n\nPROTECTION MEASURES\n${mez}\n\nWHAT HAPPENED\n  Coastal engineer: ${Sim.engineerText(st,o)}\n${vlines}\n`;
  const b=new Blob([txt],{type:"text/plain"}); const u=URL.createObjectURL(b);
  const a=document.createElement("a"); a.href=u; a.download="wattle-bay-plan.txt"; a.click(); URL.revokeObjectURL(u);
}

function init(){ st=Sim.initState(); redraw(); setTab("coast"); updateConcern(); }
if(typeof document!=="undefined") init();
"""

HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{DATA['META']['title']}</title><style>{CSS}</style></head><body>
<header><h1>{DATA['META']['title']}</h1><div class="sub">{DATA['META']['subtitle']}</div></header>
<div class="tabbar">
  <button class="tab on" data-t="coast" onclick="setTab('coast')">1 &middot; Stakeholders</button>
  <button class="tab" data-t="houses" onclick="setTab('houses')">2 &middot; Houses</button>
  <button class="tab" data-t="protect" onclick="setTab('protect')">3 &middot; Protect &amp; run</button>
  <button class="tab" data-t="explain" onclick="setTab('explain')">4 &middot; Explain</button>
</div>
<div class="stage" id="stage">
  <div class="mapcol">
    <div id="stakeConcern" class="concern"></div>
    <div class="mapwrap"><div id="map" style="width:100%;height:100%"></div></div>
    <div class="legend">
      <span><i class="sw" style="background:#bcd9e6"></i>sea (arrows = waves)</span>
      <span><i class="sw" style="background:#f2c543"></i>beach now</span>
      <span><i class="sw" style="background:#7a9b5e"></i>dunes</span>
      <span><i class="sw" style="background:#d7cfb8"></i>land / cliff</span>
      <span><i class="sw" style="background:#3d7fb8"></i>river mouth</span>
      <span><i class="sw" style="background:#cf8336"></i>your measure</span>
      <span>&#8226;&#8226;&#8226; old coastline</span>
    </div>
  </div>
  <div class="sidecol" id="side"></div>
</div>
<script>{JS.replace('__DATA__', DATA_JSON)}</script></body></html>"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT,"w",encoding="utf-8").write(HTML)
print("wrote",OUT,len(HTML),"bytes")
