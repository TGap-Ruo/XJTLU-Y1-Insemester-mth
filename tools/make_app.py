# -*- coding: utf-8 -*-
"""打包单文件刷题器 HTML（内联 KaTeX + 题库）"""
import base64, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, OUT, ASSETS

tpl = open(os.path.join(ROOT, "build", "app_template.html"), encoding="utf-8").read()

css = open(os.path.join(ASSETS, "katex.min.css"), encoding="utf-8").read()


def inline_font(m):
    f = m.group(1)
    p = os.path.join(ASSETS, "fonts", f)
    if not os.path.exists(p):
        return "url()"
    b = base64.b64encode(open(p, "rb").read()).decode()
    return 'url(data:font/woff2;base64,%s) format("woff2")' % b


css = re.sub(r'url\(fonts/([A-Za-z0-9_-]+\.woff2)\) format\("woff2"\)', inline_font, css)
# 去掉 woff / ttf 回退（避免额外体积与错误引用）
css = re.sub(r',url\(fonts/[A-Za-z0-9_-]+\.(woff|ttf)\) format\("(woff|truetype)"\)', "", css)

katex_js = open(os.path.join(ASSETS, "katex.min.js"), encoding="utf-8").read()
auto = open(os.path.join(ASSETS, "auto-render.min.js"), encoding="utf-8").read()

data = json.load(open(os.path.join(OUT, "questions.json"), encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

html = tpl.replace("__KATEX_CSS__", css)
html = html.replace("__KATEX_JS__", katex_js + "\n" + auto)
html = html.replace("__DATA__", "const DATA=" + payload + ";")

if os.environ.get("DEBUG_JS"):
    html = html.replace("<head>", """<head><script>
window.addEventListener('error',function(e){var d=document.createElement('pre');
d.style.cssText='position:fixed;bottom:0;left:0;right:0;background:#fee;color:#900;padding:14px;font-size:12px;z-index:9999;white-space:pre-wrap';
d.textContent='ERROR: '+e.message+' @ '+(e.filename||'')+':'+(e.lineno||'')+' | '+(e.error&&e.error.stack||'');(document.body||document.documentElement).appendChild(d);});
</script>""")

dst = os.path.join(OUT, "MTH026_SmartQuiz.html")
open(dst, "w", encoding="utf-8").write(html)
print("写入 %.2f MB → %s" % (len(html.encode()) / 1048576, dst))
