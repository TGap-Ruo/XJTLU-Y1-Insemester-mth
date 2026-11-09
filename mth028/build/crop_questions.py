#!/usr/bin/env python3
"""Render each MTH028 question as a clean question image (no answers leaked).

Facts established by the PDF reconnaissance (do not "simplify" these away):

* The ten PDFs are Moodle *attempt review* pages.  Every question prints a
  Correct/Incorrect status, the student's selected radio / filled values, a
  green tick next to the right option, a verdict line and (usually) an orange
  "The correct answer is:" box.
* Questions NEVER span a page (CSS page-break-inside:avoid).  A later page is
  the NEXT question, not a continuation.  So each crop uses exactly one page.
* Stretchy matrix brackets have absurd span bboxes (y0=-7695).  Never build a
  clip from span bboxes; use fixed y windows derived from search_for anchors.
* The selection radio is GREY, not green.  Colour filtering alone leaves it
  behind (it gives away the student's pick).  Wipe the radio column and the
  tick/cross glyphs by their exact PDF rectangles.

Outputs out/img/q/q<quiz>-<no>.png, out/img/a/q<quiz>-<no>.png and data/crops.json.
"""
import json
import os
import re
import pymupdf
from PIL import Image, ImageDraw

ROOT = "/Users/zhj/WorkBuddy/2026-11-05-22-50-04/mth028"
SRC = os.path.join(os.path.dirname(ROOT), "mth028-material", "MTH028-Quizzes")
INDEX = os.path.join(ROOT, "data", "quiz_index.json")
QDIR = os.path.join(ROOT, "out", "img", "q")
ADIR = os.path.join(ROOT, "out", "img", "a")
SCALE = 2.0
LEFT, RIGHT = 32.0, 566.0
FOOTER_Y = 806.0
MAX_W = 1400


def page_marks(page):
    """Rectangles (PDF coords) that must be whitewashed on a question crop."""
    rects = []
    # PUA tick / cross glyphs: \uf058 (right), \uf057 (wrong), sometimes \uf05a
    for w in page.get_text("words"):
        x0, y0, x1, y1, txt = w[0], w[1], w[2], w[3], w[4]
        if any(0xE000 <= ord(c) <= 0xF8FF for c in txt):
            rects.append((x0 - 3, y0 - 3, x1 + 3, y1 + 3))
    # radios sit in a narrow left column; wipe that column on option rows only
    for w in page.get_text("words"):
        x0, y0, x1, y1, txt = w[0], w[1], w[2], w[3], w[4]
        if re.fullmatch(r"[A-E]\.", txt) and x0 < 110:
            rects.append((36, y0 - 4, min(x0 - 3, 70), y1 + 6))
    # the coloured "Correct"/"Incorrect" status text under the Question header
    for r in page.search_for("Correct") + page.search_for("Incorrect"):
        if r.y0 < 120:
            rects.append((r.x0 - 2, r.y0 - 2, r.x1 + 2, r.y1 + 2))
    return rects


def render(doc, pno, y0, y1, path, wipe=False):
    if y1 - y0 < 20:
        return None
    page = doc[pno]
    clip = pymupdf.Rect(LEFT, max(0, y0), RIGHT, min(page.rect.height, y1))
    pix = page.get_pixmap(matrix=pymupdf.Matrix(SCALE, SCALE), clip=clip, alpha=False)
    pix.save(path)
    im = Image.open(path).convert("RGB")
    if wipe:
        draw = ImageDraw.Draw(im)
        # 1) header + status rows ("Question N" / "Correct"), always first ~62pt
        draw.rectangle((0, 0, im.width, min(im.height, int(60 * SCALE))), fill="white")
        # 2) exact rectangles in PDF space -> image space
        for (a, b, c, d) in page_marks(page):
            box = (int((a - LEFT) * SCALE), int((b - y0) * SCALE),
                   int((c - LEFT) * SCALE), int((d - y0) * SCALE))
            if box[2] > 0 and box[3] > 0 and box[0] < im.width and box[1] < im.height:
                draw.rectangle(box, fill="white")
        # 3) any remaining saturated green/red/blue mark (anti-aliased edges)
        px = im.load()
        for yy in range(im.height):
            for xx in range(im.width):
                r, g, bl = px[xx, yy][:3]
                green = g > 70 and g > r * 1.22 and g > bl * 1.22
                red = r > 90 and r > g * 1.35 and r > bl * 1.35
                blue = bl > 110 and bl > r * 1.30 and bl > g * 1.12
                if (green or red or blue) and max(r, g, bl) - min(r, g, bl) > 32:
                    px[xx, yy] = (255, 255, 255)
    if im.width > MAX_W:
        im = im.resize((MAX_W, int(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(path, optimize=True)
    return (im.width, im.height)


def main():
    rows = json.load(open(INDEX))
    os.makedirs(QDIR, exist_ok=True)
    os.makedirs(ADIR, exist_ok=True)
    docs = {qi: pymupdf.open(os.path.join(SRC, "%d.pdf" % qi)) for qi in range(1, 11)}
    manifest = []
    for r in rows:
        qi, qno = r["quiz"], r["qno"]
        doc = docs[qi]
        p0, y0 = r["head"]["p"], r["head"]["y"]
        p1, y1 = r["next"]["p"], r["next"]["y"]
        stops = [FOOTER_Y]
        for key in ("verdict", "correct"):
            stops += [y for p, y in r[key] if p == p0 and y > y0 + 20]
        if p1 == p0 and y1 > y0 + 20:
            stops.append(y1)
        bottom = min(stops) - 15          # keep clear of the orange answer box
        top = y0 - 6
        qpath = "%s/q%d-%02d.png" % (QDIR, qi, qno)
        got = render(doc, p0, top, bottom, qpath, wipe=True)
        ans_img = None
        if r["correct"]:
            ap, ay = r["correct"][0]
            af = "%s/q%d-%02d.png" % (ADIR, qi, qno)
            # Anchor y is the "The correct answer is:" baseline; tall matrices
            # extend ~25pt above it, so widen upward (old ay-6 cut the top row).
            if render(doc, ap, max(0, ay - 30), min(ay + 55, FOOTER_Y), af):
                ans_img = "img/a/q%d-%02d.png" % (qi, qno)
        manifest.append({
            "qid": r["qid"], "quiz": qi, "qno": qno, "type": r["type"],
            "has_printed_answer": r["has_printed_answer"],
            "printed_answer_text": r["printed_answer_text"],
            "img": "img/q/q%d-%02d.png" % (qi, qno) if got else None,
            "answer_img": ans_img,
            "head": r["head"], "next": r["next"],
            "crop": {"p": p0, "y0": round(top, 1), "y1": round(bottom, 1)},
        })
    json.dump(manifest, open(os.path.join(ROOT, "data", "crops.json"), "w"),
              ensure_ascii=False, indent=1)
    ok = [m for m in manifest if m["img"]]
    sizes = [os.path.getsize(os.path.join(ROOT, "out", m["img"])) for m in ok]
    print("question crops", len(ok), "/", len(manifest),
          "answer crops", sum(1 for m in manifest if m["answer_img"]))
    print("bytes min/max/total", min(sizes), max(sizes), sum(sizes) // 1024, "KB")


if __name__ == "__main__":
    main()
