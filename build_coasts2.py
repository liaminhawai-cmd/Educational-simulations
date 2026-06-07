#!/usr/bin/env python3
# Build the v2 offline Coasts sim from data_coasts2.py.  Run: python3 build_coasts2.py
# Out: /mnt/user-data/outputs/Wattle-Bay-Coastal-Manager-v13.html
import json, os
import data_coasts2 as DC

OUT = "/mnt/user-data/outputs/Coasts-Interactive.html"
DATA = {"META":DC.META,"SWELL":DC.SWELL,"SEG":DC.SEGMENTS,"STRAT":DC.STRATEGIES,
        "APPS":DC.APPLICATIONS,"VOICES":DC.VOICES,
        "VLINES":DC.VOICE_LINES,"C":DC.CONST}
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
.tabs{display:flex;gap:4px;flex-wrap:wrap;border-bottom:2px solid var(--line);margin-bottom:12px}
.tab{cursor:pointer;border:1px solid var(--line);border-bottom:none;background:#e7ebee;border-radius:6px 6px 0 0;padding:8px 14px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;font-weight:600;color:var(--muted)}
.tab.on{background:var(--paper);color:var(--ink);border-color:var(--accent)}
.view{display:none}.view.on{display:block}
.panel{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:14px;margin-bottom:12px}
.lead{font-family:ui-sans-serif,system-ui,sans-serif;color:var(--muted);font-size:13px;margin:0 0 10px}
h2.sec{font-size:18px;margin:0 0 6px}
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
.app{border:1px solid var(--line);border-radius:7px;padding:11px 13px;margin-bottom:9px}
.app h3{font-family:ui-sans-serif,system-ui,sans-serif;font-size:14.5px;margin:0 0 3px}.app p{font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;color:var(--muted);margin:0 0 8px}
.toggle{display:inline-flex;border:1px solid var(--line);border-radius:18px;overflow:hidden}
.toggle button{cursor:pointer;border:none;background:#fff;font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;padding:6px 14px;color:var(--muted)}
.toggle button.approve.on{background:var(--okb);color:var(--ok);font-weight:600}.toggle button.reject.on{background:var(--nob);color:var(--no);font-weight:600}.toggle button.locked{opacity:.5;cursor:not-allowed}
button.run{font-family:ui-sans-serif,system-ui,sans-serif;cursor:pointer;border:1px solid var(--accent);background:var(--accent);color:#fff;border-radius:7px;padding:11px 18px;font-size:14.5px;font-weight:600}button.run:disabled{opacity:.4;cursor:not-allowed}
.voice{border-left:3px solid var(--line);padding:8px 12px;margin-bottom:9px;background:#fafafa}
.voice.eng{border-left-color:var(--accent)}.voice.good{border-left-color:var(--ok)}.voice.mixed{border-left-color:var(--amber)}.voice.bad{border-left-color:var(--no)}
.voice .who{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}.voice p{margin:3px 0 0;font-size:14px}
.stamp{font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;font-weight:700;color:var(--accent);margin:4px 0 10px}
.note{font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;color:var(--muted);margin-top:8px}
textarea{width:100%;min-height:60px;font:inherit;font-size:14px;padding:8px;border:1px solid var(--line);border-radius:6px;resize:vertical;margin-top:6px}
.stakebar{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}
.skbtn{cursor:pointer;font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;border:1px solid var(--line);background:#fff;border-radius:16px;padding:6px 11px;color:var(--muted)}
.skbtn.on{font-weight:700}
.concern{font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;color:var(--ink);min-height:18px;margin:0 0 8px}
.toggle button.cond.on{background:#fff4e2;color:#a9671f;font-weight:600}
.btn2{font-family:ui-sans-serif,system-ui,sans-serif;cursor:pointer;border:1px solid var(--accent);background:#fff;color:var(--accent);border-radius:7px;padding:9px 14px;font-size:13.5px;font-weight:600;margin-top:10px}
.stakeview{border-left:3px solid var(--line);padding:10px 13px;background:#fafafa;margin-top:10px;border-radius:0 6px 6px 0}
.stakeview .sv-name{font-family:ui-sans-serif,system-ui,sans-serif;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.03em}
.stakeview p{margin:5px 0 6px;font-size:14px}
.stakeview ul{margin:0;padding-left:18px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:13.5px}
.stakeview li{margin-bottom:2px}
.budget-row{display:flex;align-items:center;gap:10px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:13px;padding:8px 10px;background:#f7fafb;border:1px solid var(--line);border-radius:6px;margin-top:10px}
.budget-bar-wrap{flex:1;height:8px;background:#e3e0e8;border-radius:4px;overflow:hidden}
.budget-bar-fill{height:100%;border-radius:4px;transition:width .25s}
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
  if(st.meas[i]==="dunes")  e*=(1-0.25*Math.max(s.dune,0.5));
  return e;
}

/* ===== pure sim ===== */
function clamp(v,a,b){return v<a?a:v>b?b:v;}
function initState(){
  return {seg:D.SEG.map(s=>({...s,energyBase:s.energy,sand:s.sand,dune:s.dune,retreat:0,lost:false})),
          g:geom(), meas:D.SEG.map(()=> "none"),
          apps:{trawl:null,marina:null,housing:null,caravan:null,oyster:null}, stake:null,
          fish:1.0, spend:0, year:0};
}
function applyApprovals(st){ if(st.apps.housing==="approve" && st.seg[4].asset===null) st.seg[4].asset="houses"; }
function appLvl(st,id){return ({approve:1,conditions:0.5})[st.apps[id]]||0;}
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
    if(i===7) Q*=(1-0.5*appLvl(st,'marina'));     // dredged channel cuts drift past the township
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
    if(i===7) s[i].sand-=0.05*emult*appLvl(st,'marina');          // dredging sink
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
  if(st.apps.caravan==="approve" && m[6]!=="dunes") s[6].dune=clamp(s[6].dune-0.02,0,1);
  if(m[6]==="dunes") s[6].dune=clamp(s[6].dune+0.01,0,1);
  const tl=appLvl(st,'trawl');
  st.fish = clamp(st.fish + (tl>0? -C.FISH_TRAWL*tl : C.FISH_RECOVER), 0, 1);
  st.year++;
}
function run(st,years,rng){ for(let y=0;y<years;y++) stepYear(st,rng()); }
function outcome(st){
  const s=st.seg;
  const beach=BEACH_SEGS.reduce((a,i)=>a+s[i].sand,0)/BEACH_SEGS.length;
  const dunes=(s[5].dune+s[6].dune)/2, assetsLost=s.filter(x=>x.lost).length;
  const estuary=clamp((s[8].sand/0.34)*0.55+(s[9].sand/0.62)*0.45-appLvl(st,'marina')*0.30-appLvl(st,'trawl')*0.15,0,1);
  const walled=st.meas.filter(x=>x==="seawall"||x==="groyne").length;
  const approved=Object.values(st.apps).filter(v=>v==="approve"||v==="conditions").length;
  return {beach,dunes,assetsLost,estuary,fish:st.fish,walled,approved,startBeach:START_BEACH};
}
function voiceStates(st,o){const mar=appLvl(st,'marina'), tr=appLvl(st,'trawl');return{
  owners:(o.estuary>=0.42 && !(mar>0&&o.estuary<0.55))?"good":(o.estuary<0.18||(mar>0&&o.estuary<0.35))?"bad":"mixed",
  eco:(o.dunes>=0.45&&o.estuary>=0.28&&o.fish>=0.55&&tr===0)?"good":(o.dunes<0.25||o.estuary<0.15||o.fish<0.40)?"bad":"mixed",
  town:(o.beach>=0.8*o.startBeach&&o.assetsLost===0&&o.walled<=2)?"good":(o.beach<0.5*o.startBeach||o.assetsLost>0)?"bad":"mixed",
  fish:(o.fish>=0.55&&o.approved>=1)?"good":(o.fish<0.40||o.approved===0)?"bad":"mixed"};}
function engineerText(st,o){
  const s=st.seg, b=[];
  const dB=o.beach-o.startBeach;
  b.push(dB>0.06?"The sheltered bay has built out, beaches widening.":dB<-0.06?"The beaches have thinned overall.":"The beaches have roughly held.");
  const lost=s.filter(x=>x.lost).map(x=>x.asset);
  if(lost.length) b.push("The "+lost.join(" and the ")+" "+(lost.length>1?"have":"has")+" gone over the eroding cliff.");
  if((st.meas.includes("groyne")||st.meas.includes("seawall")) && s[10].sand<0.30)
    b.push("Starved of sand by the structures updrift, Far Beach has worn away.");
  if(st.apps.marina && s[8].sand<0.24) b.push("Dredging has cut the sand feeding the river mouth and the spit.");
  if(s[9].sand>0.85) b.push("The spit has grown as the drift drops its load past the river mouth.");
  return b.join(" ");
}
const Sim={initState,stepYear,run,outcome,voiceStates,engineerText,applyApprovals,geom,energyOf,START_BEACH};
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
  const em=st.seg[8], ex=pts[8][0];
  o+=`<path d="M ${(ex-16)} ${pts[8][1].toFixed(1)} q 18 60 6 120 l 22 0 q 10 -60 4 -120 z" fill="#3d7fb8"/>`;
  // assets (drawn landward of the coastline)
  st.seg.forEach((s,i)=>{ if(!s.asset) return;
    const x=pts[i][0], y=pts[i][1]+30, lost=s.lost, opa=lost?0.35:1;
    if(s.asset==="road") o+=`<rect x="${x-34}" y="${y}" width="68" height="7" rx="2" fill="${lost?'#caa':'#8a6d4b'}" opacity="${opa}"/>`;
    if(s.asset==="houses"){for(let k=-1;k<2;k++) o+=`<rect x="${x+k*18-6}" y="${y}" width="13" height="11" fill="${lost?'#caa':'#b1492f'}" opacity="${opa}"/>`; if(lost) o+=`<text x="${x}" y="${y+9}" font-size="13" text-anchor="middle" fill="#b1492f">&#10005;</text>`;}
    if(s.asset==="town"){for(let k=-1;k<3;k++) o+=`<rect x="${x+k*15-4}" y="${y}" width="11" height="13" fill="#6f6a78"/>`;}
  });
  // measure badges + click hotspots + labels
  st.seg.forEach((s,i)=>{const x=pts[i][0], y=pts[i][1];
    if(st.meas[i]!=="none"){o+=`<circle cx="${x.toFixed(1)}" cy="${(y-16).toFixed(1)}" r="11" fill="#cf8336" stroke="#fff" stroke-width="2"/>`+
       `<text x="${x.toFixed(1)}" y="${(y-12).toFixed(1)}" font-size="12" text-anchor="middle" fill="#fff" font-weight="700">${D.STRAT[st.meas[i]].letter}</text>`;}
    if(sel===i) o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="17" fill="none" stroke="#cf8336" stroke-width="2.5"/>`;
    o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="18" fill="#000" opacity="0" style="cursor:pointer" onclick="selectSeg(${i})"/>`;
    o+=`<text x="${x.toFixed(1)}" y="${(y+ (s.cliff?-30:54)).toFixed(1)}" font-size="9.5" text-anchor="middle" fill="#3a566b">${i}</text>`;
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

function computeSpend(meas){
  return (meas||st.meas).reduce((a,k)=>a+((D.STRAT[k]&&D.STRAT[k].cost)||0),0);
}
function renderBudget(){
  const spent=computeSpend(), rem=C.BUDGET-spent;
  const pct=Math.min(Math.round(spent/C.BUDGET*100),100);
  const col=pct>=90?"#b1492f":pct>=65?"#cf8336":"#3a8a4e";
  $("budgetRow").innerHTML=`<span><strong>Budget:</strong> ${rem} of ${C.BUDGET} remaining</span><div class="budget-bar-wrap"><div class="budget-bar-fill" style="width:${pct}%;background:${col}"></div></div>`;
}

function renderStake(){
  $("stakeBar").innerHTML=D.VOICES.map(v=>`<button class="skbtn${st.stake===v.id?' on':''}" style="${st.stake===v.id?`border-color:${v.colour};color:${v.colour}`:''}" onclick="setStake('${v.id}')">${v.name}</button>`).join("");
  const v=D.VOICES.find(x=>x.id===st.stake);
  $("stakeConcern").innerHTML = v? `<span style="color:${v.colour}">&#9679;</span> ${v.concern}` : "";
  const sp=$("stakePanel");
  if(!v){
    sp.innerHTML=`<p class="lead" style="margin:10px 0 0">Pick a stakeholder to see the coast through their eyes.</p>`;
    return;
  }
  const goalItems=v.goals.map(g=>`<li>${g}</li>`).join("");
  sp.innerHTML=`<div class="stakeview" style="border-left-color:${v.colour}"><div class="sv-name" style="color:${v.colour}">${v.name}: ${v.role}</div><p>${v.view}</p><ul>${goalItems}</ul></div>`;
}
function setStake(id){ st.stake = st.stake===id? null : id; renderStake(); redraw(); }

function downloadReport(){
  const o=Sim.outcome(st), vs=Sim.voiceStates(st,o);
  const spent=computeSpend();
  const dec=D.APPS.map(a=>`  ${a.name}: ${st.apps[a.id]||"undecided"}`).join("\n");
  const mez=st.seg.map((s,i)=>st.meas[i]!=="none"?`  ${i} ${s.name}: ${D.STRAT[st.meas[i]].name}`:null).filter(Boolean).join("\n")||"  (none)";
  const vlines=D.VOICES.filter(v=>v.id!=="engineer").map(v=>`  ${v.name}: ${D.VLINES[v.id][vs[v.id]]}`).join("\n");
  const txt=`WATTLE BAY COASTAL PLAN, year ${st.year}\n\nBUDGET: ${spent} of ${C.BUDGET} spent\n\nDEVELOPMENT DECISIONS\n${dec}\n\nMANAGEMENT MEASURES\n${mez}\n\nWHAT HAPPENED\n  Coastal engineer: ${Sim.engineerText(st,o)}\n${vlines}\n`;
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
  ch.innerHTML=`<h3>${sel} · ${s.name}</h3>
    <div class="lead" style="margin:0 0 4px">${s.cliff?"Cliff":"Sandy coast"} · wave energy ${eff} · ${s.soft>0.5?"soft rock (erodes fast)":s.soft<0.2?"hard rock":"medium rock"}${s.asset?` · protects the ${s.asset}`:""}</div>
    <div class="stratgrid">${opts}</div>
    <div class="advdis"><span class="a">+ ${cur.adv}</span><br><span class="d">&minus; ${cur.dis}</span></div>
    <div id="budgetMsg" style="color:var(--no);font-family:ui-sans-serif,system-ui,sans-serif;font-size:12.5px;min-height:16px;margin-top:3px"></div>
    ${built?'<div class="note">A hard structure is built here and cannot be removed cheaply.</div>':''}`;
}
function setMeasure(k){
  const test=[...st.meas]; test[sel]=k;
  const newSpend=computeSpend(test);
  if(newSpend>C.BUDGET){
    const msg=$("budgetMsg"); if(msg) msg.textContent="Over budget. Remove or swap a measure first.";
    return;
  }
  st.meas[sel]=k; st.spend=newSpend;
  renderChooser(); redraw(); renderBudget();
}
function renderApps(){$("apps").innerHTML=D.APPS.map(a=>{const v=st.apps[a.id], lock=phase===2;
  const b=(val,cls,label)=>`<button class="${cls}${v===val?' on':''}${lock?' locked':''}" onclick="${lock?'':`setApp('${a.id}','${val}')`}">${label}</button>`;
  return `<div class="app"><h3>${a.name}</h3><p>${a.brief}</p><div class="toggle">
    ${b('approve','approve','Approve')}${b('conditions','cond','With conditions')}${b('reject','reject','Reject')}</div></div>`;}).join("");}
function setApp(id,val){st.apps[id]=val; renderApps();}
function mkRng(seed){let s=seed>>>0;return ()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function doRun(years,label){
  if(phase===1) Sim.applyApprovals(st);
  Sim.run(st,years,mkRng(4242+st.year));
  const o=Sim.outcome(st), vs=Sim.voiceStates(st,o);
  let h=`<div class="stamp">${label} (year ${st.year})</div>`;
  h+=`<div class="voice eng"><div class="who">Coastal engineer</div><p>${Sim.engineerText(st,o)}</p></div>`;
  D.VOICES.filter(v=>v.id!=="engineer").forEach(v=>{const stt=vs[v.id];
    h+=`<div class="voice ${stt}"><div class="who">${v.name}</div><p>${D.VLINES[v.id][stt]}</p></div>`;});
  $("review").innerHTML=h; redraw(); renderChooser(); renderApps();
}
function runPhase1(){
  if(Object.values(st.apps).some(v=>!v)){ $("phaseNote").textContent="Rule on every application first (Applications tab), then run."; return; }
  doRun(10,"After the first decade"); phase=2; $("p1btn").style.display="none"; $("p2wrap").style.display="block";
  $("phaseNote").textContent="Phase 2: adjust your measures and run on. Approvals are locked, and hard structures already built cannot be removed."; renderApps(); renderChooser();}
function runPhase2(){doRun(20,"After thirty years"); $("p2btn").disabled=true; $("reflect").style.display="block";}
function setView(v){document.querySelectorAll(".tab").forEach(t=>t.classList.toggle("on",t.dataset.v===v));
  document.querySelectorAll(".view").forEach(w=>w.classList.toggle("on",w.id==="v-"+v));}
function init(){st=Sim.initState(); redraw(); renderStake(); renderApps(); renderBudget();}
if(typeof document!=="undefined") init();
"""

HTML = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{DATA['META']['title']}</title><style>{CSS}</style></head><body>
<header><h1>{DATA['META']['title']}</h1><div class="sub">{DATA['META']['subtitle']}</div></header>
<div class="wrap">
<div class="intro">{DATA['META']['intro']}</div>
<div class="tabs">
<div class="tab on" data-v="map" onclick="setView('map')">The coast</div>
<div class="tab" data-v="apps" onclick="setView('apps')">Applications</div>
</div>
<div id="v-map" class="view on">
<div class="panel">
<h2 class="sec">Wattle Bay</h2>
<p class="lead">{DATA['META']['driftNote']} The arrows are the waves; they bend toward the coast and hit the headland hardest. Pick a stakeholder to see the coast through their eyes. Tap a point on the coast to read it and place a measure.</p>
<div id="stakeBar" class="stakebar"></div>
<div id="stakeConcern" class="concern"></div>
<div class="mapwrap"><div id="map"></div></div>
<div class="legend">
<span><i class="sw" style="background:#bcd9e6"></i>sea (arrows = waves)</span>
<span><i class="sw" style="background:#e9d8a6"></i>beach / spit</span>
<span><i class="sw" style="background:#7a9b5e"></i>dunes</span>
<span><i class="sw" style="background:#d7cfb8"></i>land / cliff</span>
<span><i class="sw" style="background:#3d7fb8"></i>river mouth</span>
<span><i class="sw" style="background:#cf8336"></i>your measure</span>
</div>
<div id="stakePanel"></div>
<div id="budgetRow" class="budget-row"></div>
<div class="chooser" id="chooser"></div>
</div>
<div class="panel">
<p class="note" id="phaseNote">Phase 1: rule on the applications, place your measures, then run the first decade.</p>
<button class="run" id="p1btn" onclick="runPhase1()">Run the first decade (10 years)</button>
<div id="p2wrap" style="display:none"><button class="run" id="p2btn" onclick="runPhase2()">Run to thirty years</button></div>
<div class="review" id="review"></div>
<button class="btn2" onclick="downloadReport()">Download the plan</button>
<div id="reflect" style="display:none">
<p class="note">Some houses at Wattle Bay were built dangerously close to the cliff. Using what just happened, what advice would you give planners, builders and buyers? (about 25 words)</p>
<textarea placeholder="Your advice..."></textarea></div>
</div>
</div>
<div id="v-apps" class="view"><div class="panel"><h2 class="sec">Development applications</h2>
<p class="lead">Approve or reject each. Every approval is money for the area and a pressure on the coast.</p><div id="apps"></div></div></div>
</div><script>{JS.replace('__DATA__', DATA_JSON)}</script></body></html>"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT,"w",encoding="utf-8").write(HTML)
print("wrote",OUT,len(HTML),"bytes")
