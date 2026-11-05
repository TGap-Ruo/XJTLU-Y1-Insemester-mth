# -*- coding: utf-8 -*-
"""合并 → 打乱选项 → 输出 out/questions.json"""
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import typeinfo
import q_l1, q_l2, q_l3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")
os.makedirs(OUT, exist_ok=True)

raw = q_l1.Q + q_l2.Q + q_l3.Q
rng = random.Random(20261105)
items = []
for i, it in enumerate(raw):
    opts = [it["c"]] + it["w"]
    assert len(opts) == 4, (it["t"], len(opts))
    idx = list(range(4))
    rng.shuffle(idx)
    shuffled = [opts[j] for j in idx]
    ans = idx.index(0)
    t = typeinfo.TYPE_BY_ID[it["t"]]
    items.append(dict(
        id=f"Q{i+1:03d}", type=it["t"], lec=t["lec"], sec=t["sec"], diff=t["diff"],
        stem=it["q"], options=shuffled, answer=ans, sol=it["s"],
    ))

# 统计
from collections import Counter
cnt = Counter(x["type"] for x in items)
for t in typeinfo.TYPES:
    assert cnt[t["id"]] >= 3, (t["id"], cnt[t["id"]])

data = dict(types=typeinfo.TYPES, chapters=typeinfo.CHAPTERS, questions=items)
with open(os.path.join(OUT, "questions.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

print("题型", len(typeinfo.TYPES), "题目", len(items))
print("各讲题量:", dict(Counter(x["lec"] for x in items)))
print("每题量范围:", min(cnt.values()), "-", max(cnt.values()))
