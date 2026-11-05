# -*- coding: utf-8 -*-
"""共享样式与打印工具"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "out")
EDGE = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"

CSS = r"""
:root{
  --ink:#141b26; --ink2:#38455a; --ink3:#6b7a8f;
  --line:#dfe5ee; --line2:#eef2f7;
  --pri:#1d3f6e; --pri2:#2f6fb5; --pri-bg:#f2f6fc;
  --amber:#a9621a; --amber-bg:#fdf6ec;
  --green:#226b47; --green-bg:#f0f7f2;
  --red:#a23b30; --red-bg:#fbf1ef;
  --purple:#5b3f8f; --purple-bg:#f6f2fc;
}
*{box-sizing:border-box;-webkit-print-color-adjust:exact; print-color-adjust:exact;}
@page{ size:A4; margin:16mm 15mm 16mm 15mm; }
@page:first{ margin:0; }
html,body{margin:0;padding:0;}
body{
  font-family:"Songti SC","STSong","Source Han Serif SC",serif;
  font-size:10.2pt; line-height:1.78; color:var(--ink);
  background:#fff;
}
.page{ padding:0; }
h1,h2,h3,h4,.sans{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;}

/* ---------- 封面 ---------- */
.cover{height:297mm; position:relative; overflow:hidden; page-break-after:always;
  background:linear-gradient(160deg,#10233d 0%,#1d3f6e 46%,#2b5b96 100%); color:#fff; padding:0;}
.cover .grid{position:absolute; inset:0; opacity:.16;
  background-image:linear-gradient(rgba(255,255,255,.5) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.5) 1px,transparent 1px);
  background-size:26px 26px;}
.cover .glow{position:absolute; width:520px;height:520px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,214,140,.4),transparent 68%); right:-140px; top:-120px;}
.cover .inner{position:relative; padding:34mm 24mm 20mm 22mm; height:100%; display:flex; flex-direction:column;}
.cover .brand{font-family:"PingFang SC",sans-serif; font-size:10pt; letter-spacing:.42em; color:#bcd3ee; text-transform:uppercase;}
.cover .rule{width:56px;height:3px;background:#f0c479;margin:7mm 0 9mm;}
.cover h1{font-size:33pt; line-height:1.24; margin:0 0 5mm; font-weight:800; letter-spacing:.01em;}
.cover .sub{font-size:13pt; color:#d8e6f7; font-weight:300; letter-spacing:.06em; margin-bottom:2mm;}
.cover .sub2{font-size:10.5pt; color:#9fb9d8; letter-spacing:.04em;}
.cover .tags{display:flex; gap:6px; flex-wrap:wrap; margin-top:9mm;}
.cover .tag{font-family:"PingFang SC",sans-serif; font-size:8.6pt; padding:3px 9px; border:1px solid rgba(255,255,255,.34);
  border-radius:2px; color:#e2edf9; background:rgba(255,255,255,.07);}
.cover .meta{margin-top:auto; display:grid; grid-template-columns:repeat(2,1fr); gap:0; border-top:1px solid rgba(255,255,255,.22); padding-top:6mm;}
.cover .meta div{font-size:9pt; color:#a9c2dd; font-family:"PingFang SC",sans-serif; padding:2mm 0; line-height:1.6;}
.cover .meta b{display:block; font-size:12.5pt; color:#fff; font-family:"PingFang SC",sans-serif; font-weight:600; letter-spacing:.02em;}
.cover .stamp{position:absolute; right:22mm; bottom:24mm; font-family:"PingFang SC",sans-serif; font-size:8pt;
  color:#7e9ec2; letter-spacing:.3em;}

/* ---------- 章节封面 ---------- */
.chapter{page-break-before:always; padding-top:4mm;}
.ch-hero{background:linear-gradient(120deg,#1d3f6e,#2f6fb5); color:#fff; padding:11mm 12mm 9mm; border-radius:3px; position:relative; overflow:hidden;}
.ch-hero:after{content:attr(data-num); position:absolute; right:6mm; top:-8mm; font-family:"PingFang SC",sans-serif;
  font-size:96pt; font-weight:800; color:rgba(255,255,255,.13); letter-spacing:-.04em;}
.ch-hero .kicker{font-family:"PingFang SC",sans-serif; font-size:8.6pt; letter-spacing:.28em; color:#a9c9ea; margin-bottom:3mm;}
.ch-hero h2{margin:0; font-size:20pt; font-weight:800; letter-spacing:.02em;}
.ch-hero{margin-bottom:4mm;}
.ch-hero .desc{font-size:10pt; color:#cfe0f2; margin-top:3mm; font-family:"PingFang SC",sans-serif;}
.ch-hero .src{font-family:"PingFang SC",sans-serif; font-size:8.4pt; color:#9fc0e0; margin-top:5mm; letter-spacing:.02em;}
.hero-amber{background:linear-gradient(120deg,#6b3f14,#b5762a);}
.hero-amber .kicker{color:#f0d9b5;}
.hero-amber .desc{color:#f3e2c8;}

/* ---------- 标题层级 ---------- */
h2.sec{page-break-after:avoid; font-size:14.5pt; color:var(--pri); margin:9mm 0 4mm; padding-bottom:2.6mm; border-bottom:2px solid var(--pri); font-weight:700;}
h3.sub{page-break-after:avoid; font-size:11.6pt; color:var(--pri); margin:7mm 0 2.5mm; font-weight:700; padding-left:8px; border-left:3.5px solid var(--pri2);}
h4{font-size:10.4pt; margin:5mm 0 2mm; color:var(--ink); font-weight:700;}

/* ---------- 考点卡 ---------- */
.kp{border:1px solid var(--line); border-radius:3px; margin:0 0 6mm; page-break-inside:auto; overflow:hidden;}
.kp-h{page-break-after:avoid; display:flex; align-items:baseline; gap:3mm; background:var(--pri-bg); padding:3.2mm 4mm; border-bottom:1px solid var(--line);}
.kp-n{font-family:"PingFang SC",sans-serif; font-size:8.2pt; font-weight:700; color:#fff; background:var(--pri);
  padding:1.1mm 2.2mm; border-radius:2px; letter-spacing:.06em;}
.kp-t{font-family:"PingFang SC",sans-serif; font-size:11pt; font-weight:700; color:var(--pri); flex:1;}
.kp-a{font-family:"PingFang SC",sans-serif; font-size:7.8pt; color:var(--ink3); white-space:nowrap;}
.kp-b{padding:3.6mm 4mm 4mm;}
.kp-b p{margin:0 0 2.2mm;}
.kp-b ul{margin:1mm 0 2.4mm; padding-left:5.2mm;}
.kp-b li{margin:0.8mm 0;}
.lead{font-weight:700; color:var(--pri); font-family:"PingFang SC",sans-serif; font-size:9.4pt;}

/* ---------- 公式盒 ---------- */
.fbox{page-break-inside:avoid; background:#f7f9fc; border:1px solid var(--line); border-left:3px solid var(--pri2); border-radius:2px;
  padding:3mm 4mm; margin:2.5mm 0 3mm; font-size:10pt; page-break-inside:avoid;}
.fbox .t{font-family:"PingFang SC",sans-serif; font-size:8.4pt; color:var(--pri2); letter-spacing:.14em; margin-bottom:1.6mm; font-weight:700;}
.fbox .row{display:flex; flex-wrap:wrap; gap:0 6mm;}
.fbox .row>span{min-width:44%;}

/* ---------- 提示条 ---------- */
.tip{border-radius:2px; padding:2.6mm 3.6mm; margin:2.5mm 0; font-size:9.4pt; page-break-inside:avoid;
  border-left:3px solid; background:#fafbfd;}
.tip b{font-family:"PingFang SC",sans-serif; font-size:8.6pt; letter-spacing:.06em;}
.tip.warn{border-color:var(--red); background:var(--red-bg);} .tip.warn b{color:var(--red);}
.tip.how{border-color:var(--amber); background:var(--amber-bg);} .tip.how b{color:var(--amber);}
.tip.link{border-color:var(--purple); background:var(--purple-bg);} .tip.link b{color:var(--purple);}

/* ---------- 表格 ---------- */
table{width:100%; border-collapse:collapse; margin:3mm 0 4mm; font-size:9pt; page-break-inside:auto;}
thead{display:table-header-group;}
tr{page-break-inside:avoid;}
th{background:var(--pri); color:#fff; font-family:"PingFang SC",sans-serif; font-weight:600; font-size:8.6pt;
  padding:2.2mm 2.4mm; text-align:left; letter-spacing:.02em;}
td{padding:1.9mm 2.4mm; border-bottom:1px solid var(--line2); vertical-align:top;}
tr:nth-child(even) td{background:#fafbfd;}
table.compact td{padding:1.4mm 2.2mm; font-size:8.6pt;}

/* ---------- 例题 ---------- */
.ex{border:1px solid var(--line); border-radius:3px; margin:3mm 0; page-break-inside:auto;}
.ex-h{page-break-after:avoid; background:#f4f7fb; padding:2.2mm 3.4mm; font-family:"PingFang SC",sans-serif; font-size:8.6pt;
  color:var(--pri); font-weight:700; letter-spacing:.04em; border-bottom:1px solid var(--line); display:flex; justify-content:space-between;}
.ex-b{padding:3mm 3.4mm; font-size:9.6pt;}
.ex-b .q{margin-bottom:2mm;}
.ex-b .a{background:var(--green-bg); border-left:3px solid var(--green); padding:2.2mm 3mm; margin-top:2mm; font-size:9.4pt;}
.ex-b .a b{font-family:"PingFang SC",sans-serif; color:var(--green); font-size:8.4pt; letter-spacing:.08em;}
.stars{color:#d99a2b; letter-spacing:.06em; font-size:9pt;}
.toc-row{display:flex; align-items:baseline; font-size:9.6pt; padding:2.1mm 0; border-bottom:1px dotted var(--line);}
.toc-row .n{width:9mm; color:var(--pri2); font-family:"PingFang SC",sans-serif; font-weight:700; font-size:9pt;}
.toc-row .t{flex:1;}
.toc-row .s{color:var(--ink3); font-size:8.4pt; font-family:"PingFang SC",sans-serif;}
.katex{font-size:1.02em;}
.katex-display{margin:2mm 0 !important;}
.pb{page-break-before:always;}
.nobreak{page-break-inside:avoid;}
.small{font-size:8.8pt; color:var(--ink2);}
.muted{color:var(--ink3);}
.hl{background:linear-gradient(transparent 62%, #fdeab8 62%); padding:0 1px;}
.center{text-align:center;}
.two-col{display:grid; grid-template-columns:1fr 1fr; gap:0 7mm;}
.stepline{display:flex; gap:3mm; margin:1.2mm 0; font-size:9.4pt; align-items:baseline;}
.stepline b{flex:0 0 5mm; height:5mm; line-height:5mm; text-align:center; border-radius:50%;
  background:#1d3f6e; color:#fff; font-family:"PingFang SC",sans-serif; font-size:7.6pt;}
.stepline span{flex:1;}
.steps{margin:2mm 0 0;}
.tc{border:1px solid var(--line); border-radius:3px; margin:0 0 6mm; page-break-inside:auto;}
.tc-h{display:flex; align-items:baseline; gap:3mm; padding:3mm 4mm; background:linear-gradient(90deg,#eef3fa,#f7fafd);
  border-bottom:1px solid var(--line); page-break-after:avoid;}
.tc-n{font-family:"PingFang SC",sans-serif; font-size:8.2pt; font-weight:700; color:#fff; background:#2f6fb5;
  padding:1.1mm 2.2mm; border-radius:2px; letter-spacing:.04em;}
.tc-t{font-family:"PingFang SC",sans-serif; font-size:11pt; font-weight:700; color:#1d3f6e; flex:1;}
.tc-m{font-family:"PingFang SC",sans-serif; font-size:7.8pt; color:#6b7a8f; white-space:nowrap;}
.tc-b{padding:3.4mm 4mm 4mm;}
.lbl{font-family:"PingFang SC",sans-serif; font-size:8pt; font-weight:700; letter-spacing:.1em; color:#2f6fb5;
  display:inline-block; margin:0 0 1.4mm;}
.lbl.g{color:#226b47;} .lbl.a{color:#a9621a;}

.selftest{border:1px solid #cfd9e6; border-radius:3px; margin:5mm 0 0; page-break-inside:auto; background:#fcfdff;}
.st-h{display:flex; justify-content:space-between; background:#eef3fa; border-bottom:1px solid #cfd9e6;
  padding:2.4mm 4mm; font-family:"PingFang SC",sans-serif; font-size:8.8pt; color:#1d3f6e; font-weight:700; letter-spacing:.08em;}
.st-b{padding:3.4mm 4mm 1mm; font-size:9.2pt;}
.st-k{border-top:1px dashed #cfd9e6; padding:2.4mm 4mm; font-size:8.8pt; color:#226b47;
  font-family:"PingFang SC",sans-serif; background:#f4faf6;}

.opts{display:grid; grid-template-columns:1fr 1fr; gap:1.2mm 5mm; margin:2mm 0 0; font-size:9.2pt;}
.opts>span{position:relative; padding-left:6mm; line-height:1.5;}
.opts>span b{position:absolute; left:0; top:0; color:#2f6fb5; font-family:"PingFang SC",sans-serif; font-size:8.4pt;}
.opts>span.ok{color:#1c5c3c; background:#eef7f1; border-radius:2px;}
.opts>span.ok b{color:#226b47;}
.ansline{margin-left:4mm; color:#226b47; font-weight:700; font-family:"PingFang SC",sans-serif; font-size:8.8pt;}
"""


def head(title):
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="file://{ASSETS}/katex.min.css">
<style>{CSS}</style>
</head><body>"""


def tail():
    return f"""<script src="file://{ASSETS}/katex.min.js"></script>
<script src="file://{ASSETS}/auto-render.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded",function(){{
  renderMathInElement(document.body,{{
    delimiters:[{{left:"$$",right:"$$",display:true}},{{left:"$",right:"$",display:false}}],
    throwOnError:false, strict:false
  }});
}});
</script></body></html>"""


def print_pdf(html_path, pdf_path):
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    # own profile dir: a running Edge window locks the default one and the
    # headless print then hangs until the timeout
    prof = "/tmp/mth026_edge_profile"
    cmd = [EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
           f"--user-data-dir={prof}",
           "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
           "--virtual-time-budget=12000",
           f"--print-to-pdf={pdf_path}", f"file://{html_path}"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=420)
    if not os.path.exists(pdf_path):
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit("PDF 生成失败")
    return pdf_path
