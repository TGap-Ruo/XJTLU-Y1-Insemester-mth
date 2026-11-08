#!/usr/bin/env python3
"""Map the 150 quiz items onto the MTH028 slide topics (1.1 - 1.9).

Classification is by the vocabulary of the printed stem, following the
section titles of the course slides / Lay chapter 1.  It is deliberately a
*best-effort* mapping: each row also records the matched keywords so a human
can audit or re-map it later.  Adding new items later needs no code change:
just add another line to data/topic_map.json (or leave it to be inferred).

Output: data/topic_map.json
"""
import json
import os
import re
import pymupdf

ROOT = "/Users/zhj/WorkBuddy/2026-11-05-22-50-04/mth028"
SRC = os.path.join(os.path.dirname(ROOT), "mth028-material", "MTH028-Quizzes")
INDEX = os.path.join(ROOT, "data", "quiz_index.json")
OUT = os.path.join(ROOT, "data", "topic_map.json")

# (topic id, [weighted keyword patterns]) -- order = priority when tied
RULES = [
    ("1.9", [r"standard matrix", r"matrix of (the |a )?linear transformation",
             r"rotation", r"shear", r"projection (onto|matrix)",
             r"the transformation .{0,30}matrix"]),
    ("1.8", [r"linear transformation", r"transformation\s+T\b", r"\bdomain\b",
             r"\bcodomain\b", r"\brange of\b", r"image of", r"mapping\s+T",
             r"one.to.one", r"onto\b"]),
    ("1.7", [r"linearly (in|de)pendent", r"linear (in|de)pendence",
             r"dependence relation", r"set (is|of) (not )?linearly",
             r"linear dependence"]),
    ("1.5", [r"homogeneous", r"nontrivial solution", r"trivial solution",
             r"parametric vector form", r"general solution (of|to|in)",
             r"solution set.{0,40}span", r"write the general solution"]),
    ("1.4", [r"\bAx\s*=\s*b\b", r"matrix.vector product", r"identity matrix",
             r"matrix equation", r"existence (of|and)", r"consistent for (all|every)",
             r"span\{?.{0,20}\}?.{0,30}R", r"does not span",
             r"computetheproduct", r"computethematrixproduct",
             r"findtheproduct", r"matrixproduct"]),
    ("1.3", [r"linear combination", r"\bspan(s|ning|ned)?\b", r"vector equation",
             r"column vector", r"\bweights?\b", r"subset spanned", r"v[1-4]\s*=",
             r"computethevector", r"findthevector", r"writeavectorequation"]),
    ("1.2", [r"echelon form", r"\bRREF\b", r"\bREF\b", r"pivot", r"leading entr",
             r"basic variable", r"free variable", r"row reduc", r"row echelon",
             r"reduced row", r"backward phase", r"forward phase"]),
    ("1.1", [r"augmented matrix", r"coefficient matrix", r"consistent",
             r"inconsistent", r"row (operation|replace|interchange|scaling)",
             r"replace row", r"elementary row", r"system (is|of linear|corresponds)",
             r"solution of the system", r"row equivalent"]),
]
FALLBACK = "1.1"     # systems / row operations is the safest home for the rest


def stem_text(doc, pno, y0, y1):
    """Readable stem text from the question card (ignore broken glyph spans)."""
    page = doc[pno]
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                y, t = s["bbox"][1], s["text"]
                if not (y0 < y < y1) or not t.strip():
                    continue
                if any(0xE000 <= ord(c) <= 0xF8FF for c in t):
                    continue
                out.append((round(y, 1), s["bbox"][0], t))
    out.sort()
    lines = []
    for y, x, t in out:
        if lines and abs(y - lines[-1][0]) <= 2.0:
            lines[-1][1].append((x, t))
        else:
            lines.append([y, [(x, t)]])
    txt = " ".join("".join(t for _, t in sorted(parts)) for _, parts in lines)
    txt = re.sub(r"\s+", " ", txt)
    # drop the Moodle chrome
    txt = re.sub(r"(?i)question\s+\d+|select one:|correct|incorrect|"
                 r"your answer is|the correct answer is|answer:", " ", txt)
    return txt.strip()[:700]


def classify(txt):
    """The PDF text layer drops spaces ("augmentedmatrix"), so score both the
    spaced text and a whitespace-stripped variant against de-spaced patterns."""
    low = txt.lower()
    squashed = re.sub(r"\s+", "", low)
    scored = []
    for sec, pats in RULES:
        n = 0
        for p in pats:
            if re.search(p, low) or re.search(re.sub(r"\s+", "", p), squashed):
                n += 1
        scored.append((n, -RULES.index((sec, pats)), sec))
    scored.sort(reverse=True)
    hits, _, sec = scored[0]
    return (sec if hits else FALLBACK), hits


def main():
    rows = json.load(open(INDEX))
    docs = {q: pymupdf.open(os.path.join(SRC, "%d.pdf" % q)) for q in range(1, 11)}
    res, dist = [], {}
    for r in rows:
        p0, y0 = r["head"]["p"], r["head"]["y"] + 58
        stops = [806]
        for key in ("verdict", "correct", "answer_input"):
            stops += [y for p, y in r[key] if p == p0 and y > y0]
        if r["next"]["p"] == p0 and r["next"]["y"] > y0:
            stops.append(r["next"]["y"])
        y1 = min(stops) - 8
        txt = stem_text(docs[r["quiz"]], p0, y0, y1)
        sec, conf = classify(txt)
        dist[sec] = dist.get(sec, 0) + 1
        res.append({"qid": r["qid"], "quiz": r["quiz"], "qno": r["qno"],
                    "topic": sec, "confidence": conf, "stem": txt})
    json.dump({"mapping": res,
               "note": "best-effort classification from printed stems; edit this file to override any item"},
              open(OUT, "w"), ensure_ascii=False, indent=1)
    print("mapped", len(res), "items")
    for k in sorted(dist): print("  %-4s %3d" % (k, dist[k]))
    print("low-confidence (0 keywords):", sum(1 for x in res if x["confidence"] == 0))
    print("saved", OUT)


if __name__ == "__main__":
    main()
