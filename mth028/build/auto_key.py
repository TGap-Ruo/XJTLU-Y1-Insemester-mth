#!/usr/bin/env python3
"""Auto-grade choice questions by matching answer numbers against option numbers.

For each choice question that lacks a suggested_key, extract the numeric tokens
from the "The correct answer is:" box and from each option row, then pick the
option whose multiset of numbers best matches the answer.  This handles matrix
answers (vectors / systems) where OCR text is garbled but the digit glyphs
are clean.

Writes back into data/quiz_structured.json: suggested_key, key_confidence,
key_method.
"""
import json, os, re, sys
from collections import Counter
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
SRC = os.path.join(os.path.dirname(ROOT), "mth028-material", "MTH028-Quizzes")
if not os.path.isdir(SRC):
    # fallback: sibling directory
    SRC = os.path.join(os.path.dirname(ROOT), "mth028-material", "MTH028-Quizzes")

NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")

def nums_near(page, y_lo, y_hi, x_lo=0, x_hi=9999):
    """Collect numeric word tokens in a y-band on the page."""
    out = []
    for w in page.get_text("words"):
        x0, y0, x1, y1, t = w[0], w[1], w[2], w[3], w[4]
        if y_lo <= y0 <= y_hi and x_lo <= x0 <= x_hi:
            t2 = t.replace("−", "-").strip()
            if NUM_RE.match(t2):
                out.append(t2)
    return out

def score(ans_nums, opt_nums):
    """Overlap score between two number multisets (higher = better match)."""
    a, o = Counter(ans_nums), Counter(opt_nums)
    if not a:
        return 0.0
    inter = sum((a & o).values())
    return inter / max(len(a), 1)

def main():
    idx = json.load(open(os.path.join(D, "quiz_index.json")))
    qs = json.load(open(os.path.join(D, "quiz_structured.json")))
    items = qs["items"]
    by_qid = {x["qid"]: x for x in items}

    docs = {qi: pymupdf.open(os.path.join(SRC, "%d.pdf" % qi)) for qi in range(1, 11)}

    fixed = 0
    for r in idx:
        if r["type"] != "choice":
            continue
        qid = r["qid"]
        s = by_qid.get(qid, {})
        if s.get("suggested_key"):
            continue  # already has a key
        if not r.get("correct"):
            continue  # no printed answer -> can't auto-grade
        page = docs[r["quiz"]][r["correct"][0][0]]
        ay = r["correct"][0][1]

        # answer numbers: band around the "correct" anchor (±40pt covers 3-row matrices)
        ans = nums_near(page, ay - 35, ay + 40)
        if not ans:
            continue

        # option numbers: each option row ±30pt around its y anchor
        best_L, best_sc = None, -1
        for opt in r.get("options", []):
            oy = opt["y"]
            on = nums_near(page, oy - 15, oy + 50)
            sc = score(ans, on)
            if sc > best_sc:
                best_sc, best_L = sc, opt["L"]

        if best_L and best_sc >= 0.6:
            s["suggested_key"] = best_L
            s["key_confidence"] = "high" if best_sc >= 0.85 else "medium"
            s["key_method"] = "number-match"
            fixed += 1
            print(f"  {qid}: key={best_L} score={best_sc:.2f} ans={ans}")
        elif best_L:
            s["suggested_key"] = best_L
            s["key_confidence"] = "low"
            s["key_method"] = "number-match"
            print(f"  {qid}: key={best_L} LOW score={best_sc:.2f} ans={ans}")

    json.dump(qs, open(os.path.join(D, "quiz_structured.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"\nFixed {fixed} choice questions.")

if __name__ == "__main__":
    main()
