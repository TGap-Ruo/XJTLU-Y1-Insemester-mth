#!/usr/bin/env python3
"""Diagnose the Moodle review-page layout of MTH028 practice quizzes.

Prints, per page, the visual text lines with y coordinates so we can work out
where the question box starts/ends and where the printed answer box sits.
Read-only: writes nothing except stdout.
"""
import os
import re
import sys
import pymupdf

ROOT = "/Users/zhj/WorkBuddy/2026-11-05-22-50-04/mth028-material/MTH028-Quizzes"


def visual_lines(page, tol=2.0):
    """The PDF text layer splits glyphs into single-char spans. Cluster by y."""
    spans = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for s in line["spans"]:
                txt = s["text"]
                if not txt.strip():
                    continue
                y, x = s["bbox"][1], s["bbox"][0]
                if y < -100 or y > page.rect.height + 100:
                    continue  # off-page glyphs (broken matrix fonts)
                spans.append((y, x, txt))
    spans.sort()
    rows = []
    for y, x, t in spans:
        if rows and abs(y - rows[-1][0]) <= tol:
            rows[-1][1].append((x, t))
        else:
            rows.append([y, [(x, t)]])
    return [(round(y, 1), "".join(t for _, t in sorted(parts))) for y, parts in rows]


def main():
    which = sys.argv[1:] or ["1.pdf", "6.pdf", "10.pdf"]
    for name in which:
        path = os.path.join(ROOT, name)
        doc = pymupdf.open(path)
        print("=" * 78)
        print(name, "pages", len(doc), "rect", doc[0].rect)
        for pno in range(len(doc)):
            lines = visual_lines(doc[pno])
            heads = [(y, t) for y, t in lines
                     if re.match(r"^Question\s+\d+", t) or "correct answer is" in t.lower()
                     or re.match(r"^Answer:", t) or re.match(r"^[A-E]\.\s", t)]
            first = lines[0][1][:50] if lines else ""
            print("p%-2d lines=%-3d  %s" % (pno + 1, len(lines), heads[:8]))
            if pno == 0:
                for y, t in lines[:60]:
                    print("      y=%6.1f |%s" % (y, t[:96]))


if __name__ == "__main__":
    main()
