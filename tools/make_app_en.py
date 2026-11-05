# -*- coding: utf-8 -*-
"""Build the English smart-quiz web app (index.html + q/ image folder)."""
import json, os, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT
from sections import SECTIONS, CHAPTERS, BY_Q
from method_a import M1
from method_b import M2
from expl_all import E
from terms import SHORT, GLOSSARY
from make_outline import FORMULAS

OUT = os.path.join(ROOT, "out", "MTH026_QuizEN")
QSRC = os.path.join(ROOT, "qbank", "q")
ASSETS = os.path.join(ROOT, "assets")
ANS = json.load(open(os.path.join(ROOT, "build", "answers_final.json")))
PIT = json.load(open(os.path.join(ROOT, "build", "pitems.json")))

M = {**M1, **M2}


def esc(t):
    """HTML-escape prose before it is injected with innerHTML.

    A raw '<' inside a solution (e.g. $-7<x<4$) otherwise opens a bogus tag
    and the browser eats the rest of the sentence.  Escape first; KaTeX reads
    textContent afterwards, so the maths still renders correctly.
    """
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build_data():
    items = []
    for n in range(1, 352):
        sec = BY_Q[n]
        en, zh = E.get(n, ("", ""))
        m = M[sec["id"]]
        items.append({
            "id": n, "s": sec["id"], "c": sec["ch"], "a": ANS[str(n)]["ans"],
            "en": esc(en), "zh": esc(zh),
            "focus": esc(m["focus"]), "trap": esc(m["trap"]),
        })
    secs = [{"id": s["id"], "en": s["en"], "zh": s["zh"], "n": s["n"], "ch": s["ch"],
             "from": s["start"], "to": s["end"]} for s in SECTIONS]
    chs = [{"n": c[0], "en": c[1], "zh": c[2]} for c in CHAPTERS]
    # Part B: ids sit in their own range so they can never collide with Q1-Q351.
    # No letter is stored — the printed answer is an image, and guessing which
    # option it matches is exactly the guess that failed before.  The reader
    # grades their own pick instead.
    pqch = {s["id"]: s["ch"] for s in SECTIONS}
    pq = [{"id": 1000 + it["pid"], "s": it["sec"], "c": pqch.get(it["sec"], 0),
           "p": it["pid"]} for it in PIT]
    # the knowledge map, folded in so the page needs nothing but itself
    ref = []
    for s in SECTIONS:
        m = M.get(s["id"], {})
        ref.append({
            "id": s["id"], "en": s["en"], "zh": s["zh"], "c": s["ch"],
            "n": s["n"],
            "focus": esc(m.get("focus", "")),
            "steps": [esc(x) for x in m.get("steps", [])],
            "note": esc(m.get("zh", "")),
            "trap": esc(m.get("trap", "")),
        })
    forms = [{"name": n, "rows": [[a, b] for a, b in rows]} for n, rows in FORMULAS]
    gloss = [{"g": ge, "gz": gz,
              "items": [[esc(a), esc(b), esc(c)] for a, b, c in items]}
             for ge, gz, items in GLOSSARY]
    return {"items": items, "sections": secs, "chapters": chs, "pq": pq,
            "ref": ref, "forms": forms, "gloss": gloss}


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MTH026 · Complete Question Bank &amp; Smart Quiz</title>
<link rel="stylesheet" href="katex/katex.min.css">
<style>
:root{
  --ink:#101827; --ink2:#3a4759; --ink3:#6c7b90; --ink4:#96a3b4;
  --line:#e3e9f1; --line2:#eef3f8; --bg:#f4f7fb; --paper:#fff;
  --pri:#16406e; --pri2:#2c6ba8; --pri3:#eaf1fa;
  --green:#1d6b47; --green-bg:#edf8f1; --green-line:#bfe2cd;
  --red:#a8352a; --red-bg:#fdf1ef; --red-line:#f0cdc7;
  --amber:#98621a; --amber-bg:#fdf7ec;
  --sh:0 1px 2px rgba(16,32,56,.05),0 10px 26px -14px rgba(16,32,56,.18);
  --sh2:0 2px 6px rgba(16,32,56,.07),0 22px 48px -20px rgba(16,32,56,.24);
  --r:14px;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-size:15px;line-height:1.65;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,"PingFang SC",sans-serif;
  -webkit-font-smoothing:antialiased}
button{font:inherit;cursor:pointer;border:0;background:none;color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
.hide{display:none!important}

/* topbar */
.top{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.9);backdrop-filter:blur(12px);
  border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;gap:12px;height:58px}
