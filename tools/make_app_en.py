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
# Part B answer letters, recovered offline from the Moodle review line
# "The correct answer is:" (matched against the five option blocks by their
# three-line fraction structure).  321 of 323; the two missing were never
# answered, so the paper prints no correct answer for them.
PANSW = os.path.join(ROOT, "build", "panswers.json")
PANS = json.load(open(PANSW))["answers"] if os.path.exists(PANSW) else {}

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
    # Every item now carries its answer letter, recovered from the paper's own
    # "The correct answer is:" line, so the app can mark Part B automatically
    # instead of asking the reader to grade their own pick.  Two items (p31,
    # p63) were never answered on the paper and therefore print no correct
    # answer; they keep a null letter and fall back to self-marking.
    pqch = {s["id"]: s["ch"] for s in SECTIONS}
    pq = [{"id": 1000 + it["pid"], "s": it["sec"], "c": pqch.get(it["sec"], 0),
           "p": it["pid"], "a": PANS.get(str(it["pid"]))} for it in PIT]
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
  --amber:#98621a; --amber-bg:#fdf7ec; --gold:#c8922e;
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
.brand{display:flex;align-items:center;gap:10px;font-weight:700;white-space:nowrap;min-width:0;flex:0 0 auto}
.brand .mark{width:26px;height:26px;border-radius:8px;background:linear-gradient(135deg,#16406e,#2c6ba8);
  color:#fff;display:grid;place-items:center;font-size:10px;font-weight:800;letter-spacing:.03em}
.brand small{display:block;font-size:10.5px;color:var(--ink3);font-weight:500;letter-spacing:.08em;text-transform:uppercase;
  overflow:hidden;text-overflow:ellipsis;max-width:100%}
.brand>div:last-child{min-width:0;overflow:hidden}
.spacer{flex:1}
.chip{display:inline-flex;align-items:center;gap:6px;background:#fff;border:1px solid var(--line);
  border-radius:100px;padding:5px 11px;font-size:12.5px;color:var(--ink2);white-space:nowrap}
.chip b{color:var(--ink);font-variant-numeric:tabular-nums}
.btn{border-radius:10px;padding:9px 16px;font-size:14px;font-weight:600;transition:.16s;white-space:nowrap}
.btn.pri{background:var(--pri);color:#fff;box-shadow:0 1px 2px rgba(22,64,110,.3)}
.btn.pri:hover{background:#12365e}
.btn.ghost{background:#fff;border:1px solid var(--line);color:var(--ink2)}
.btn.ghost:hover{border-color:#c9d5e3;background:#fafcfe}
.btn:disabled{opacity:.45;cursor:not-allowed}
/* the bar carries a lot of chrome; drop the least important chips first */
@media(max-width:1300px){#cStreak{display:none}}
@media(max-width:1080px){.brand small{display:none}}
@media(max-width:1010px){#cAns,#cAcc{display:none}}
@media(max-width:860px){.top .wrap{gap:8px}.brand>div{font-size:13.5px}}
@media(max-width:560px){#acctName{display:none}#btnAcct{padding:9px 11px}
  .brand>div{display:none}.top .wrap{gap:6px}
  .top .btn.ghost{font-size:13px;padding:8px 11px}}
@media(max-width:520px){#btnReset,.brand{display:none}}

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
.sec-n{font-size:12px;color:var(--ink3);font-variant-numeric:tabular-nums;width:96px;text-align:right;flex:0 0 auto}
.sec-n .miss{color:var(--red);font-weight:700;font-size:11px;margin-left:3px}

/* bilingual labels: English stays primary, Chinese rides along in grey */
.zhx,.tz{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  font-size:11.5px;font-weight:500;letter-spacing:0;color:var(--ink4)}
.sec-t .tz{margin-left:6px;font-size:11.5px}
.k .zhx{margin-left:5px;text-transform:none;letter-spacing:0;font-size:11px}
.btn .zhx{margin-left:4px;font-size:11px;opacity:.7;color:inherit}
@media(max-width:1320px){.navz{display:none}}
.hero .zh{color:#bdd3ea;font-size:13px;margin-top:8px;max-width:58ch;
  font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
.hero .zh b{color:#fff}

/* engine status strip */
.eng{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:#fff;border:1px solid var(--line);
  border-left:3px solid var(--pri2);border-radius:12px;padding:10px 15px;margin:0 0 18px;font-size:12.5px;
  color:var(--ink2);box-shadow:var(--sh)}
.eng b{color:var(--ink);font-variant-numeric:tabular-nums}
.eng .sep{color:var(--line);font-size:14px}
.eng .zhx{font-size:11.5px}
.eng .lnk{font-size:12px;color:var(--pri2);text-decoration:underline;text-underline-offset:2px}
.why{display:flex;align-items:flex-start;gap:8px;background:#f7fafd;border:1px dashed #cfdcea;
  border-radius:10px;padding:8px 12px;margin:0 0 12px;font-size:12.5px;color:var(--ink2);line-height:1.5}
.why .tag{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--pri2);font-weight:700;flex:0 0 auto}
@media(max-width:640px){
  .sec-t{white-space:normal;line-height:1.45;font-size:13px}
  .sec-t .tz{display:inline;margin-left:5px;font-size:11px}
  .sec-n{width:74px;font-size:11.5px}
  .bar{width:76px}
  .sec-row{padding:10px 0}
}

/* quiz */
.qwrap{max-width:760px;margin:22px auto 60px;min-height:calc(100vh - 190px);display:flex;flex-direction:column;justify-content:center}
.qwrap>*{flex:0 0 auto}
.qcard{background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:var(--sh2);overflow:hidden}
.qhead{display:flex;align-items:center;gap:10px;padding:12px 18px;background:#f7fafd;border-bottom:1px solid var(--line)}
.qno{font-size:12px;font-weight:700;color:#fff;background:var(--pri2);border-radius:6px;padding:2px 9px;flex:0 0 auto}
.qsec{font-size:12px;color:var(--ink3);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.qprog{margin-left:auto;display:flex;align-items:center;gap:8px;flex:0 0 auto;white-space:nowrap}
@media(max-width:760px){.qprog .track{display:none}}
.qprog .track{width:96px;height:6px;background:#e7edf4;border-radius:100px;overflow:hidden}
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
/* unified item index */
.idxsearch{margin:2px 0 10px}
.idxsearch input{width:100%;max-width:440px;font:inherit;font-size:13.5px;padding:9px 13px;
  border:1px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);outline:none}
.idxsearch input:focus{border-color:#a9c6e4;box-shadow:0 0 0 3px rgba(44,107,168,.10)}
.idxmeta{font-size:12px;color:var(--ink3);margin:0 0 10px;font-variant-numeric:tabular-nums}
.idxgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(76px,1fr));gap:7px;
  max-height:58vh;overflow:auto;padding:2px}
.idx-b{display:flex;flex-direction:column;align-items:flex-start;position:relative;border:1px solid var(--line);
  background:#fff;border-radius:9px;padding:6px 9px;font-variant-numeric:tabular-nums;transition:.14s}
.idx-b b{font-size:13px;font-weight:700;color:var(--ink2);line-height:1.3}
.idx-b i{font-size:10px;color:var(--ink4);font-style:normal;line-height:1.2}
.idx-b u{position:absolute;right:7px;top:5px;font-size:10px;text-decoration:none}
.idx-b.p b{color:#8a5a12}
.idx-b:hover{border-color:#a9c6e4;background:#f7fbff}
.idx-b.ok{border-color:var(--green-line);background:var(--green-bg)}
.idx-b.ok u{color:var(--green)}
.idx-b.bad{border-color:var(--red-line);background:var(--red-bg)}
.idx-b.bad u{color:var(--red)}

/* account */
.dot{width:7px;height:7px;border-radius:50%;background:#c3ccd8;display:inline-block;flex:0 0 auto}
.dot.on{background:#2f9e6b}.dot.err{background:#cf5b4a}
.modal{position:fixed;inset:0;background:rgba(12,22,36,.42);display:none;z-index:80;
  align-items:center;justify-content:center;padding:20px}
.modal.on{display:flex}
.mbox{background:#fff;border-radius:18px;box-shadow:var(--sh2);width:100%;max-width:404px;padding:22px 24px 20px;
  max-height:88vh;overflow:auto}
.mhd{display:flex;align-items:flex-start;gap:10px}
.mhd h3{margin:0;font-size:17px}
.mhd .x{margin-left:auto;font-size:14px;color:var(--ink3);padding:2px 7px;border-radius:8px;line-height:1.4}
.mhd .x:hover{background:#f2f6fb}
.mtabs{display:flex;gap:8px;margin:14px 0 14px}
.mtabs button{flex:1;padding:8px 0;font-size:13.5px;border-radius:9px;border:1px solid var(--line);
  background:#fff;color:var(--ink2)}
.mtabs button.on{background:var(--pri3);border-color:#bcd2e8;color:var(--pri);font-weight:700}
.fld{margin-bottom:11px}
.fld label{display:block;font-size:12px;color:var(--ink3);margin-bottom:4px;font-weight:600}
.fld input{width:100%;font:inherit;font-size:14px;padding:9px 12px;border:1px solid var(--line);
  border-radius:9px;outline:none;background:#fff;color:var(--ink)}
.fld input:focus{border-color:#a9c6e4;box-shadow:0 0 0 3px rgba(44,107,168,.10)}
.merr{font-size:12.5px;color:var(--red);background:var(--red-bg);border-radius:8px;padding:7px 11px;margin:0 0 11px}
.mnote{font-size:12px;color:var(--ink3);margin:12px 0 0;line-height:1.6}
.who{display:flex;align-items:center;gap:12px;margin:14px 0 16px}
.who .av{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#16406e,#2c6ba8);
  color:#fff;display:grid;place-items:center;font-weight:800;font-size:16px;flex:0 0 auto}
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);
  background:rgba(16,24,39,.92);color:#fff;padding:10px 18px;border-radius:100px;font-size:13.5px;
  opacity:0;transition:.24s;z-index:99;pointer-events:none}
.toast.on{opacity:1;transform:translateX(-50%) translateY(0)}

/* star / favourites */
.star{flex:0 0 auto;width:30px;height:30px;display:inline-flex;align-items:center;justify-content:center;
  font-size:18px;line-height:1;color:var(--ink4);border:1px solid var(--line);border-radius:9px;
  background:#fff;padding:0;transition:.14s}
.star:hover{border-color:var(--gold);color:var(--gold);background:#fffaf0}
.star.on{color:var(--gold);border-color:#e6cf9c;background:#fff8e8}
.qhead>.star{margin-left:auto}
.qhead>.star+.qprog{margin-left:8px}
.btn.ic{padding:9px 12px;font-size:15px;flex:0 0 auto}
.btn.ic .zhx{font-size:11px;margin-left:4px}
@media(max-width:1320px){#btnFav .zhx{display:none}}
@media(max-width:560px){.btn.ic{padding:8px 9px;font-size:14px}#btnFav{padding:8px 9px}}

/* preview + favourites board */
.pv-hd2{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:24px 0 4px}
.pv-hd2 h2{margin:0;font-size:22px}
.pv-sub{color:var(--ink3);font-size:13px;margin:0 0 14px}
.pv-tools{display:flex;gap:9px;flex-wrap:wrap;align-items:center;margin:0 0 12px}
.pv-grid{max-height:180px}
.pv-count{font-size:12px;color:var(--ink3);margin:0 0 8px;font-variant-numeric:tabular-nums}
.pv-cards{display:grid;grid-template-columns:1fr;gap:14px;margin:14px 0}
.pv-card{background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:var(--sh);
  overflow:hidden;scroll-margin-top:78px}
.pv-card.hl{border-color:var(--gold);box-shadow:0 0 0 3px rgba(200,146,46,.28),var(--sh2)}
.pv-hd{display:flex;align-items:center;gap:9px;padding:10px 14px;background:#f7fafd;
  border-bottom:1px solid var(--line);flex-wrap:wrap}
.pv-hd .qno{flex:0 0 auto}
.qno.pq{background:#9a6a1c}
.pv-sec{font-size:12.5px;color:var(--ink2);min-width:0;flex:1 1 auto;overflow:hidden;
  text-overflow:ellipsis;white-space:nowrap}
.pv-done{font-size:11.5px;color:var(--ink4);flex:0 0 auto;white-space:nowrap}
.pv-done.ok{color:var(--green)}.pv-done.bad{color:var(--red)}
.pv-img{padding:12px 14px 2px}
.pv-img img{display:block;width:100%;height:auto;border-radius:8px}
.pv-ans{margin:10px 14px 0;background:var(--green-bg);border:1px solid var(--green-line);
  border-radius:10px;padding:9px 13px;font-size:14px;color:var(--green);font-weight:700}
.pv-ans b{font-size:16px}
.pv-note{margin:10px 14px 0;font-size:12px;color:var(--amber);background:var(--amber-bg);
  border-radius:9px;padding:7px 11px}
.pv-aimg,.pv-simg{margin:10px 14px 0}
.pv-aimg img{display:block;max-width:100%;max-height:74px;width:auto;height:auto;border-radius:6px}
.pv-simg img{display:block;width:100%;height:auto;border-radius:8px}
.pv-det{margin:10px 14px 0;border:1px solid var(--line);border-radius:10px;background:#fcfdff;overflow:hidden}
.pv-det>summary{cursor:pointer;padding:9px 13px;font-size:13px;font-weight:600;color:var(--pri2);
  list-style:none;display:flex;align-items:center;gap:8px}
.pv-det>summary::-webkit-details-marker{display:none}
.pv-det>summary:before{content:'\25B8';font-size:12px;color:var(--ink4)}
.pv-det[open]>summary:before{content:'\25BE'}
.pv-det .sol{padding:0 14px 12px}
.pv-ft{display:flex;gap:9px;align-items:center;flex-wrap:wrap;padding:12px 14px 14px}
.pv-fav{display:inline-flex;align-items:center;gap:5px;border:1px solid var(--line);background:#fff;
  border-radius:10px;padding:8px 13px;font-size:13px;font-weight:600;color:var(--ink2)}
.pv-fav .ico{font-size:15px;color:var(--ink4)}
.pv-fav.on{border-color:#e6cf9c;background:#fff8e8;color:#8a6014}
.pv-fav.on .ico{color:var(--gold)}
.pv-pager{display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:center;margin:16px 0}
.pv-empty{text-align:center;padding:38px 20px;color:var(--ink3)}
.idx-b.fav:before{content:'\2605';position:absolute;right:6px;bottom:4px;font-size:10px;
  color:var(--gold);line-height:1}
@media(max-width:520px){
  .star{width:27px;height:27px;font-size:16px}
  .qhead{padding:10px 12px;gap:7px}
  .pv-hd{gap:7px;padding:10px 11px}
  .pv-sec{white-space:normal;flex-basis:55%}
  .pv-hd2 h2{font-size:19px}
  .pv-ft .btn{padding:8px 12px}
}
</style>
</head>
<body>
<div class="top"><div class="wrap">
  <div class="brand"><div class="mark">26</div>
    <div title="MTH026 微积分（一） · 674 道题 · 54 个考点">MTH026
      <small>Calculus I · 674 items · 54 topics</small></div></div>
  <div class="spacer"></div>
  <button class="btn ghost" onclick="route('home')">Practice<span class="zhx navz">练习</span></button>
  <button class="btn ghost" onclick="route('ref')">Reference<span class="zhx navz">手册</span></button>
  <button class="btn ghost" onclick="route('browse')">Bank<span class="zhx navz">题库</span></button>
  <button class="btn ghost ic" id="btnFav" onclick="route('fav')" title="Favourites 收藏夹">★<span class="zhx navz">收藏</span></button>
  <div class="chip" id="cAns">Answered <b>0</b></div>
  <div class="chip" id="cAcc">Accuracy <b>—</b></div>
  <div class="chip" id="cStreak">Streak <b>0</b></div>
  <button class="btn ghost" id="btnAcct" onclick="openAcct()" style="display:flex;align-items:center;gap:7px">
    <span class="dot" id="acctDot"></span><span id="acctName">Sign in</span></button>
  <button class="btn ghost" id="btnReset" onclick="resetAll()">Reset</button>
</div></div>
<div class="modal" id="mAcct" onclick="if(event.target===this) closeAcct()">
  <div class="mbox">
    <div class="mhd"><h3 id="mTitle">Account</h3>
      <button class="x" onclick="closeAcct()" aria-label="Close">&#10005;</button></div>
    <div id="mBody"></div>
  </div>
</div>
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
PQ.forEach(p=>{ BYID[p.id]={id:p.id, s:p.s, c:p.c, p:p.p, pq:1, a:p.a}; });
const PQBYSEC = {}; PQ.forEach(p=>{ (PQBYSEC[p.s]=PQBYSEC[p.s]||[]).push(p.id); });
/* one topic = both decks. Graded items first, then the originals served for it,
   so a topic is fully covered only when every item of either deck has been seen. */
const ALLBYSEC = {};
SECS.forEach(s=>{ const a=[];
  for(let i=s.from;i<=s.to;i++) a.push(i);
  (PQBYSEC[s.id]||[]).forEach(p=>a.push(p));
  ALLBYSEC[s.id]=a;
});
const TOTAL_PQ = PQ.length;
const REF = DATA.ref || [], FORMS = DATA.forms || [], GLOSS = DATA.gloss || [];
/* Each account owns its own localStorage bucket.  curOwner===null is the guest
   bucket (the historical key, so old data survives).  A signed-in account uses
   mth026.en.v1@<name>; name is already lower-cased by the server. */
let curOwner = null, curView = 'home';
function lsKey(){ return curOwner===null? LS : LS+'@'+curOwner; }
function hasRecords(s){
  return Object.keys((s&&s.h)||{}).length>0 || Object.keys((s&&s.fav)||{}).length>0;
}
/* Old localStorage blobs may hold fav[id]=true/false/null or padded keys.
   The server skips bool/null and abs>1e14, so normalise before anything is
   uploaded: keys become canonical integer strings, values signed ms ints. */
function normFav(f){
  /* Same whitelist as the server's _fav_int(): a favourite is a signed ms
     timestamp, nothing else. Booleans/nulls are dropped rather than turned into
     1/0 — the server would accept 1 as a real (tiny) timestamp and isFav() would
     then show a ghost star that can never be explained. */
  const out={};
  Object.keys(f||{}).forEach(k=>{
    const key=String(Number(k));
    if(!/^\d+$/.test(key) || !(+key>0)) return;
    const raw=f[k];
    if(typeof raw==='boolean' || raw==null) return;
    const v=+raw;
    if(!Number.isFinite(v) || v===0 || Math.abs(v)>1e14) return;
    out[key]=v;
  });
  return out;
}
function emptyStore(){ return {h:{}, fav:{}, streak:0, best:0}; }
function loadBucket(key){
  let s=emptyStore();
  try{ const raw=localStorage.getItem(key); if(raw) s=Object.assign(s,JSON.parse(raw)); }catch(e){}
  s.fav=normFav(s.fav);
  return s;
}
let store = loadBucket(LS);   // boot from the guest bucket: old data is never lost
function save(quiet){
  try{localStorage.setItem(lsKey(),JSON.stringify(store))}catch(e){}
  if(!quiet) schedulePush();
}

/* ---------- account + cloud sync ----------
   Signed out, the browser is the only store. Signed in, the server keeps a
   copy and the two are merged per item by timestamp, so no device can erase
   what another device recorded. */
const CAN_API = location.protocol==='http:' || location.protocol==='https:';
let ACCT=null, SYNC=CAN_API?'guest':'local', acctMode='in', pushTimer=null;

function api(path, opts){
  opts=opts||{};
  opts.credentials='same-origin';
  opts.headers=Object.assign({'Content-Type':'application/json'}, opts.headers||{});
  return fetch(path, opts)
    .then(r=>r.json().catch(()=>({})).then(d=>({ok:r.ok, status:r.status, d:d||{}})))
    .catch(()=>null);
}

function mergeInto(dst, src){
  const h=(src&&src.h)||{};
  Object.keys(h).forEach(k=>{
    const a=dst.h[k], b=h[k]||{};
    if(!a || (+b.t||0)>=(+a.t||0)) dst.h[k]=b;
  });
  dst.fav=dst.fav||{};
  const f=(src&&src.fav)||{};
  Object.keys(f).forEach(k=>{
    const a=+(dst.fav[k])||0, b=+(f[k])||0;          // true->1, false/null->0
    if(Math.abs(b)>=Math.abs(a)) dst.fav[k]=b;        // newest abs wins; deletions too
  });
  dst.streak=Math.max(+dst.streak||0, +src.streak||0);
  dst.best=Math.max(+dst.best||0, +src.best||0);
}

/* Switch the local bucket to `name` (ACCT.name, lowercase).  Call only after
   the server has confirmed the session.  Cancel any pending debounced push
   FIRST, so the previous owner's store can never be uploaded under the new
   account.  Then carry a guest's progress into the account exactly once, or
   move between two account buckets, and finally load the target bucket. */
function switchOwner(name){
  if(pushTimer){ clearTimeout(pushTimer); pushTimer=null; }
  if(curOwner===name) return;
  if(curOwner===null){
    const guest=loadBucket(LS), acctKey=LS+'@'+name;
    if(hasRecords(guest)){
      const acct=loadBucket(acctKey);
      mergeInto(acct, guest);
      try{ localStorage.setItem(acctKey,JSON.stringify(acct)); }catch(e){}
      try{ localStorage.removeItem(LS); }catch(e){}   // retire the guest key
    }
    curOwner=name;
    store=loadBucket(acctKey);
  } else {
    save(true);                     // flush the old account's bucket
    curOwner=name;
    store=loadBucket(lsKey());      // new account's bucket, or an empty store
  }
}
/* Repaint whatever the reader is looking at after the active bucket changed,
   otherwise the header and cards keep showing the previous account's numbers.
   Quiet in an in-flight quiz: viewQuiz()/viewPq() only render round state, they
   never reset round.picked, so a revealed answer survives the switch. */
function redrawAfterSwitch(){
  if(curView==='home') viewHome();
  else if(curView==='quiz') viewQuiz();
  else if(curView==='res') viewRes();
  else if(curView==='preview') viewPreview();
  else if(curView==='fav') viewFav();
  else if(curView==='ref') viewRef();
  else if(curView==='browse') viewBrowse();
  paintTop();
}

function setSync(s){ SYNC=s; paintAcct(); }

function schedulePush(){
  if(!ACCT||!CAN_API) return;
  clearTimeout(pushTimer);
  pushTimer=setTimeout(()=>syncNow(), 700);
}

function syncNow(){
  if(!ACCT||!CAN_API) return Promise.resolve();
  setSync('busy');
  return api('api/progress',{method:'PUT',
      body:JSON.stringify({h:store.h, streak:store.streak, best:store.best, fav:store.fav})})
    .then(r=>{
      if(!r){ setSync('err'); return; }
      if(r.status===401){
        // Session expired: leave the account bucket too, or a later save would
        // write its records into the guest key and leak into the next login.
        if(pushTimer){ clearTimeout(pushTimer); pushTimer=null; }
        save(true); ACCT=null; curOwner=null;
        store=loadBucket(LS); setSync('guest'); redrawAfterSwitch();
        return;
      }
      if(!r.ok){ setSync('err'); return; }
      mergeInto(store, r.d);
      save(true);
      setSync('on');
    });
}

function bootAcct(){
  if(!CAN_API){ setSync('local'); return Promise.resolve(); }
  return api('api/me').then(r=>{
    if(!r){ setSync('err'); return; }
    if(!r.d || !r.d.user){ setSync('guest'); return; }
    switchOwner(r.d.user.name);      // bucket first, then any cloud traffic
    ACCT=r.d.user; setSync('busy');
    return api('api/progress').then(g=>{
      if(g && g.ok){ mergeInto(store, g.d); save(true); }
      return syncNow();
    }).then(()=>{ redrawAfterSwitch(); });
  });
}

function paintAcct(){
  const n=document.getElementById('acctName'), d=document.getElementById('acctDot');
  if(!n||!d) return;
  n.textContent = ACCT? ACCT.display : (CAN_API? 'Sign in' : 'Local only');
  const label={on:'Synced to your account', busy:'Syncing…', err:'Sync failed',
               guest:'Not signed in — saved in this browser', local:'Saved in this browser'};
  d.className='dot'+(SYNC==='on'?' on':(SYNC==='err'?' err':''));
  d.title=label[SYNC]||'';
}

function openAcct(){
  acctMode = ACCT? 'me':'in';
  renderAcct();
  document.getElementById('mAcct').classList.add('on');
  if(acctMode!=='me') setTimeout(()=>{ const i=document.getElementById('au'); if(i) i.focus(); },60);
}
function closeAcct(){ document.getElementById('mAcct').classList.remove('on'); }
function switchAcct(m){ acctMode=m; renderAcct(); }

function renderAcct(){
  const t=document.getElementById('mTitle'), b=document.getElementById('mBody');
  if(!t||!b) return;
  if(acctMode==='me' && ACCT){
    t.textContent='Your account · 我的账号';
    const n=Object.keys(store.h).length;
    b.innerHTML=`
      <div class="who"><div class="av">${(ACCT.display||'?').charAt(0).toUpperCase()}</div>
        <div><div style="font-weight:700">${ACCT.display}</div>
        <div class="muted" style="font-size:12px">${n} records on this device ·
          ${SYNC==='on'?'synced':(SYNC==='err'?'last sync failed':'not synced yet')}<br>
          <span class="zhx">本机 ${n} 条记录 · ${SYNC==='on'?'已同步':(SYNC==='err'?'上次同步失败':'尚未同步')}</span></div></div></div>
      <button class="btn ghost" style="width:100%;margin-bottom:8px"
        onclick="syncNow().then(()=>{renderAcct();toast('Synced · 已同步');})">Sync now <span class="zhx">立即同步</span></button>
      <button class="btn ghost" style="width:100%;color:var(--red)" onclick="doLogout()">Sign out <span class="zhx">退出登录</span></button>
      <p class="mnote">Signing out ends this session but keeps the records on this device.
      Sign in on another device with the same username and the two sets are merged question by question.<br>
      <span class="zhx">退出只结束本次登录，本机记录保留；在另一台设备用同一账号登录后，两边的答题记录会按题目逐条合并。</span></p>`;
    return;
  }
  const up = acctMode==='up';
  t.textContent = up? 'Create an account · 注册' : 'Sign in · 登录';
  b.innerHTML=`
    <div class="mtabs">
      <button class="${up?'':'on'}" onclick="switchAcct('in')">Sign in <span class="zhx">登录</span></button>
      <button class="${up?'on':''}" onclick="switchAcct('up')">Create account <span class="zhx">注册</span></button>
    </div>
    <div class="fld"><label for="au">Username <span class="zhx">用户名</span></label>
      <input id="au" autocomplete="username" placeholder="3–24 characters, letters or digits"
        onkeydown="if(event.key==='Enter')submitAcct()"></div>
    <div class="fld"><label for="ap">Password <span class="zhx">密码</span></label>
      <input id="ap" type="password" autocomplete="${up?'new-password':'current-password'}"
        placeholder="${up?'at least 6 characters':'your password'}"
        onkeydown="if(event.key==='Enter')submitAcct()"></div>
    <div id="mErr"></div>
    <button class="btn pri" id="mGo" style="width:100%;margin-top:2px" onclick="submitAcct()">${up?'Create account':'Sign in'}
      <span class="zhx">${up?'注册':'登录'}</span></button>
    <p class="mnote">${up
      ? 'No email, no verification — a username and a password is all. The '
        +Object.keys(store.h).length+' records already on this device move into the new account.'
      : 'Progress kept in this browser is merged with whatever the account already holds; the newest answer wins per question.'}
      <br><span class="zhx">不需要邮箱验证；本机已有的记录会并入账号，同一道题以最新一次作答为准。</span></p>`;
}

function submitAcct(){
  const u=((document.getElementById('au')||{}).value||'').trim();
  const p=(document.getElementById('ap')||{}).value||'';
  const err=document.getElementById('mErr'), go=document.getElementById('mGo');
  const up = acctMode==='up';
  if(!err||!go) return;
  if(!u||!p){ err.innerHTML='<div class="merr">Fill in both fields.</div>'; return; }
  err.innerHTML=''; go.disabled=true; go.textContent= up?'Creating…':'Signing in…';
  api(up?'api/register':'api/login',{method:'POST',body:JSON.stringify({u:u,p:p})}).then(r=>{
    const reset=()=>{ go.disabled=false; go.textContent= up?'Create account':'Sign in'; };
    if(!r){ err.innerHTML='<div class="merr">No answer from the server. Check your connection.</div>'; reset(); return; }
    if(!r.ok){ err.innerHTML='<div class="merr">'+((r.d&&r.d.error)||'Something went wrong')+'</div>'; reset(); return; }
    ACCT=r.d.user; acctMode='me';
    switchOwner(r.d.user.name);
    return syncNow().then(()=>{
      closeAcct(); redrawAfterSwitch(); viewHome();
      toast(up? 'Account created — progress will follow you' : 'Signed in as '+ACCT.display);
    });
  });
}

function doLogout(){
  api('api/logout',{method:'POST'}).then(()=>{
    if(pushTimer){ clearTimeout(pushTimer); pushTimer=null; }
    save(true);                       // persist the account's bucket first
    ACCT=null; curOwner=null; setSync(CAN_API?'guest':'local');
    store=loadBucket(LS);             // back to the guest bucket (or empty)
    closeAcct(); redrawAfterSwitch(); viewHome(); toast('Signed out');
  });
}

/* ---------- stats ---------- */
function secStat(id){
  const s=SECMAP[id]; let done=0, ok=0;
  for(let i=s.from;i<=s.to;i++){ const r=store.h[i]; if(r){done++; if(r.ok) ok++;} }
  return {done, ok, n:s.n, acc: done? ok/done : 0};
}
/* Accuracy counts every automatically graded record (Q + P items that carry a
   recovered answer letter).  Legacy self-marked P records (self:1) are still
   "answered", but their reader-supplied verdict must not move the accuracy the
   engine steers by — they are reported separately as selfDone. */
function overall(){
  let done=0, ok=0, selfDone=0, qDone=0, pDone=0;
  Object.keys(store.h).forEach(k=>{
    const r=store.h[k], isP=+k>=1000;
    if(r.self){ selfDone++; if(isP) pDone++; return; }
    done++; if(r.ok) ok++;
    if(isP) pDone++; else qDone++;
  });
  return {done, ok, selfDone, answered:done+selfDone, qDone, pDone,
          acc: done? ok/done : 0};
}
/* Only auto-graded P records feed this accuracy.  History kept from the old
   self-marking flow is listed on its own so the two are never mixed. */
function pqStat(){
  let done=0, ok=0, selfDone=0;
  PQ.forEach(p=>{
    const r=store.h[p.id];
    if(!r) return;
    if(r.self){ selfDone++; return; }
    done++; if(r.ok) ok++;
  });
  return {done, ok, selfDone, acc: done? ok/done : 0};
}
function paintTop(){
  const o=overall();
  document.getElementById('cAns').innerHTML='Answered <b>'+o.answered+'</b>';
  document.getElementById('cAcc').innerHTML='Accuracy <b>'+(o.done? Math.round(o.acc*100)+'%':'—')+'</b>';
  document.getElementById('cStreak').innerHTML='Streak <b>'+store.streak+'</b>';
  document.querySelectorAll('[data-fav-count]').forEach(el=>{ el.textContent=favCount(); });
  paintAcct();
}
function toast(m){ const t=document.getElementById('toast'); t.textContent=m; t.classList.add('on');
  clearTimeout(t._t); t._t=setTimeout(()=>t.classList.remove('on'),1600); }
function resetAll(){
  const extra = ACCT? ' This also clears the copy kept by your account.' : '';
  if(!confirm('Clear all progress?'+extra)) return;
  store=emptyStore(); save(true);   // only the current bucket is cleared
  if(ACCT&&CAN_API){ api('api/progress',{method:'DELETE'}).then(()=>setSync('on')); }
  paintTop(); route('home');
}

/* ---------- favourites ----------
   store.fav[id] = signed epoch ms. >0 is starred, <0 is a "tombstone" for an
   un-star. abs() is the operation time, so a later deletion still wins when two
   devices are merged. Legacy booleans read as 1 / 0 via +v. */
function isFav(id){ return (+((store.fav||{})[id])||0) > 0; }
function favCount(){ return Object.keys(store.fav||{}).filter(k=>isFav(k)).length; }
function starBtn(id){
  const on=isFav(id);
  return `<button class="star${on?' on':''}" data-star="${id}" onclick="toggleFav(${id})" title="Favourite 收藏" aria-label="Favourite">${on?'★':'☆'}</button>`;
}
function favBtn(id){
  const on=isFav(id);
  return `<button class="pv-fav${on?' on':''}" data-star="${id}" onclick="toggleFav(${id})">`
    +`<span class="ico">${on?'★':'☆'}</span> `
    +`<span class="lb-en">${on?'Starred':'Favourite'}</span> `
    +`<span class="zhx lb-zh">${on?'已收藏':'收藏'}</span></button>`;
}
function toggleFav(id){
  const was=isFav(id);
  store.fav=store.fav||{};
  store.fav[id]= was? -Date.now() : Date.now();
  save();
  const now=!was;
  document.querySelectorAll('[data-star="'+id+'"]').forEach(b=>{
    b.classList.toggle('on', now);
    const ico=b.querySelector('.ico');
    if(ico) ico.textContent= now?'★':'☆'; else b.textContent= now?'★':'☆';
    const en=b.querySelector('.lb-en'), zh=b.querySelector('.lb-zh');
    if(en) en.textContent= now?'Starred':'Favourite';
    if(zh) zh.textContent= now?'已收藏':'收藏';
  });
  document.querySelectorAll('[data-fav-count]').forEach(el=>{ el.textContent=favCount(); });
  toast(now? 'Starred · 已收藏' : 'Removed · 已取消');
  /* Quiz cards must never be redrawn (that would erase the picked answer and
     the revealed solution). On the Preview / Favourites board there is no such
     state to lose, so refresh the index and paged list in place. pvPaint() keeps
     scroll position and the search box; renderPv() would rebuild everything. */
  if(!document.querySelector('.qcard') && document.getElementById('pvCards')) pvPaint();
}
function clearFav(){
  if(!favCount()) return;
  if(!confirm('Remove all favourites? · 清空收藏夹？')) return;
  const t=Date.now();
  Object.keys(store.fav).forEach(k=>{ if(isFav(k)) store.fav[k]=-t; });
  save(); route('fav'); toast('Favourites cleared · 已清空');
}
function currentFavId(){
  if(document.querySelector('.qcard') && round && round.list && round.list.length)
    return round.list[round.i];
  const el=document.querySelector('.pv-card.hl') || document.querySelector('.pv-card');
  if(el) return +el.getAttribute('data-id');
  return null;
}

/* ---------- smart engine ----------
   Round 1 walks every topic once (coverage). After that every topic is scored:
   open mistakes (dominant) + measured weakness + unseen material + forgetting,
   minus a penalty for the topic just served. Inside the winning topic the exact
   item you missed is re-tested before anything new is served. */
const SKIP_TTL = 12*3600*1000;

function skips(){
  const raw=store.skip||{}, now=Date.now(), out={q:{},s:{}};
  ['q','s'].forEach(k=>Object.keys(raw[k]||{}).forEach(key=>{
    if(now-(+raw[k][key]||0) < SKIP_TTL) out[k][key]=+raw[k][key];
  }));
  return out;
}
function addSkip(kind,key){
  store.skip=store.skip||{q:{},s:{}};
  store.skip[kind]=store.skip[kind]||{};
  store.skip[kind][key]=Date.now();
  save();
}
function clearSkips(){
  store.skip={q:{},s:{}}; save();
  toast('Skip list cleared · 跳过记录已清空');
  viewHome(); paintTop();
}
function cycleState(){
  if(!store.cyc || !store.cyc.seen) store.cyc={n:(store.cyc&&store.cyc.n)||1, seen:{}};
  return store.cyc;
}
function cycleInfo(){ const c=cycleState(); return {n:c.n||1, seen:Object.keys(c.seen).length, all:SECS.length}; }
function markCycle(sec){
  const c=cycleState();
  c.seen[sec]=1;
  if(Object.keys(c.seen).length>=SECS.length){ c.n=(c.n||1)+1; c.seen={}; return true; }
  return false;
}

/* one topic measured across both decks */
function diag(id){
  const all=ALLBYSEC[id];
  let done=0, ok=0, miss=0, unseen=0, last=Infinity;
  for(const i of all){
    const r=store.h[i];
    if(!r){ unseen++; continue; }
    done++; if(r.ok) ok++; else miss++;
    if((r.t||0)<last) last=r.t||0;
  }
  return {id, n:all.length, done, ok, miss, unseen,
          acc: done? ok/done : 0, cov: all.length? done/all.length : 0, last: last===Infinity?0:last};
}
function days(t){ return t? Math.min((Date.now()-t)/86400000, 30) : 30; }
function weakness(d){
  let s=0;
  s += 5.0*Math.min(d.miss,3);              // every open mistake outranks everything else
  s += 2.2*(1-d.acc)*Math.min(d.done,4);    // weakness, but only as far as evidence goes
  s += 1.5*(1-d.cov);                       // material never seen still needs covering
  s += 0.7*Math.min(days(d.last)/7,4);      // forgetting: 0-4 weeks
  if(store.lastSec===d.id) s -= 1.2;        // never the same topic twice in a row
  return s;
}
/* Choose one item inside a topic.  `rnd` is injectable so tests can pin the
   draw; it defaults to Math.random.  Mistakes first (P mistakes before Q),
   then unseen P, then unseen Q, then one of the three longest-untouched items.
   The topic-level weakness score in pickSmart() is deliberately untouched. */
function pickFrom(d, sk, rnd){
  rnd = rnd || Math.random;
  const all=ALLBYSEC[d.id], free=i=>!sk.q[i];
  const one=a=>a[Math.min(a.length-1, Math.max(0, Math.floor(rnd()*a.length)))];
  const isP=i=>i>=1000;
  const open=all.filter(i=>store.h[i] && !store.h[i].ok && free(i));
  if(open.length){
    const p=open.filter(isP), q=open.filter(i=>!isP(i));
    return {id:one(p.length? p : (q.length? q : open)), kind:'retry'};
  }
  const freshP=all.filter(i=>isP(i) && !store.h[i] && free(i));
  if(freshP.length) return {id:one(freshP), kind:'new'};
  const freshQ=all.filter(i=>!isP(i) && !store.h[i] && free(i));
  if(freshQ.length) return {id:one(freshQ), kind:'new'};
  const rest=all.filter(free)
    .sort((a,b)=>((store.h[a]||{}).t||0)-((store.h[b]||{}).t||0)).slice(0,3);
  return rest.length? {id:one(rest), kind:'stale'} : null;
}
function whyText(d,c){
  const n=d.miss;
  if(c.kind==='retry') return n+' open '+(n===1?'mistake':'mistakes')+' in this topic · 这类还有 '+n+' 道错题没订正';
  if(c.kind==='new') return d.unseen+' item'+(d.unseen===1?'':'s')+' never seen · 这类还有 '+d.unseen+' 道没做过';
  const dd=d.last? Math.max(1,Math.round(days(d.last))) : 0;
  return (dd? 'gone '+dd+' days' : 'not seen yet')+' without practice · 这类'+(dd? '已 '+dd+' 天没练':'还没练过');
}
function pickSmart(){
  const sk=skips();
  let pool=SECS.filter(s=>!sk.s[s.id]);
  if(!pool.length){ store.skip={q:{},s:{}}; save(true); pool=SECS.slice(); }
  const ds=pool.map(s=>diag(s.id));
  // phase 1 — one pass through every topic, syllabus order
  const un=ds.filter(d=>d.done===0);
  for(const d of un){
    const c=pickFrom(d,sk);
    if(c) return {id:c.id, why:whyText(d,c), phase:1, sec:d.id, kind:c.kind};
  }
  // phase 2 — everything ranked, mistakes first
  let best=null, bestSc=-9e9;
  for(const d of ds){
    if(d.done===0) continue;
    const c=pickFrom(d,sk); if(!c) continue;
    const sc=weakness(d);
    if(sc>bestSc){ bestSc=sc; best={d,c}; }
  }
  if(best) return {id:best.c.id, why:whyText(best.d,best.c), phase:2, sec:best.d.id, kind:best.c.kind};
  return null;
}
function untouchedSecs(){ return SECS.filter(s=>diag(s.id).done===0); }

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
function route(v,arg){ curView=v; window.scrollTo(0,0);
  const HASHV={home:'#home', ref:'#ref', browse:'#bank', preview:'#preview', fav:'#fav'};
  try{ if(HASHV[v] && location.hash!==HASHV[v]) history.replaceState(null,'',HASHV[v]); }catch(e){}
  if(v==='home') viewHome(); else if(v==='quiz') viewQuiz();
  else if(v==='res') viewRes(); else if(v==='browse') viewBrowse(arg||'all');
  else if(v==='ref') viewRef(arg);
  else if(v==='preview') viewPreview();
  else if(v==='fav') viewFav();
  paintTop();
}
function start(mode){
  let list=[];
  if(mode==='smart'){
    let p=pickSmart();
    if(!p){ store.skip={q:{},s:{}}; save(true); p=pickSmart(); }
    if(!p){ toast('Everything is answered — clearing skips.'); return; }
    list=[p.id];
    store.lastSec=p.sec; save(true);
    round={list, i:0, mode, picked:null, done:false, t0:Date.now(), ok:0, ans:0,
           why:p.why, phase:p.phase, sec:p.sec};
    route('quiz'); return;
  }
  if(mode==='mock') list=buildMock(20);
  else if(mode==='wrong') list=wrongQueue();
  else if(mode==='pq'){ startPq(10); return; }
  if(!list.length){ toast('Nothing to review — all clear.'); return; }
  round={list, i:0, mode, picked:null, done:false, t0:Date.now(), ok:0, ans:0};
  route('quiz');
}
/* skip controls — smart round only. Both are remembered for 12 h so the same
   item or topic is not immediately handed back to you. */
function skipQ(){
  const id=round.list[round.i];
  addSkip('q', id);
  toast('Skipped · 已跳过这题');
  start('smart');
}
function skipSec(){
  const id=round.list[round.i], q=BYID[id], sec=q.s;
  addSkip('s', sec);
  const done=markCycle(sec); save();
  toast('Skipping '+(SECMAP[sec]? SECMAP[sec].en : sec)+' · 暂时跳过这类');
  if(done) toast('Round complete — mistakes go first · 本轮完成，错题优先');
  start('smart');
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
/* mastery row: the topic as measured — graded items first, then its originals */
function startTopicAll(id){
  const list=(ALLBYSEC[id]||[]).slice()
    .sort((a,b)=>(store.h[a]?1:0)-(store.h[b]?1:0) || (a-b));
  if(!list.length){ toast('Nothing in this topic.'); return; }
  round={list, i:0, mode:'topic', picked:null, done:false, t0:Date.now(), ok:0, ans:0};
  route('quiz');
}

/* ---------- views ---------- */
function viewHome(){
  const o=overall();
  const pq=pqStat();
  const un=untouchedSecs().length;
  const wrong=wrongQueue().length;
  const cy=cycleInfo();
  const sk=skips(), skSec=Object.keys(sk.s).length, skQ=Object.keys(sk.q).length;
  let openMiss=0;
  SECS.forEach(s=>{ openMiss+=diag(s.id).miss; });
  const rows = SECS.map(s=>{
    const d=diag(s.id);
    const pct=Math.round(d.acc*100);
    const cov=Math.round(d.cov*100);
    const cls= d.done===0? '' : (pct>=80?'ok':(pct>=50?'warn':'bad'));
    const pqn=(PQBYSEC[s.id]||[]).length;
    return '<div class="sec-row" onclick="startTopicAll(\''+s.id+'\')" style="cursor:pointer" '
      +'title="'+s.id+' · '+d.ok+'/'+d.done+' correct, '+d.miss+' open, '+d.unseen+' unseen">'
      +'<span class="sec-id">'+s.id+'</span>'
      +'<span class="sec-t">'+s.en+'<span class="tz">'+s.zh+'</span>'+(pqn
          ? ' <span class="pill" style="font-size:11px;padding:1px 7px" '
            +'onclick="event.stopPropagation();startTopicPq(\''+s.id+'\')">'+pqn+'P</span>' : '')
      +'</span>'
      +'<span class="bar" title="'+cov+'% covered · '+pct+'% correct"><i class="'+cls+'" style="width:'+(d.done? Math.max(cov,5):0)+'%"></i></span>'
      +'<span class="sec-n">'+d.done+'/'+d.n+(d.miss? '<span class="miss">'+d.miss+'&#10005;</span>':'')+'</span></div>';
  }).join('');
  const fresh = o.answered===0;
  document.getElementById('view').innerHTML = `
  <div class="wrap">
    <div class="hero">
      <h1>${fresh? 'Start where it matters' : 'Keep the streak alive'}
        <span class="zh" style="display:inline;font-size:15px">${fresh? '从最该练的地方开始' : '继续保持手感'}</span></h1>
      <p>${fresh
        ? 'The engine walks you through <b>one question from every topic first</b> — all <b>674</b> items, both decks — then scores every topic on open mistakes, weakness and forgetting, so what you got wrong comes back first.'
        : 'You have answered <b>'+o.qDone+'</b> of 351 graded items and <b>'+o.pDone+'</b> of 323 originals. Round '+cy.n+' has covered '+cy.seen+'/'+cy.all+' topics.'}</p>
      <p class="zh">${fresh
        ? '先每个考点过一遍（共 674 道，两套题合一），之后按「<b>未订正的错题</b> → 薄弱程度 → 多久没练」给考点打分，错得多的题型优先回来。'
        : '本轮已过 <b>'+cy.seen+'/'+cy.all+'</b> 个考点，还有 <b>'+openMiss+'</b> 道错题没订正，它们会排在下一轮最前面。'}</p>
      <div class="row">
        <button class="btn white" onclick="start('smart')">${un<SECS.length? 'Continue smart round':'Start smart round'}
          <span class="zhx">${un<SECS.length? '继续智能刷题':'开始智能刷题'}</span></button>
        <button class="btn light" onclick="start('mock')">Mock test · 20 <span class="zhx">模拟卷</span></button>
        <button class="btn light" onclick="start('pq')">Quiz originals · 10 <span class="zhx">原题</span></button>
        <button class="btn light" onclick="route('browse')">Browse all 674 <span class="zhx">全部题目</span></button>
        <button class="btn light" onclick="route('preview')">Preview <span class="zhx">题库速览</span></button>
        <button class="btn light" onclick="route('fav')">★ Favourites · <span data-fav-count>${favCount()}</span> <span class="zhx">收藏夹</span></button>
      </div>
    </div>
    <div class="eng">
      <span>Round <b>${cy.n}</b> <span class="zhx">第 ${cy.n} 轮</span></span>
      <span class="sep">|</span>
      <span><b>${cy.seen}/${cy.all}</b> topics this round <span class="zhx">本轮已过考点</span></span>
      <span class="sep">|</span>
      <span><b>${openMiss}</b> open mistakes <span class="zhx">待订正错题</span></span>
      ${skSec||skQ? `<span class="sep">|</span>
        <span>skipped <b>${skSec}</b> topics / <b>${skQ}</b> questions <span class="zhx">已跳过</span>
        <button class="lnk" onclick="clearSkips()">clear <span class="zhx">清除</span></button></span>`:''}
      <span class="sep">|</span>
      <span class="zhx">推荐依据：错题数 → 正确率 → 覆盖度 → 遗忘天数</span>
    </div>
    <div class="card click" onclick="start('pq')" style="display:flex;align-items:center;gap:18px;margin-bottom:18px;flex-wrap:wrap">
      <div style="min-width:120px"><div class="k">From your practice quizzes <span class="zhx">来自你的练习卷</span></div>
        <div class="stat" style="font-size:26px">${pq.done}<small>/ ${TOTAL_PQ}</small></div></div>
      <div style="flex:1;min-width:240px">
        <p style="margin:0 0 4px"><b>The 323 items you were actually served</b> — question, the paper's own
        “Answer:” line and its printed solution, all page crops.</p>
        <p class="muted" style="margin:0">Most items carry a recovered answer letter, so your pick is marked
        automatically. Two items (p31, p63) have no printable answer and still use self-marking —
        ${pq.done? 'accuracy on auto-marked items so far '+Math.round(pq.acc*100)+'%' : 'nothing marked yet'}
        ${pq.selfDone? '&middot; '+pq.selfDone+' older self-marked records (answered only, not in accuracy)':''}.</p>
      </div>
      <div><button class="btn pri">Open a set of 10 <span class="zhx">打开 10 题</span></button></div>
    </div>
    <div class="grid g3" style="margin-bottom:18px">
      <div class="card"><div class="k">Progress <span class="zhx">总进度</span></div><div class="stat">${o.answered}<small>/ ${ITEMS.length+TOTAL_PQ}</small></div>
        <p>${un===0? 'Every topic has been started.' : un+' topics not started yet.'}
        ${o.qDone}/${ITEMS.length} graded &middot; ${o.pDone}/${TOTAL_PQ} originals.</p></div>
      <div class="card"><div class="k">Accuracy <span class="zhx">自动判分正确率</span></div><div class="stat">${o.done? Math.round(o.acc*100)+'%':'—'}</div>
        <p>${o.ok} correct out of ${o.done} auto-graded answers (graded Q + auto-marked P).
        ${o.selfDone? o.selfDone+' older self-marked records count as answered but not in accuracy.':''}</p></div>
      <div class="card click" onclick="${wrong? "start('wrong')":"toast('No mistakes recorded yet.')"}">
        <div class="k">Review <span class="zhx">错题复习</span></div><div class="stat">${wrong}</div>
        <p>${wrong? 'Questions you got wrong — tap to drill them.':'Nothing to repair yet.'}</p></div>
    </div>
    <div class="card" style="padding:16px 20px 6px">
      <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:2px;flex-wrap:wrap">
        <h3 style="margin:0">Topic mastery <span class="tz" style="font-size:12.5px">考点掌握度</span></h3>
        <span class="muted">graded + originals · 精编与原题合并计算</span>
        <div class="spacer" style="flex:1"></div>
        <span class="muted">answered <span class="zhx">已做/总题</span></span>
      </div>
      <p class="muted" style="margin:0 0 8px;font-size:11.5px">
        Bar = how much is covered, colour = accuracy · 进度条为覆盖度，颜色代表正确率 ·
        <span style="color:var(--red)">3&#10005;</span> = open mistakes · 未订正错题</p>
      ${rows}
    </div>
    <p class="muted" style="margin:18px 0 40px;text-align:center">
      ${ACCT? 'Progress saves to your account <b>'+ACCT.display+'</b> and to this browser.'
             : (CAN_API? 'Progress saves in this browser only — sign in to carry it across devices.'
                        : 'Opened as a local file, so progress stays in this browser only.')}
      Questions are the original page crops — nothing is re-typed.</p>
  </div>`;
}

function viewQuiz(){
  if(round.i>=round.list.length){ round.done=true; return viewRes(); }
  const id=round.list[round.i], q=BYID[id];
  if(q && q.pq) return viewPq();
  const rec=store.h[id];
  const solo = round.mode==='smart' && round.list.length===1;
  const cy=cycleInfo();
  const covered = cy.seen;
  const pct = solo ? Math.round(covered/SECS.length*100)
                   : Math.round(((round.i)/round.list.length)*100);
  const phase = untouchedSecs().length? 1:2;
  const progLabel = solo
    ? 'Phase '+phase+' · '+covered+'/'+SECS.length+' topics'
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
    ${solo && round.why? `<div class="why"><span class="tag">Why this one · 为什么推这题</span>
      <span>${round.why}</span></div>`:''}
    <div class="qcard">
      <div class="qhead">
        <span class="qno">Q${q.id}</span>
        <span class="qsec" title="${q.s} · ${SECMAP[q.s].en} · ${SECMAP[q.s].zh}">${q.s} · ${SECMAP[q.s].en}<span class="tz"> ${SECMAP[q.s].zh}</span></span>
        ${starBtn(id)}
        <div class="qprog" title="Round ${cy.n} · 第 ${cy.n} 轮">
          <span class="muted" style="font-size:12px">${progLabel}</span>
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
    <div style="display:flex;gap:8px;margin-top:14px;align-items:center;flex-wrap:wrap">
      <button class="btn ghost" onclick="route('home')">Exit <span class="zhx">退出</span></button>
      ${solo? `<button class="btn ghost sm" onclick="skipQ()">Skip question <span class="zhx">跳过这题</span></button>
      <button class="btn ghost sm" onclick="skipSec()">Skip topic <span class="zhx">跳过这类</span></button>`:''}
      <div class="spacer" style="flex:1"></div>
      ${shown? (solo
        ? `<button class="btn pri" onclick="start('smart')">Next question &rarr;</button>`
        : `<button class="btn pri" onclick="advance()">${round.i+1>=round.list.length?'See results':'Next question'}</button>`):''}
    </div>
    <p class="muted" style="text-align:center;margin-top:14px">${solo
      ? 'Shortcut: <b>A–E</b> to answer · <b>S</b> to skip the question · <b>T</b> to skip the topic.'
      : 'Pick a letter. The full worked solution appears straight after.'}</p>
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
  markCycle(q.s);
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

/* ---------- Part B: the items you were served ----------
   Most P items now carry a recovered answer letter (BYID[id].a), so they are
   graded automatically exactly like the Q deck.  p31 / p63 have no printable
   answer (a === null) and fall back to the old reader self-marking flow. */
function viewPq(){
  const id=round.list[round.i], q=BYID[id];
  const p=String(q.p).padStart(3,'0');
  const auto=!!q.a;                       // a letter => automatic grading
  const picked=round.picked, shown=picked!==null;
  // inside a smart round the originals are served one at a time, mixed with the
  // graded items, so grading must hand over to "next" instead of ending a round
  const solo = round.mode==='smart' && round.list.length===1;
  const selfGraded = solo && round.marked;   // only the fallback path uses this
  const canNext = auto? shown : selfGraded;  // auto is done as soon as a letter is picked
  const cy = cycleInfo();
  const unLeft = solo? SECS.length-cy.seen : 0;
  const letters=['A','B','C','D','E'];
  const opts = letters.map(L=>{
    let cls='opt';
    if(shown){
      if(auto){ if(L===q.a) cls+=' ok'; else if(L===picked) cls+=' bad'; }
      else if(L===picked) cls+=' sel';
    }
    return `<button class="${cls}" ${shown?'disabled':''} onclick="pickPq('${L}')">${L}</button>`;
  }).join('');
  const ansImg=`<a href="pq/p${p}_a.jpg" target="_blank" title="Open full size">
        <img src="pq/p${p}_a.jpg" alt="Answer" style="display:block;max-height:74px;max-width:100%;width:auto"></a>`;
  const solImg=`<a href="pq/p${p}_s.jpg" target="_blank" title="Open full size">
        <img class="qimg" src="pq/p${p}_s.jpg" alt="Solution"></a>`;
  let reveal='';
  if(shown && auto){
    const ok=picked===q.a;
    reveal = `
    <div class="fb ${ok?'ok':'bad'}">
      <div class="h">${ok?'Correct':'Not quite'} <span class="tag">answer ${q.a}</span></div>
      <div style="padding:2px 14px 0">${ansImg}</div>
      <div class="h" style="padding-top:12px">Their worked solution
        <span class="tag">tap to zoom</span></div>
      <div style="padding:2px 14px 14px">${solImg}</div>
    </div>`;
  } else if(shown){
    reveal = `
    <div class="fb" style="background:#fffdf8;border-color:#e7dcc6">
      <div class="h" style="color:#8a5a12">Answer, as printed <span class="tag">you picked ${picked}</span></div>
      <div style="padding:2px 14px 0">${ansImg}</div>
      <div class="h" style="color:#8a5a12;padding-top:12px">Their worked solution
        <span class="tag" style="background:#f3ece0;color:#8a7550">tap to zoom</span></div>
      <div style="padding:2px 14px 14px">${solImg}</div>
      <div style="display:flex;gap:10px;padding:0 14px 16px;align-items:center">
        ${selfGraded
          ? `<span class="muted" style="font-size:13px">Recorded — you marked this ${store.h[q.id]&&store.h[q.id].ok? 'correct':'as missed'}.</span>`
          : `<button class="btn pri" onclick="gradePq(1)">My pick was right</button>
        <button class="btn ghost" onclick="gradePq(0)">I missed it</button>`}
      </div>
    </div>`;
  }
  document.getElementById('view').innerHTML = `
  <div class="wrap"><div class="qwrap">
    ${solo && round.why? `<div class="why"><span class="tag">Why this one · 为什么推这题</span>
      <span>${round.why}</span></div>`:''}
    <div class="qcard">
      <div class="qhead">
        <span class="qno" style="background:#9a6a1c">P${q.p}</span>
        <span class="qsec" title="${q.s} · ${SECMAP[q.s].en} · ${SECMAP[q.s].zh}">${q.s} · ${SECMAP[q.s].en}<span class="tz"> ${SECMAP[q.s].zh}</span></span>
        ${starBtn(id)}
        <div class="qprog" title="Round ${cy.n} · 第 ${cy.n} 轮">
          <span class="muted" style="font-size:12px">${solo
          ? 'Phase '+(untouchedSecs().length?1:2)+' · '+cy.seen+'/'+SECS.length+' topics'
          : 'Originals · '+(round.i+1)+'/'+round.list.length}</span>
          <span class="track"><i style="width:${solo
            ? Math.round((SECS.length-unLeft)/SECS.length*100)
            : Math.round(round.i/round.list.length*100)}%"></i></span></div>
      </div>
      <div class="qbody"><img class="qimg" src="pq/p${p}_q.jpg" alt="Question"></div>
      <div class="opts">${opts}</div>
      ${reveal}
    </div>
    <div style="display:flex;gap:8px;margin-top:14px;align-items:center;flex-wrap:wrap">
      <button class="btn ghost" onclick="route('home')">Exit <span class="zhx">退出</span></button>
      ${solo? `<button class="btn ghost sm" onclick="skipQ()">Skip question <span class="zhx">跳过这题</span></button>
      <button class="btn ghost sm" onclick="skipSec()">Skip topic <span class="zhx">跳过这类</span></button>`:''}
      <div class="spacer" style="flex:1"></div>
      ${shown? (solo
        ? (canNext? `<button class="btn pri" onclick="start('smart')">Next question &rarr;</button>`: '')
        : `<button class="btn ${auto?'pri':'ghost'}" onclick="advance()">${auto
            ? (round.i+1>=round.list.length?'See results':'Next question')
            : (round.i+1>=round.list.length?'Skip to results':'Skip')}</button>`):''}
    </div>
    <p class="muted" style="text-align:center;margin-top:14px">${auto
      ? (shown? 'Marked automatically — the engine has recorded your answer.'
              : 'Pick a letter — the answer is marked automatically.')
      : (shown
        ? (selfGraded? 'Marked. The engine picks the next item from whatever you keep missing.'
                     : 'Compare with the printed answer, then mark your own attempt.')
        : (solo? 'Pick the letter you would have chosen, or skip — <b>S</b> skips the question, <b>T</b> the whole topic.'
                : 'Pick the letter you would have chosen. Nothing is scored until you mark it.'))}</p>
  </div></div>`;
  paintTop();
}
function pickPq(L){
  if(round.picked!==null) return;
  const q=BYID[round.list[round.i]];
  round.picked=L;
  if(q.a){
    // automatic grading: same contract as the graded Q deck, no self:1 marker
    const ok=L===q.a;
    store.h[q.id]={a:L, ok, t:Date.now()};
    if(ok){ store.streak++; if(store.streak>store.best) store.best=store.streak; }
    else store.streak=0;
    markCycle(q.s);
    save();
  }
  viewQuiz(); renderMath();
  const fb=document.querySelector('.fb');
  if(fb && fb.getBoundingClientRect().top > innerHeight-120) fb.scrollIntoView({block:'center',behavior:'smooth'});
}
/* Fallback only: items whose answer letter is null keep the old self-marking
   contract (self:1), which the accuracy stats deliberately exclude. */
function gradePq(ok){
  const q=BYID[round.list[round.i]];
  if(q.a) return;                        // auto-graded items never reach here
  store.h[q.id]={a:round.picked, ok:!!ok, t:Date.now(), self:1};
  if(ok){ store.streak++; if(store.streak>store.best) store.best=store.streak; }
  else store.streak=0;
  if(round.mode==='smart') markCycle(q.s);
  save();
  if(round.mode==='smart' && round.list.length===1){
    round.marked=true; viewQuiz(); return;   // smart round: wait for "next"
  }
  advance();
}

function viewRes(){
  const total=round.list.length;
  let ok=0, scored=0, rows='';
  if(round.mode==='mock'){
    const bySec={};
    round.list.forEach(id=>{ const q=BYID[id]; const r=store.h[id];
      if(!r||r.self) return;                 // self-marked history is not scored
      bySec[q.s]=bySec[q.s]||{n:0,ok:0}; bySec[q.s].n++; if(r.ok) bySec[q.s].ok++; });
    rows=Object.keys(bySec).map(s=>{
      const b=bySec[s]; const p=Math.round(b.ok/b.n*100);
      return {s, b, p};
    }).sort((a,b)=>a.p-b.p).map(r=>{
      const s=r.s, b=r.b, p=r.p;
      return '<div class="sec-row"><span class="sec-id">'+s+'</span><span class="sec-t">'+SECMAP[s].en
        +(SECMAP[s].zh? '<span class="tz">'+SECMAP[s].zh+'</span>':'')+'</span>'
        +'<span class="bar"><i class="'+(p>=80?'ok':(p>=50?'warn':'bad'))+'" style="width:'+Math.max(p,6)+'%"></i></span>'
        +'<span class="sec-n">'+b.ok+'/'+b.n+'</span></div>';
    }).join('');
  }
  round.list.forEach(id=>{ const r=store.h[id]; if(r&&!r.self){ scored++; if(r.ok) ok++; } });
  const pct= scored? Math.round(ok/scored*100):0;
  document.getElementById('view').innerHTML=`
  <div class="wrap"><div class="res">
    <div class="card" style="text-align:center;padding:30px 24px">
      <div class="k">${round.mode==='mock'?'Mock test complete':(round.mode==='wrong'?'Repair round complete':(round.mode==='pq'?'Originals round complete':'Round complete'))}
        <span class="zhx">${round.mode==='mock'?'模拟卷完成':(round.mode==='wrong'?'错题复习完成':(round.mode==='pq'?'原题一组完成':'本轮完成'))}</span></div>
      <div class="bigscore">${pct}%</div>
      <p class="muted" style="margin-top:6px">${ok} of ${scored} correct${round.mode==='mock'?' · 20-item mock':' · this round'}</p>
      ${total? `<p style="margin-top:10px">${round.list.map(id=>{
          const r=store.h[id]; const nm = id>=1000? 'P'+(id-1000) : 'Q'+id;
          return `<span class="pill">${nm} ${r&&r.ok?'✓':'✕'}</span>`;}).join('')}</p>`:''}
    </div>
    ${rows? '<div class="card" style="margin-top:14px"><h3>By topic <span class="tz">按考点</span></h3>'+rows+'</div>':''}
    <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap">
      <button class="btn pri" onclick="start('${round.mode==='pq'?'pq':'smart'}')">${round.mode==='pq'?'Another set of 10':'Continue smart round'}</button>
      <button class="btn ghost" onclick="start('wrong')">Drill my mistakes <span class="zhx">只刷错题</span></button>
      <button class="btn ghost" onclick="route('home')">Back to overview <span class="zhx">返回首页</span></button>
    </div>
  </div></div>`;
  paintTop();
}

let refTab='topics', refCh='all';
function viewRef(tab, ch){
  if(tab) refTab=tab;
  if(ch!==undefined) refCh=ch;
  const tabs = [['topics','Topics <span class="zhx">考点</span> '+REF.length],
                ['forms','Formula sheet <span class="zhx">公式表</span>'],
                ['gloss','Terminology <span class="zhx">术语表</span>']]
    .map(p=>`<button class="${refTab===p[0]?'on':''}" onclick="viewRef('${p[0]}')">${p[1]}</button>`).join('');
  let body='';
  if(refTab==='topics'){
    const chips = [`<button class="${refCh==='all'?'on':''}" onclick="viewRef('topics','all')">All chapters <span class="zhx">全部章节</span></button>`]
      .concat(CHS.map((c,i)=>`<button class="${refCh===i?'on':''}" onclick="viewRef('topics',${i})">Ch ${i+1}</button>`)).join('');
    body = `<div class="tabs">${chips}</div>` + CHS.map((c,i)=>{
      if(refCh!=='all' && refCh!==i) return '';
      const list = REF.filter(r=>r.c===i);
      if(!list.length) return '';
      return `<div class="sec-hd"><span class="n">Ch ${i+1}</span><span class="t">${c.en}</span><span class="s">${c.zh}</span></div>`
        + list.map(r=>`<div class="ref-card" id="r${r.id}">
            <div class="ref-h"><span class="ref-id">${r.id}</span><span class="ref-en">${r.en}</span>
              <span class="ref-zh">${r.zh}</span></div>
            <div class="ref-k">What it tests <span class="zhx">考什么</span></div><p class="ref-focus">${r.focus}</p>
            <div class="ref-k">How to do it <span class="zhx">怎么做</span></div><ol class="ref-steps">${r.steps.map(s=>`<li>${s}</li>`).join('')}</ol>
            ${r.note? `<p class="ref-note">${r.note}</p>`:''}
            ${r.trap? `<div class="ref-trap"><b>Trap</b> &middot; <span class="zhx" style="color:var(--red)">易错点</span> ${r.trap}</div>`:''}
            <div style="margin-top:11px;display:flex;gap:8px;flex-wrap:wrap">
              <button class="btn ghost" onclick="startTopic('${r.id}')">Drill ${r.n} graded <span class="zhx">精编</span></button>
              ${PQBYSEC[r.id]? `<button class="btn ghost" onclick="startTopicPq('${r.id}')">${PQBYSEC[r.id].length} originals <span class="zhx">原题</span></button>`:''}
              <button class="btn ghost" onclick="startTopicAll('${r.id}')">Whole topic <span class="zhx">整个考点</span></button>
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
      <h2 style="margin:0;font-size:22px">Reference <span class="tz" style="font-size:14px">考点手册</span></h2>
      <span class="muted">method &middot; steps &middot; trap for every topic, plus the formula sheet and terminology
        <span class="zhx">每个考点的方法、步骤与陷阱，附公式表和术语表</span></span></div>
    <div class="tabs">${tabs}</div>
    ${body}
    <p class="muted" style="margin:22px 0 40px;text-align:center">
      Same content as the printed knowledge map — this page needs no network and no other file.</p>
  </div>`;
  paintTop(); renderMath();
}
/* every item in one index: the 351 compiled Q items and the 323 originals,
   so a number printed on the PDF can always be found here */
const UNI = ITEMS.map(q=>({id:q.id, lb:'Q'+q.id, s:q.s, c:q.c, p:0}))
  .concat(PQ.map(p=>({id:p.id, lb:'P'+p.p, s:p.s, c:p.c, p:1})));
let browseCh='all', browseType='all';

function setType(k){ browseType=k; viewBrowse(); }

function viewBrowse(ch){
  if(ch!==undefined) browseCh=ch;
  document.getElementById('view').innerHTML=`
  <div class="wrap"><div class="res">
    <div class="card">
      <h3 style="margin-bottom:2px">The whole bank <span class="tz" style="font-size:12.5px">全部题库</span></h3>
      <p class="muted">All ${UNI.length} items in one index — ${ITEMS.length} compiled (Q) and
        ${PQ.length} from your own attempts (P). Tap a number to open it on its own.
        <span class="zhx">674 道题汇总：351 道精编（Q）+ 323 道练习卷原题（P），点编号单独打开。</span></p>
      <div class="filter" id="idxType"></div>
      <div class="filter" id="idxCh"></div>
      <div class="idxsearch"><input id="idxQ" placeholder="Find a number — 12, Q12, P7, or a topic id like 2.5 / 搜题号或考点" oninput="setSearch(this.value)"></div>
      <div class="idxmeta" id="idxMeta"></div>
      <div class="idxgrid" id="idxGrid"></div>
    </div>
    <div style="margin-top:14px"><button class="btn ghost" onclick="route('home')">Back <span class="zhx">返回</span></button></div>
  </div></div>`;
  paintIdx();
  paintTop();
}

function setSearch(v){
  const box=document.getElementById('idxQ');
  if(box) box._v=v;
  paintIdx();
}

function paintIdx(){
  const tEl=document.getElementById('idxType'), cEl=document.getElementById('idxCh');
  if(!tEl||!cEl) return;
  tEl.innerHTML=[['all','All <span class="zhx">全部</span> '+UNI.length],
                 ['q','Compiled <span class="zhx">精编</span> '+ITEMS.length],
                 ['p','Originals <span class="zhx">原题</span> '+PQ.length]]
    .map(([k,t])=>`<button class="${browseType===k?'on':''}" onclick="setType('${k}')">${t}</button>`).join('');
  cEl.innerHTML=['<button class="'+(browseCh==='all'?'on':'')+'" onclick="viewBrowse(\'all\')">All chapters <span class="zhx">全部章节</span></button>']
    .concat(CHS.map((c,i)=>`<button class="${browseCh==i?'on':''}" onclick="viewBrowse(${i})">Ch ${i+1}</button>`)).join('');

  const box=document.getElementById('idxQ');
  const raw=box? (box._v!==undefined? box._v : box.value) : '';
  const q=raw.trim().toLowerCase();
  const num=q.match(/^([qp]?)\s*0*(\d{1,3})$/);
  const list=UNI.filter(it=>{
    if(browseCh!=='all' && it.c!==browseCh) return false;
    if(browseType==='q' && it.p) return false;
    if(browseType==='p' && !it.p) return false;
    if(!q) return true;
    if(num){
      const pre=num[1], n=Number(num[2]);
      if(pre==='q' && it.p) return false;
      if(pre==='p' && !it.p) return false;
      return Number(it.lb.slice(1))===n;
    }
    return it.s.indexOf(q)===0;
  });

  let ok=0, seen=0;
  const cells=list.map(it=>{
    const r=store.h[it.id]; if(r){seen++; if(r.ok) ok++;}
    const st=r?(r.ok?'ok':'bad'):'new';
    const sec=SECMAP[it.s];
    return `<button class="idx-b ${st}${it.p?' p':''}${isFav(it.id)?' fav':''}" onclick="startSingle(${it.id})"
      title="${it.lb} · ${it.s}${sec? ' · '+sec.en+' · '+sec.zh : ''}"><b>${it.lb}</b><i>${it.s}</i>${r?(r.ok?'<u>✓</u>':'<u>✕</u>'):''}</button>`;
  }).join('');
  const meta=document.getElementById('idxMeta'), grid=document.getElementById('idxGrid');
  meta.textContent=list.length
    ? `${list.length} item${list.length===1?'':'s'} · ${seen} attempted · ${ok} correct ／ 共 ${list.length} 题，已做 ${seen}，正确 ${ok}`
    : 'Nothing matches that filter. ／ 没有匹配的题目。';
  grid.innerHTML=cells || '<p class="muted" style="padding:8px 0;grid-column:1/-1">No item in this slice.</p>';
}
function startSingle(id){
  round={list:[id], i:0, mode:'single', picked:null, done:false, t0:Date.now()};
  route('quiz');
}

/* ---------- preview / favourites board ----------
   Pure browsing: answers are shown immediately; nothing is answered or scored.
   viewFav reuses the same renderer with the data source limited to starred ids. */
let pvType='all', pvCh='all', pvQ='', pvPage=0, pvScope='all', pvMode='preview';
const PV_PER=6;
function pvEsc(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/"/g,'&quot;')
  .replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function pvMatch(it, q){
  if(!q) return true;
  const num=q.match(/^([qp]?)\s*0*(\d{1,3})$/);
  if(num){
    const pre=num[1], n=Number(num[2]);
    if(pre==='q' && it.p) return false;
    if(pre==='p' && !it.p) return false;
    return Number(it.lb.slice(1))===n;
  }
  if(it.s.indexOf(q)===0) return true;                     // topic id, e.g. 2.5
  const sec=SECMAP[it.s];
  if(sec && (sec.en.toLowerCase().indexOf(q)>=0 || sec.zh.indexOf(q)>=0)) return true;
  return it.lb.toLowerCase().indexOf(q)>=0;                // Q12 / P7 fallback
}
function pvList(){
  const q=(pvQ||'').trim().toLowerCase();
  return UNI.filter(it=>{
    if(pvCh!=='all' && it.c!==pvCh) return false;
    if(pvScope==='fav' && !isFav(it.id)) return false;
    if(pvType==='q' && it.p) return false;
    if(pvType==='p' && !it.p) return false;
    if(pvScope==='all' && pvType==='fav' && !isFav(it.id)) return false;
    return pvMatch(it, q);
  });
}
function pvSetType(k){ pvType=k; pvPage=0; renderPv(pvMode); }
function pvSetCh(c){ pvCh=c; pvPage=0; renderPv(pvMode); }
function pvSetQ(v){ pvQ=v; pvPage=0; pvPaint(); }
function pvPageGo(n){ pvPage=n; pvPaint();
  const el=document.getElementById('pvCards'); if(el) el.scrollIntoView({block:'start',behavior:'smooth'}); }
function pvGo(id){
  const list=pvList(), idx=list.findIndex(x=>x.id===id);
  if(idx<0) return;
  pvPage=Math.floor(idx/PV_PER); pvPaint();
  const el=document.querySelector('.pv-card[data-id="'+id+'"]');
  if(el){ el.classList.add('hl'); el.scrollIntoView({block:'center',behavior:'smooth'}); }
}

function previewCard(id){
  const q=BYID[id], sec=SECMAP[q.s]||{en:'',zh:''}, rec=store.h[id];
  const isP=q.pq===1;
  const badge=isP? 'P'+q.p : 'Q'+q.id;
  const done=rec? (rec.ok? '<span class="pv-done ok">✓ Done · 已做对</span>'
                        : '<span class="pv-done bad">✕ Missed · 做错过</span>')
                : '<span class="pv-done">Not tried · 未做</span>';
  let qimg, ans;
  if(isP){
    const p=String(q.p).padStart(3,'0');
    qimg=`<img src="pq/p${p}_q.jpg" alt="Question ${p}" loading="lazy">`;
    const imgs=`<div class="pv-aimg"><a href="pq/p${p}_a.jpg" target="_blank" title="Open full size">
        <img src="pq/p${p}_a.jpg" alt="Printed answer" loading="lazy"></a></div>
      <details class="pv-det"><summary>Printed solution 打印解答 <span class="tz">展开查看</span></summary>
        <div class="pv-simg"><a href="pq/p${p}_s.jpg" target="_blank" title="Open full size">
          <img src="pq/p${p}_s.jpg" alt="Printed solution" loading="lazy"></a></div>
      </details>`;
    if(q.a){
      ans=`<div class="pv-ans">Answer: <b>${q.a}</b> <span class="tz">答案 · 自动判分</span></div>`+imgs;
    } else {
      ans=`<div class="pv-note">Self-marked · 原题无标准选项，答案取自原卷打印行
        <span class="tz">printed answer, not a reconstructed letter · 答案取自原卷打印行，非反推的选项字母</span></div>
      <div class="pv-ans">Answer · 打印答案行 <span class="tz">答案以下图为准</span></div>`+imgs;
    }
  } else {
    const n=String(q.id).padStart(3,'0');
    qimg=`<img src="q/q${n}.png" alt="Question ${q.id}" loading="lazy">`;
    ans=`<div class="pv-ans">Answer: <b>${q.a}</b> <span class="tz">答案</span></div>
      <details class="pv-det"><summary>Solution 解析 <span class="tz">展开查看</span></summary>
        <div class="sol">
          <div class="col"><div class="lb">Solution</div>${q.en}</div>
          <div class="col zh"><div class="lb">中文解析</div>${q.zh}</div>
          ${q.focus? `<div class="col"><div class="lb">Focus 考点</div>${q.focus}</div>`:''}
          ${q.trap? `<div class="col"><div class="lb">Trap 易错点</div>${q.trap}</div>`:''}
        </div>
      </details>`;
  }
  return `<article class="pv-card" data-id="${id}" id="pv${id}">
    <div class="pv-hd">
      <span class="qno${isP?' pq':''}">${badge}</span>
      <span class="pv-sec" title="${q.s} · ${sec.en} · ${sec.zh}">${q.s} · ${sec.en}<span class="tz"> ${sec.zh}</span></span>
      ${starBtn(id)}
      ${done}
    </div>
    <div class="pv-img">${qimg}</div>
    ${ans}
    <div class="pv-ft">
      <button class="btn ghost" onclick="startSingle(${id})">Practice this <span class="zhx">做这题</span></button>
      ${favBtn(id)}
    </div>
  </article>`;
}

function pvPaint(){
  const g=document.getElementById('pvGrid'), c=document.getElementById('pvCards');
  if(!g||!c) return;
  const list=pvList();
  const pages=Math.max(1,Math.ceil(list.length/PV_PER));
  if(pvPage>=pages) pvPage=pages-1;
  if(pvPage<0) pvPage=0;
  const page=list.slice(pvPage*PV_PER,(pvPage+1)*PV_PER);
  g.innerHTML=list.map(it=>{
    const r=store.h[it.id], st=r?(r.ok?'ok':'bad'):'new';
    return `<button class="idx-b ${st}${it.p?' p':''}${isFav(it.id)?' fav':''}" onclick="pvGo(${it.id})"
      title="${it.lb} · ${it.s}"><b>${it.lb}</b><i>${it.s}</i>${r?(r.ok?'<u>✓</u>':'<u>✕</u>'):''}</button>`;
  }).join('') || '<p class="muted" style="grid-column:1/-1">No item in this slice.</p>';
  c.innerHTML=list.length? page.map(it=>previewCard(it.id)).join('')
    : `<div class="card pv-empty">
        <div style="font-size:30px">☆</div>
        <h3 style="margin:8px 0 4px">${pvScope==='fav'? 'No favourites yet' : 'Nothing matches'}</h3>
        <p class="muted">${pvScope==='fav'
          ? 'Tap the ★ on any question to keep it here — answers are shown straight away.'
          : 'Try another type, chapter or search term.'}</p>
        <p class="muted"><span class="zhx">${pvScope==='fav'
          ? '在任何题上点 ★ 即可加入收藏夹，这里会直接显示答案。' : '换个类型、章节或关键词试试。'}</span></p>
        <button class="btn ghost" style="margin-top:10px" onclick="route('browse')">Browse the bank <span class="zhx">去题库</span></button>
      </div>`;
  const meta=document.getElementById('pvMeta');
  if(meta) meta.textContent=list.length
    ? `${list.length} item${list.length===1?'':'s'} · page ${pvPage+1}/${pages} ／ 共 ${list.length} 题，第 ${pvPage+1}/${pages} 页`
    : '0 items ／ 共 0 题';
  const pager=document.getElementById('pvPager');
  if(pager) pager.innerHTML=`
    <button class="btn ghost" ${pvPage<=0?'disabled':''} onclick="pvPageGo(${pvPage-1})">&larr; Prev <span class="zhx">上一页</span></button>
    <span class="muted">Page ${pvPage+1} / ${pages}</span>
    <button class="btn ghost" ${pvPage>=pages-1?'disabled':''} onclick="pvPageGo(${pvPage+1})">Next <span class="zhx">下一页</span> &rarr;</button>`;
  renderMath();
}

function renderPv(mode){
  pvMode=mode; pvScope= mode==='fav'? 'fav':'all';
  if(pvScope==='fav' && pvType==='fav') pvType='all';
  const favOnly=pvScope==='fav';
  const types = favOnly
    ? [['all','All favourites <span class="zhx">全部收藏</span> '+favCount()],
       ['q','Compiled <span class="zhx">精编</span>'],
       ['p','Originals <span class="zhx">原题</span>']]
    : [['all','All <span class="zhx">全部</span> '+UNI.length],
       ['q','Compiled <span class="zhx">精编</span> '+ITEMS.length],
       ['p','Originals <span class="zhx">原题</span> '+PQ.length],
       ['fav','★ Favourites <span class="zhx">收藏</span> '+favCount()]];
  const typeHtml=types.map(([k,t])=>`<button class="${pvType===k?'on':''}" onclick="pvSetType('${k}')">${t}</button>`).join('');
  const chHtml=['<button class="'+(pvCh==='all'?'on':'')+'" onclick="pvSetCh(\'all\')">All chapters <span class="zhx">全部章节</span></button>']
    .concat(CHS.map((c,i)=>`<button class="${pvCh===i?'on':''}" onclick="pvSetCh(${i})">Ch ${i+1}</button>`)).join('');
  const tools = favOnly
    ? `<div class="pv-tools">
        <span class="chip">★ <b data-fav-count>${favCount()}</b> starred <span class="zhx">已收藏</span></span>
        ${favCount()? '<button class="btn ghost" onclick="clearFav()">Clear all <span class="zhx">清空</span></button>':''}
        <button class="btn ghost" onclick="route('preview')">Full preview <span class="zhx">题库速览</span></button>
      </div>`
    : '';
  document.getElementById('view').innerHTML=`
  <div class="wrap pv-wrap">
    <div class="pv-hd2">
      <h2>${favOnly? 'Favourites <span class="tz">收藏夹</span>' : 'Preview <span class="tz">题库速览</span>'}</h2>
      <span class="muted">${favOnly? 'Your starred items · 只看收藏题'
        : 'Browse the whole bank · 通览全部 674 题'}</span>
    </div>
    <p class="pv-sub">Answers shown immediately — no answering, no scoring · 直接看题与答案，不记分</p>
    ${tools}
    <div class="card" style="padding:14px 16px">
      <div class="filter" id="pvType">${typeHtml}</div>
      <div class="filter" id="pvCh">${chHtml}</div>
      <div class="idxsearch"><input id="pvQ" value="${pvEsc(pvQ)}"
        placeholder="Find 12 / Q12 / P7 / 2.5 / a topic name · 搜题号、考点或名称"
        oninput="pvSetQ(this.value)"></div>
      <div class="pv-count" id="pvMeta"></div>
      <div class="idxgrid pv-grid" id="pvGrid"></div>
    </div>
    <div class="pv-cards" id="pvCards"></div>
    <div class="pv-pager" id="pvPager"></div>
    <div style="margin:6px 0 40px"><button class="btn ghost" onclick="route('home')">Back <span class="zhx">返回</span></button></div>
  </div>`;
  pvPaint();
  paintTop();
}

function viewPreview(){ pvPage=0; renderPv('preview'); }
function viewFav(){ pvPage=0; renderPv('fav'); }

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
  if(e.target && /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) return;
  const L=['a','b','c','d','e'], k=e.key.toLowerCase();
  if(k==='f'){
    const m=document.getElementById('mAcct');
    if(m && m.classList.contains('on')) return;
    const id=currentFavId();
    if(id!=null){ e.preventDefault(); toggleFav(id); }
    return;
  }
  const solo = round.mode==='smart' && round.list.length===1;
  if(L.includes(k)){ const b=[...document.querySelectorAll('.opt')][L.indexOf(k)];
    if(b&&!b.disabled) b.click(); }
  if(solo && k==='s'){ skipQ(); return; }
  if(solo && k==='t'){ skipSec(); return; }
  if(e.key==='Enter'){ const n=[...document.querySelectorAll('.btn.pri')].pop(); if(n) n.click(); }
});
/* Deep links survive a reload. replaceState never fires hashchange, so the
   listener below cannot recurse; quiz/res are deliberately not in the map. */
const HASHROUTE={'#home':'home','#ref':'ref','#bank':'browse','#preview':'preview','#fav':'fav'};
window.addEventListener('hashchange',()=>{ const v=HASHROUTE[location.hash]; if(v) route(v); });

/* ---------- admin answer overrides ----------
   The admin console can correct an answer letter.  The endpoint only ever
   returns valid A-E letters — clearing an override simply drops the row, so the
   built-in answer stays in force.  That is why we never assign `null` here: for
   a compiled item it would erase the built-in letter and `L===q.a` could never
   be true again, leaving the question unanswerable forever.

   Apply on every successful fetch (assigning a value twice is harmless) and only
   repaint when a letter actually changed.  We deliberately do NOT cache the
   version to skip work: a skipped apply is a silently stale answer. */
function applyOverrides(){
  return api('api/overrides').then(r=>{
    if(!r || !r.ok || !r.d || !Array.isArray(r.d.rows)) return;
    let changed=false;
    r.d.rows.forEach(row=>{
      const q=BYID[row.id];
      if(q && /^[A-E]$/.test(row.a||'') && q.a!==row.a){ q.a=row.a; changed=true; }
    });
    if(!changed) return;
    // Answer letters are printed on the preview / favourites board: refresh it.
    // Never repaint a quiz here — an in-flight round must keep its revealed state.
    if(curView==='preview') viewPreview();
    else if(curView==='fav') viewFav();
  });
}

paintTop(); viewHome(); renderMath();
if(location.hash==='#pq') start('pq');
else if(location.hash==='#ref') route('ref');
else if(location.hash==='#bank') route('browse');
else if(location.hash==='#preview') route('preview');
else if(location.hash==='#fav') route('fav');
if(CAN_API) applyOverrides();
bootAcct().then(()=>paintTop());
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