.brand{display:flex;align-items:center;gap:10px;font-weight:700}
.brand .mark{width:26px;height:26px;border-radius:8px;background:linear-gradient(135deg,#16406e,#2c6ba8);
  color:#fff;display:grid;place-items:center;font-size:10px;font-weight:800;letter-spacing:.03em}
.brand small{display:block;font-size:10.5px;color:var(--ink3);font-weight:500;letter-spacing:.08em;text-transform:uppercase}
.spacer{flex:1}
.chip{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid var(--line);
  border-radius:100px;padding:5px 11px;font-size:12.5px;color:var(--ink2);white-space:nowrap}
.chip b{color:var(--ink);font-variant-numeric:tabular-nums}
.btn{border-radius:10px;padding:9px 16px;font-size:14px;font-weight:600;transition:.16s}
.btn.pri{background:var(--pri);color:#fff;box-shadow:0 1px 2px rgba(22,64,110,.3)}
.btn.pri:hover{background:#12365e}
.btn.ghost{background:#fff;border:1px solid var(--line);color:var(--ink2)}
.btn.ghost:hover{border-color:#c9d5e3;background:#fafcfe}
.btn:disabled{opacity:.45;cursor:not-allowed}

/* hero */
.hero{margin:26px 0 20px;background:linear-gradient(130deg,#12325a,#1e5289 60%,#2e6fae);
  border-radius:20px;padding:30px 32px;color:#fff;position:relative;overflow:hidden;box-shadow:var(--sh2)}
.hero:after{content:"";position:absolute;inset:0;opacity:.35;pointer-events:none;
  background:radial-gradient(700px 260px at 88% -10%,rgba(255,214,140,.5),transparent 70%)}
.hero>*{position:relative;z-index:1}
.hero h1{margin:0 0 6px;font-size:26px;letter-spacing:-.01em}
.hero p{margin:0;color:#cfe0f2;font-size:14px;max-width:58ch}
.hero .row{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}
.hero .btn.light{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.3);color:#fff}
.hero .btn.light:hover{background:rgba(255,255,255,.22)}
.hero .btn.white{background:#fff;color:var(--pri)}

/* grids */
.grid{display:grid;gap:14px}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
@media(max-width:820px){.g3,.g2{grid-template-columns:1fr}}
.card{background:var(--paper);border:1px solid var(--line);border-radius:var(--r);padding:18px 18px;box-shadow:var(--sh)}
.card.click{cursor:pointer;transition:.16s}
.card.click:hover{border-color:#bcd2e8;transform:translateY(-1px);box-shadow:var(--sh2)}
.card h3{margin:0 0 4px;font-size:15px}
.card .k{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--pri2);font-weight:700}
.card p{margin:6px 0 0;font-size:13px;color:var(--ink3);line-height:1.55}
.stat{font-size:26px;font-weight:700;letter-spacing:-.02em}
.stat small{font-size:12px;font-weight:500;color:var(--ink3);margin-left:4px}

/* section list */
.sec-row{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid var(--line2)}
.sec-row:last-child{border:0}
.sec-id{font-size:11px;font-weight:700;color:#fff;background:var(--pri2);border-radius:5px;
  padding:1px 7px;min-width:38px;text-align:center}
.sec-t{flex:1;font-size:13.5px;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bar{width:112px;height:7px;border-radius:100px;background:#eef2f7;overflow:hidden;flex:0 0 auto}
.bar i{display:block;height:100%;background:var(--pri2);border-radius:100px;transition:.3s}
.bar i.ok{background:#2f9e6b}.bar i.warn{background:#e0a33a}.bar i.bad{background:#cf5b4a}
.sec-n{font-size:12px;color:var(--ink3);font-variant-numeric:tabular-nums;width:56px;text-align:right}

/* quiz */
.qwrap{max-width:760px;margin:22px auto 60px;min-height:calc(100vh - 190px);display:flex;flex-direction:column;justify-content:center}
.qwrap>*{flex:0 0 auto}
.qcard{background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:var(--sh2);overflow:hidden}
.qhead{display:flex;align-items:center;gap:10px;padding:12px 18px;background:#f7fafd;border-bottom:1px solid var(--line)}
.qno{font-size:12px;font-weight:700;color:#fff;background:var(--pri2);border-radius:6px;padding:2px 9px}
.qsec{font-size:12px;color:var(--ink3)}
.qprog{margin-left:auto;display:flex;align-items:center;gap:8px}
.qprog .track{width:130px;height:6px;background:#e7edf4;border-radius:100px;overflow:hidden}
.qprog .track i{display:block;height:100%;background:linear-gradient(90deg,#2c6ba8,#3f86c9);border-radius:100px}
.qbody{padding:16px 18px 6px}
.qimg{display:block;width:100%;height:auto;border-radius:8px}
.opts{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;padding:14px 18px 6px}
@media(max-width:560px){.opts{grid-template-columns:repeat(3,1fr)}}
.opt{border:1.5px solid var(--line);border-radius:11px;padding:12px 0;font-size:17px;font-weight:700;
  color:var(--ink2);background:#fff;transition:.14s;text-align:center;font-variant-numeric:tabular-nums}
.opt:hover:not(:disabled){border-color:#a9c6e4;background:#f7fbff;color:var(--pri)}
.opt.sel{border-color:var(--pri2);background:var(--pri3);color:var(--pri)}
.opt.ok{border-color:#4aa87c;background:var(--green-bg);color:var(--green)}
.opt.bad{border-color:#d2776a;background:var(--red-bg);color:var(--red)}
.opt:disabled{cursor:default}

/* reference */
.tabs{display:flex;gap:8px;margin:0 0 16px;flex-wrap:wrap}
.tabs button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 15px;
  font-size:13px;cursor:pointer;color:var(--ink2);font-family:inherit}
.tabs button.on{background:var(--pri);border-color:var(--pri);color:#fff}
.ref-card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:15px 18px 16px;
  margin-bottom:12px;box-shadow:var(--sh);break-inside:avoid}
.ref-h{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:10px;
  padding-bottom:9px;border-bottom:1px solid var(--line2)}
.ref-id{font-size:12px;font-weight:800;color:#fff;background:var(--pri2);padding:2px 8px;
  border-radius:6px;letter-spacing:.03em}
.ref-en{font-size:15.5px;font-weight:700;color:var(--ink)}
.ref-zh{font-size:13px;color:var(--ink3)}
.ref-k{font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--ink4);
  margin:0 0 3px;font-weight:700}
.ref-focus{font-size:14px;margin:0 0 11px;color:var(--ink2)}
.ref-steps{margin:0 0 11px;padding-left:20px;font-size:13.8px;line-height:1.9;color:var(--ink)}
.ref-steps li{margin:1px 0}
.ref-note{font-size:13.4px;color:var(--ink2);background:var(--pri3);border-radius:10px;
  padding:9px 12px;margin:0 0 10px}
.ref-trap{font-size:13px;color:var(--red);background:var(--red-bg);
  border-left:3px solid var(--red);border-radius:0 8px 8px 0;padding:8px 12px}
.ref-trap b{color:var(--red)}
.sec-hd{display:flex;align-items:baseline;gap:10px;margin:22px 0 10px;padding-bottom:6px;
  border-bottom:2px solid var(--pri)}
.sec-hd .n{font-size:12px;color:#fff;background:var(--pri);padding:2px 8px;border-radius:6px;font-weight:700}
.sec-hd .t{font-size:16px;font-weight:700}
.sec-hd .s{font-size:12.5px;color:var(--ink3)}
.fbox{display:grid;grid-template-columns:1fr;gap:0}
@media(max-width:700px){.fbox{grid-template-columns:1fr}}
.frow{display:flex;gap:14px;justify-content:space-between;border-bottom:1px dotted var(--line);
  padding:6px 0;font-size:14px;align-items:baseline}
.frow>span:last-child{color:var(--ink3);text-align:right}
.gl{width:100%;border-collapse:collapse;font-size:13.5px}
.gl td{padding:7px 8px;border-bottom:1px solid var(--line2);vertical-align:top}
.gl td:nth-child(1){font-weight:700;width:32%}
.gl td:nth-child(2){color:var(--ink2);width:24%}
.gl td:nth-child(3){color:var(--ink3)}

/* feedback */
.fb{margin:12px 18px 18px;border-radius:12px;border:1px solid var(--line);overflow:hidden}
.fb.ok{border-color:var(--green-line);background:var(--green-bg)}
.fb.bad{border-color:var(--red-line);background:var(--red-bg)}
.fb .h{display:flex;align-items:center;gap:8px;padding:10px 14px;font-weight:700;font-size:14px}
.fb.ok .h{color:var(--green)}.fb.bad .h{color:var(--red)}
.fb .h .tag{font-size:11px;letter-spacing:.1em;text-transform:uppercase;background:rgba(255,255,255,.6);
  border-radius:100px;padding:1px 8px;font-weight:700}
.sol{padding:0 14px 15px}
.sol .col{font-size:14px;line-height:1.68;color:var(--ink2)}
.sol .col .lb{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink4);
  font-weight:700;margin-bottom:4px}
.sol .col+.col{margin-top:12px;padding-top:11px;border-top:1px dashed rgba(16,40,70,.16)}
.sol .zh{color:var(--ink);font-size:14px}
.sol .zh .lb{color:var(--ink3)}
.katex{font-size:1.02em}

/* results */
.res{max-width:760px;margin:22px auto 60px}
.bigscore{font-size:44px;font-weight:800;letter-spacing:-.03em;line-height:1}
.muted{color:var(--ink3);font-size:13px}
.pill{display:inline-block;font-size:12px;background:#f2f6fb;border:1px solid var(--line);
  border-radius:100px;padding:2px 10px;color:var(--ink2);margin:0 6px 6px 0}
.filter{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
.filter button{font-size:13px;padding:6px 13px;border-radius:100px;border:1px solid var(--line);
  background:#fff;color:var(--ink2)}
.filter button.on{background:var(--pri);color:#fff;border-color:var(--pri)}
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);
  background:rgba(16,24,39,.92);color:#fff;padding:10px 18px;border-radius:100px;font-size:13.5px;
  opacity:0;transition:.24s;z-index:99;pointer-events:none}
.toast.on{opacity:1;transform:translateX(-50%) translateY(0)}
</style>
</head>
<body>
<div class="top"><div class="wrap">
  <div class="brand"><div class="mark">26</div>
    <div>MTH026 <small>Calculus I · 674 items · 54 topics</small></div></div>
  <div class="spacer"></div>
  <button class="btn ghost" onclick="route('home')">Practice</button>
  <button class="btn ghost" onclick="route('ref')">Reference</button>
  <button class="btn ghost" onclick="route('browse')">Bank</button>
  <div class="chip" id="cAns">Answered <b>0</b></div>
  <div class="chip" id="cAcc">Accuracy <b>—</b></div>
  <div class="chip" id="cStreak">Streak <b>0</b></div>
  <button class="btn ghost" onclick="resetAll()">Reset</button>
</div></div>
<div id="view"></div>
<div class="toast" id="toast"></div>
<script>const DATA = __DATA__;</script>
<script src="katex/katex.min.js"></script>
<script src="katex/auto-render.min.js"></script>
<script>
const LS='mth026.en.v1';
const ITEMS = DATA.items, SECS = DATA.sections, CHS = DATA.chapters;
const PQ = DATA.pq || [];
const BYID = {}; ITEMS.forEach(q=>BYID[q.id]=q);
const SECMAP = {}; SECS.forEach(s=>SECMAP[s.id]=s);
PQ.forEach(p=>{ BYID[p.id]={id:p.id, s:p.s, c:p.c, p:p.p, pq:1}; });
const PQBYSEC = {}; PQ.forEach(p=>{ (PQBYSEC[p.s]=PQBYSEC[p.s]||[]).push(p.id); });
const TOTAL_PQ = PQ.length;
const REF = DATA.ref || [], FORMS = DATA.forms || [], GLOSS = DATA.gloss || [];
let store = {h:{}, fav:{}, streak:0, best:0};
try{ const raw=localStorage.getItem(LS); if(raw) store=Object.assign(store,JSON.parse(raw)); }catch(e){}
function save(){ try{localStorage.setItem(LS,JSON.stringify(store))}catch(e){} }

/* ---------- stats ---------- */
function secStat(id){
  const s=SECMAP[id]; let done=0, ok=0;
  for(let i=s.from;i<=s.to;i++){ const r=store.h[i]; if(r){done++; if(r.ok) ok++;} }
  return {done, ok, n:s.n, acc: done? ok/done : 0};
}
function overall(){
  // graded items only: the originals deck is self-marked and must not dilute
  // the accuracy figure the engine steers by
  const ks=Object.keys(store.h).filter(k=>+k<1000); let ok=0;
  ks.forEach(k=>{ if(store.h[k].ok) ok++; });
  return {done:ks.length, ok, acc: ks.length? ok/ks.length : 0};
}
function pqStat(){
  let done=0, ok=0;
  PQ.forEach(p=>{ const r=store.h[p.id]; if(r){done++; if(r.ok) ok++;} });
  return {done, ok, acc: done? ok/done : 0};
}
function paintTop(){
  const o=overall();
  document.getElementById('cAns').innerHTML='Answered <b>'+o.done+'</b>';
  document.getElementById('cAcc').innerHTML='Accuracy <b>'+(o.done? Math.round(o.acc*100)+'%':'—')+'</b>';
  document.getElementById('cStreak').innerHTML='Streak <b>'+store.streak+'</b>';
}
function toast(m){ const t=document.getElementById('toast'); t.textContent=m; t.classList.add('on');
  clearTimeout(t._t); t._t=setTimeout(()=>t.classList.remove('on'),1600); }
function resetAll(){ if(!confirm('Clear all progress?')) return;
  store={h:{},fav:{},streak:0,best:0}; save(); paintTop(); route('home'); }

/* ---------- smart engine ---------- */
function untouchedSecs(){
  return SECS.filter(s=>{
    for(let i=s.from;i<=s.to;i++) if(store.h[i]) return false;
    return true;
  });
}
function nextSmart(){
  // phase 1: one pass through every topic
  const un=untouchedSecs();
  if(un.length){
    const s=un[0];
    // the easiest unanswered item in that topic = first one
    for(let i=s.from;i<=s.to;i++) if(!store.h[i]) return i;
  }
  // phase 2: weakest topic first, prefer unseen then most-missed then stalest
  let best=null, bestScore=-1;
  for(const s of SECS){
    const st=secStat(s.id);
    const gap=1-st.acc;
    if(gap<=0) continue;
    // unseen item inside this topic
    let cand=null;
    for(let i=s.from;i<=s.to;i++){ if(!store.h[i]){ cand=i; break; } }
    if(cand===null){
      // most recently wrong / stalest
      let worst=null, wt=Infinity;
      for(let i=s.from;i<=s.to;i++){
        const r=store.h[i];
        if(!r.ok && (r.t||0)<wt){ wt=r.t||0; worst=i; }
      }
      cand=worst;
      if(cand===null){ // all correct: pick stalest
        let st2=Infinity;
        for(let i=s.from;i<=s.to;i++){ const t=store.h[i].t||0; if(t<st2){st2=t; cand=i;} }
      }
    }
    const score = gap*1000 + (1 - Math.min(st.done/st.n,1))*100;
    if(score>bestScore){ bestScore=score; best=cand; }
  }
  if(best!==null) return best;
  return ITEMS[Math.floor(Math.random()*ITEMS.length)].id;
}
function buildMock(n){
  const pool=[]; const per={};
  SECS.forEach(s=>per[s.id]=[]);
  ITEMS.forEach(q=>per[q.s].push(q.id));
  const ids=Object.keys(per);
  let i=0;
  while(pool.length<n && i<n*30){
    const s=ids[Math.floor(Math.random()*ids.length)];
    if(!per[s].length) { i++; continue; }
    const k=Math.floor(Math.random()*per[s].length);
    pool.push(per[s].splice(k,1)[0]); i++;
  }
  return pool;
}
function wrongQueue(){
  return Object.keys(store.h).filter(k=>!store.h[k].ok).map(Number)
    .sort((a,b)=>(store.h[a].t||0)-(store.h[b].t||0));
}

/* ---------- routing ---------- */
let round={list:[],i:0,mode:'smart',picked:null,done:false,t0:0};
function route(v,arg){ window.scrollTo(0,0);
  if(v==='home') viewHome(); else if(v==='quiz') viewQuiz();
  else if(v==='res') viewRes(); else if(v==='browse') viewBrowse(arg||'all');
  else if(v==='ref') viewRef(arg);
  paintTop();
}
function start(mode){
  let list=[];
  if(mode==='smart') list=[nextSmart()];
  else if(mode==='mock') list=buildMock(20);
  else if(mode==='wrong') list=wrongQueue();
  else if(mode==='pq'){ startPq(10); return; }
  if(!list.length){ toast('Nothing to review — all clear.'); return; }
  round={list, i:0, mode, picked:null, done:false, t0:Date.now(), ok:0, ans:0};
  route('quiz');
}
function startPq(n){
  // same weighting as the smart engine: weakest topic first, unseen item first
  const rank = SECS.map(s=>{ const st=secStat(s.id); return {id:s.id, gap: st.done? 1-st.acc : 1.45}; })
                   .filter(r=>PQBYSEC[r.id] && PQBYSEC[r.id].length)
                   .sort((a,b)=>b.gap-a.gap);
  const out=[];
  for(const r of rank){
    const pool = PQBYSEC[r.id].slice().sort((a,b)=> (store.h[a]?1:0)-(store.h[b]?1:0));
    for(const id of pool){ if(out.length<(n||10)) out.push(id); }
    if(out.length>=(n||10)) break;
  }
  if(!out.length){ toast('No originals left in this deck.'); return; }
  round={list:out, i:0, mode:'pq', picked:null, done:false, t0:Date.now()};
  route('quiz');
}
function startTopicPq(id){
  const list=(PQBYSEC[id]||[]).slice().sort((a,b)=>(store.h[a]?1:0)-(store.h[b]?1:0)).slice(0,12);
  if(!list.length){ toast('That topic was never served as a quiz item.'); return; }
  round={list, i:0, mode:'pq', picked:null, done:false, t0:Date.now()};
  route('quiz');
}
function startTopic(id){
  const s=SECMAP[id]; const list=[];
  for(let i=s.from;i<=s.to;i++) list.push(i);
  round={list, i:0, mode:'topic', picked:null, done:false, t0:Date.now(), ok:0, ans:0};
  route('quiz');
}

/* ---------- views ---------- */
function viewHome(){
  const o=overall();
  const pq=pqStat();
  const un=untouchedSecs().length;
  const wrong=wrongQueue().length;
  const nextId=nextSmart();
  const rows = SECS.map(s=>{
    const st=secStat(s.id);
    const pct=Math.round(st.acc*100);
    const cls= st.done===0? '' : (pct>=80?'ok':(pct>=50?'warn':'bad'));
    return '<div class="sec-row" onclick="startTopic(\''+s.id+'\')" style="cursor:pointer">'
      +'<span class="sec-id">'+s.id+'</span>'
      +'<span class="sec-t">'+s.en+(PQBYSEC[s.id]
          ? ' <span class="pill" style="font-size:11px;padding:1px 7px" '
            +'onclick="event.stopPropagation();startTopicPq(\''+s.id+'\')">'+PQBYSEC[s.id].length+'P</span>' : '')
      +'</span>'
      +'<span class="bar"><i class="'+cls+'" style="width:'+(st.done? Math.max(pct,6):0)+'%"></i></span>'
      +'<span class="sec-n">'+st.done+'/'+st.n+'</span></div>';
  }).join('');
  document.getElementById('view').innerHTML = `
  <div class="wrap">
    <div class="hero">
      <h1>${o.done===0? 'Start where it matters' : 'Keep the streak alive'}</h1>
      <p>${o.done===0
        ? 'The engine walks you through <b>one question from every topic first</b>, then re-weights towards whatever you keep missing. No setup needed.'
        : 'You have answered <b>'+o.done+'</b> of 351 items at <b>'+Math.round(o.acc*100)+'%</b>. Topics untouched: '+un+'.'}</p>
      <div class="row">
        <button class="btn white" onclick="start('smart')">${o.done? 'Continue smart round':'Start smart round'}</button>
        <button class="btn light" onclick="start('mock')">Mock test · 20</button>
        <button class="btn light" onclick="start('pq')">Quiz originals · 10</button>
        <button class="btn light" onclick="route('browse')">Browse all 351</button>
      </div>
    </div>
    <div class="card click" onclick="start('pq')" style="display:flex;align-items:center;gap:18px;margin-bottom:18px;flex-wrap:wrap">
      <div style="min-width:120px"><div class="k">From your practice quizzes</div>
        <div class="stat" style="font-size:26px">${pq.done}<small>/ ${TOTAL_PQ}</small></div></div>
      <div style="flex:1;min-width:240px">
        <p style="margin:0 0 4px"><b>The 323 items you were actually served</b> — question, the paper's own
        “Answer:” line and its printed solution, all page crops.</p>
        <p class="muted" style="margin:0">Numbers are randomised per attempt, so no letter can be recovered from the
        page. Pick a letter, compare it with the printed answer, then mark yourself —
        ${pq.done? 'accuracy so far '+Math.round(pq.acc*100)+'%' : 'nothing marked yet'}.</p>
      </div>
      <div><button class="btn pri">Open a set of 10</button></div>
    </div>
    <div class="grid g3" style="margin-bottom:18px">
      <div class="card"><div class="k">Progress</div><div class="stat">${o.done}<small>/ 351</small></div>
        <p>${un===0? 'Every topic has been started.' : un+' topics not started yet.'}</p></div>
      <div class="card"><div class="k">Accuracy</div><div class="stat">${o.done? Math.round(o.acc*100)+'%':'—'}</div>
        <p>${o.ok} correct out of ${o.done} answered.</p></div>
      <div class="card click" onclick="${wrong? "start('wrong')":"toast('No mistakes recorded yet.')"}">
        <div class="k">Review</div><div class="stat">${wrong}</div>
        <p>${wrong? 'Questions you got wrong — tap to drill them.':'Nothing to repair yet.'}</p></div>
    </div>
    <div class="card" style="padding:16px 20px 6px">
      <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:6px">
        <h3 style="margin:0">Topic mastery</h3>
        <span class="muted">click a topic to drill it</span>
        <div class="spacer" style="flex:1"></div>
        <span class="muted">answered</span>
      </div>
      ${rows}
    </div>
    <p class="muted" style="margin:18px 0 40px;text-align:center">
      Progress is stored in this browser only. Questions are the original page crops — nothing is re-typed.</p>
  </div>`;
}

function viewQuiz(){
  if(round.i>=round.list.length){ round.done=true; return viewRes(); }
  const id=round.list[round.i], q=BYID[id];
  if(q && q.pq) return viewPq();
  const rec=store.h[id];
  const solo = round.mode==='smart' && round.list.length===1;
  const covered = SECS.length - untouchedSecs().length;
  const pct = solo ? Math.round(covered/SECS.length*100)
                   : Math.round(((round.i)/round.list.length)*100);
  const progLabel = solo
    ? (untouchedSecs().length? 'Phase 1 · ' : 'Phase 2 · ') + covered + '/' + SECS.length + ' topics'
    : (round.i+1) + '/' + round.list.length;
  const letters=['A','B','C','D','E'];
  const picked = round.picked;
  const shown = picked!==null;
  const fb = shown ? `
    <div class="fb ${picked===q.a?'ok':'bad'}">
      <div class="h">${picked===q.a? 'Correct' : 'Not quite'} <span class="tag">answer ${q.a}</span></div>
      <div class="sol">
        <div class="col"><div class="lb">Solution</div>${q.en}</div>
        <div class="col zh"><div class="lb">中文解析</div>${q.zh}</div>
      </div>
    </div>` : '';
  document.getElementById('view').innerHTML = `
  <div class="wrap"><div class="qwrap">
    <div class="qcard">
      <div class="qhead">
        <span class="qno">Q${q.id}</span><span class="qsec">${q.s} · ${SECMAP[q.s].en}</span>
        <div class="qprog"><span class="muted" style="font-size:12px">${progLabel}</span>
          <span class="track"><i style="width:${pct}%"></i></span></div>
      </div>
      <div class="qbody"><img class="qimg" src="q/q${String(q.id).padStart(3,'0')}.png" alt="Question ${q.id}"></div>
      <div class="opts">${letters.map(L=>{
        let cls='opt';
        if(shown){ if(L===q.a) cls+=' ok'; else if(L===picked) cls+=' bad'; }
        return `<button class="${cls}" ${shown?'disabled':''} onclick="pick('${L}')">${L}</button>`;
      }).join('')}</div>
      ${fb}
    </div>
    <div style="display:flex;gap:10px;margin-top:14px;align-items:center">
      <button class="btn ghost" onclick="route('home')">Exit</button>
      <div class="spacer" style="flex:1"></div>
      ${shown? (solo
        ? `<button class="btn pri" onclick="start('smart')">Next question &rarr;</button>`
        : `<button class="btn pri" onclick="advance()">${round.i+1>=round.list.length?'See results':'Next question'}</button>`):''}
    </div>
    <p class="muted" style="text-align:center;margin-top:14px">Pick a letter. The full worked solution appears straight after.</p>
  </div></div>`;
  paintTop();
}

function pick(L){
  if(round.picked!==null) return;
  const q=BYID[round.list[round.i]];
  round.picked=L;
  const ok = L===q.a;
  store.h[q.id]={a:L, ok, t:Date.now()};
  if(ok){ store.streak++; if(store.streak>store.best) store.best=store.streak; }
  else store.streak=0;
  save(); viewQuiz(); renderMath();
  const fb = document.querySelector('.fb');
  if(fb && fb.getBoundingClientRect().bottom > innerHeight - 8){
    fb.scrollIntoView({block:'nearest', behavior:'smooth'});
  }
}
function advance(){
  round.i++; round.picked=null;
  if(round.i>=round.list.length) return viewRes();
  viewQuiz(); renderMath();
}

/* ---------- Part B: the items you were served (self-marked) ---------- */
function viewPq(){
  const id=round.list[round.i], q=BYID[id];
  const p=String(q.p).padStart(3,'0');
  const picked=round.picked, shown=picked!==null;
  const letters=['A','B','C','D','E'];
  const opts = letters.map(L=>{
    let cls='opt';
    if(shown && L===picked) cls+=' sel';
    return `<button class="${cls}" ${shown?'disabled':''} onclick="pickPq('${L}')">${L}</button>`;
  }).join('');
  const reveal = shown ? `
    <div class="fb" style="background:#fffdf8;border-color:#e7dcc6">
      <div class="h" style="color:#8a5a12">Answer, as printed <span class="tag">you picked ${picked}</span></div>
      <div style="padding:2px 14px 0">
        <a href="pq/p${p}_a.jpg" target="_blank" title="Open full size">
          <img src="pq/p${p}_a.jpg" alt="Answer" style="display:block;max-height:74px;max-width:100%;width:auto"></a></div>
      <div class="h" style="color:#8a5a12;padding-top:12px">Their worked solution
        <span class="tag" style="background:#f3ece0;color:#8a7550">tap to zoom</span></div>
      <div style="padding:2px 14px 14px">
        <a href="pq/p${p}_s.jpg" target="_blank" title="Open full size">
          <img class="qimg" src="pq/p${p}_s.jpg" alt="Solution"></a></div>
      <div style="display:flex;gap:10px;padding:0 14px 16px">
        <button class="btn pri" onclick="gradePq(1)">My pick was right</button>
        <button class="btn ghost" onclick="gradePq(0)">I missed it</button>
      </div>
    </div>` : '';
  document.getElementById('view').innerHTML = `
  <div class="wrap"><div class="qwrap">
    <div class="qcard">
      <div class="qhead">
        <span class="qno" style="background:#9a6a1c">P${q.p}</span>
        <span class="qsec">${q.s} · ${SECMAP[q.s].en}</span>
        <div class="qprog"><span class="muted" style="font-size:12px">Originals · ${round.i+1}/${round.list.length}</span>
          <span class="track"><i style="width:${Math.round(round.i/round.list.length*100)}%"></i></span></div>
      </div>
      <div class="qbody"><img class="qimg" src="pq/p${p}_q.jpg" alt="Question"></div>
      <div class="opts">${opts}</div>
      ${reveal}
    </div>
    <div style="display:flex;gap:10px;margin-top:14px;align-items:center">
      <button class="btn ghost" onclick="route('home')">Exit</button>
      <div class="spacer" style="flex:1"></div>
      ${shown? `<button class="btn ghost" onclick="advance()">${round.i+1>=round.list.length?'Skip to results':'Skip'}</button>`:''}
    </div>
    <p class="muted" style="text-align:center;margin-top:14px">${shown
      ? 'Compare with the printed answer, then mark your own attempt.'
      : 'Pick the letter you would have chosen. Nothing is scored until you mark it.'}</p>
  </div></div>`;
  paintTop();
}
function pickPq(L){
  if(round.picked!==null) return;
  round.picked=L;
  viewQuiz(); renderMath();
  const fb=document.querySelector('.fb');
  if(fb && fb.getBoundingClientRect().top > innerHeight-120) fb.scrollIntoView({block:'center',behavior:'smooth'});
}
function gradePq(ok){
  const q=BYID[round.list[round.i]];
  store.h[q.id]={a:round.picked, ok:!!ok, t:Date.now(), self:1};
  if(ok){ store.streak++; if(store.streak>store.best) store.best=store.streak; }
  else store.streak=0;
  save(); advance();
}

function viewRes(){
  const total=round.list.length;
  let ok=0, rows='';
  if(round.mode==='mock'){
    const bySec={};
    round.list.forEach(id=>{ const q=BYID[id]; const r=store.h[id];
      bySec[q.s]=bySec[q.s]||{n:0,ok:0}; bySec[q.s].n++; if(r&&r.ok) bySec[q.s].ok++; });
    rows=Object.keys(bySec).map(s=>{
      const b=bySec[s]; const p=Math.round(b.ok/b.n*100);
      return {s, b, p};
    }).sort((a,b)=>a.p-b.p).map(r=>{
      const s=r.s, b=r.b, p=r.p;
      return '<div class="sec-row"><span class="sec-id">'+s+'</span><span class="sec-t">'+SECMAP[s].en+'</span>'
        +'<span class="bar"><i class="'+(p>=80?'ok':(p>=50?'warn':'bad'))+'" style="width:'+Math.max(p,6)+'%"></i></span>'
        +'<span class="sec-n">'+b.ok+'/'+b.n+'</span></div>';
    }).join('');
  }
  total && round.list.forEach(id=>{ if(store.h[id]&&store.h[id].ok) ok++; });
  const pct= total? Math.round(ok/total*100):0;
  document.getElementById('view').innerHTML=`
  <div class="wrap"><div class="res">
    <div class="card" style="text-align:center;padding:30px 24px">
      <div class="k">${round.mode==='mock'?'Mock test complete':(round.mode==='wrong'?'Repair round complete':(round.mode==='pq'?'Originals round complete':'Round complete'))}</div>
      <div class="bigscore">${pct}%</div>
      <p class="muted" style="margin-top:6px">${ok} of ${total} correct${round.mode==='mock'?' · 20-item mock':' · this round'}</p>
      ${total? `<p style="margin-top:10px">${round.list.map(id=>{
          const r=store.h[id]; const nm = id>=1000? 'P'+(id-1000) : 'Q'+id;
          return `<span class="pill">${nm} ${r&&r.ok?'✓':'✕'}</span>`;}).join('')}</p>`:''}
    </div>
    ${rows? '<div class="card" style="margin-top:14px"><h3>By topic</h3>'+rows+'</div>':''}
    <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap">
      <button class="btn pri" onclick="start('${round.mode==='pq'?'pq':'smart'}')">${round.mode==='pq'?'Another set of 10':'Continue smart round'}</button>
      <button class="btn ghost" onclick="start('wrong')">Drill my mistakes</button>
      <button class="btn ghost" onclick="route('home')">Back to overview</button>
    </div>
  </div></div>`;
  paintTop();
}

let browseCh='all';
let refTab='topics', refCh='all';
function viewRef(tab, ch){
  if(tab) refTab=tab;
  if(ch!==undefined) refCh=ch;
  const tabs = [['topics','Topics '+REF.length],['forms','Formula sheet'],['gloss','Terminology']]
    .map(p=>`<button class="${refTab===p[0]?'on':''}" onclick="viewRef('${p[0]}')">${p[1]}</button>`).join('');
  let body='';
  if(refTab==='topics'){
    const chips = [`<button class="${refCh==='all'?'on':''}" onclick="viewRef('topics','all')">All chapters</button>`]
      .concat(CHS.map((c,i)=>`<button class="${refCh===i?'on':''}" onclick="viewRef('topics',${i})">Ch ${i+1}</button>`)).join('');
    body = `<div class="tabs">${chips}</div>` + CHS.map((c,i)=>{
      if(refCh!=='all' && refCh!==i) return '';
      const list = REF.filter(r=>r.c===i);
      if(!list.length) return '';
      return `<div class="sec-hd"><span class="n">Ch ${i+1}</span><span class="t">${c.en}</span><span class="s">${c.zh}</span></div>`
        + list.map(r=>`<div class="ref-card" id="r${r.id}">
            <div class="ref-h"><span class="ref-id">${r.id}</span><span class="ref-en">${r.en}</span>
              <span class="ref-zh">${r.zh}</span></div>
            <div class="ref-k">What it tests</div><p class="ref-focus">${r.focus}</p>
            <div class="ref-k">How to do it</div><ol class="ref-steps">${r.steps.map(s=>`<li>${s}</li>`).join('')}</ol>
            ${r.note? `<p class="ref-note">${r.note}</p>`:''}
            ${r.trap? `<div class="ref-trap"><b>Trap</b> &middot; ${r.trap}</div>`:''}
            <div style="margin-top:11px;display:flex;gap:8px;flex-wrap:wrap">
              <button class="btn ghost" onclick="startTopic('${r.id}')">Drill ${r.n} items</button>
              ${PQBYSEC[r.id]? `<button class="btn ghost" onclick="startTopicPq('${r.id}')">${PQBYSEC[r.id].length} originals</button>`:''}
            </div></div>`).join('');
    }).join('');
  } else if(refTab==='forms'){
    body = FORMS.map(g=>`<div class="sec-hd"><span class="t">${g.name}</span></div>
      <div class="card"><div class="fbox">${g.rows.map(([a,b])=>
        `<div class="frow"><span>$${a}$</span><span>$${b}$</span></div>`).join('')}</div></div>`).join('');
  } else {
    body = GLOSS.map(g=>`<div class="sec-hd"><span class="t">${g.g}</span><span class="s">${g.gz}</span></div>
      <div class="card" style="padding:4px 16px"><table class="gl">${g.items.map(([a,b,c])=>
        `<tr><td>${a}</td><td>${b}</td><td>${c}</td></tr>`).join('')}</table></div>`).join('');
  }
  document.getElementById('view').innerHTML = `
  <div class="wrap">
    <div style="display:flex;align-items:baseline;gap:12px;margin:26px 0 14px;flex-wrap:wrap">
      <h2 style="margin:0;font-size:22px">Reference</h2>
      <span class="muted">method &middot; steps &middot; trap for every topic, plus the formula sheet and terminology</span></div>
    <div class="tabs">${tabs}</div>
    ${body}
    <p class="muted" style="margin:22px 0 40px;text-align:center">
      Same content as the printed knowledge map — this page needs no network and no other file.</p>
  </div>`;
  paintTop(); renderMath();
}
function viewBrowse(ch){
  if(ch!==undefined) browseCh=ch;
  const filters = ['<button class="'+(browseCh==='all'?'on':'')+'" onclick="viewBrowse(\'all\')">All chapters</button>']
    .concat(CHS.map((c,i)=>`<button class="${browseCh==i?'on':''}" onclick="viewBrowse(${i})">Ch ${i+1}</button>`)).join('');
  const list = ITEMS.filter(q=>browseCh==='all'||q.c===browseCh).map(q=>{
    const r=store.h[q.id];
    const mark = r? (r.ok? '<span style="color:#1d6b47;font-weight:700">✓</span>':'<span style="color:#a8352a;font-weight:700">✕</span>') : '';
    return `<button class="pill" style="cursor:pointer" onclick="startSingle(${q.id})">Q${q.id} &nbsp;<span style="color:#96a3b4">${q.s}</span> ${mark}</button>`;
  }).join('');
  document.getElementById('view').innerHTML=`
  <div class="wrap"><div class="res">
    <div class="card">
      <h3 style="margin-bottom:2px">Browse the bank</h3>
      <p class="muted">Tap any item to open it on its own. ${ITEMS.length} items, 54 topics.</p>
      <div class="filter">${filters}</div>
      <div style="max-height:62vh;overflow:auto;line-height:2.4">${list}</div>
    </div>
    <div style="margin-top:14px"><button class="btn ghost" onclick="route('home')">Back</button></div>
  </div></div>`;
  paintTop();
}
function startSingle(id){
  round={list:[id], i:0, mode:'single', picked:null, done:false, t0:Date.now()};
  route('quiz');
}

/* math render */
function renderMath(){
  if(window.renderMathInElement){
    renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},
      {left:'$',right:'$',display:false}],throwOnError:false,strict:false});
  }
}
const _route=route;
route=function(v,a){ _route(v,a); renderMath(); };

document.addEventListener('keydown',e=>{
  const L=['a','b','c','d','e'], k=e.key.toLowerCase();
  if(L.includes(k)){ const b=[...document.querySelectorAll('.opt')][L.indexOf(k)];
    if(b&&!b.disabled) b.click(); }
  if(e.key==='Enter'){ const n=[...document.querySelectorAll('.btn.pri')].pop(); if(n) n.click(); }
});
paintTop(); viewHome(); renderMath();
if(location.hash==='#pq') start('pq');
else if(location.hash==='#ref') route('ref');
else if(location.hash==='#bank') route('browse');
</script>
</body>
</html>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    qd = os.path.join(OUT, "q")
    if os.path.isdir(qd):
        shutil.rmtree(qd)
    shutil.copytree(QSRC, qd)
    # Part B images: same crops as the book, re-encoded for the browser
    pd = os.path.join(OUT, "pq")
    if os.path.isdir(pd):
        shutil.rmtree(pd)
    os.makedirs(pd)
    from PIL import Image
    src = os.path.join(ROOT, "qbank", "p")
    n = 0
    for it in PIT:
        for suf in "qas":
            f = os.path.join(src, "p%03d_%s.png" % (it["pid"], suf))
            if not os.path.exists(f):
                continue
            im = Image.open(f).convert("RGB")
            if im.width > 1100:
                im = im.resize((1100, round(im.height * 1100.0 / im.width)), Image.LANCZOS)
            im.save(os.path.join(pd, "p%03d_%s.jpg" % (it["pid"], suf)), quality=88, optimize=True)
            n += 1
    print("pq images", n)
    kd = os.path.join(OUT, "katex")
    if os.path.isdir(kd):
        shutil.rmtree(kd)
    os.makedirs(kd)
    for f in ("katex.min.css", "katex.min.js", "auto-render.min.js"):
        shutil.copy(os.path.join(ASSETS, f), os.path.join(kd, f))
    shutil.copytree(os.path.join(ASSETS, "fonts"), os.path.join(kd, "fonts"))
    data = json.dumps(build_data(), ensure_ascii=False, separators=(",", ":"))
    html = HTML.replace("__DATA__", data)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    print("items", len(data and json.loads(data)["items"]), "->", os.path.join(OUT, "index.html"))


if __name__ == "__main__":
    main()
