#!/usr/bin/env python3
"""Render the question and answer images for the selected MTH028 items.

The whole point of this version is that nothing is guessed: extract_v2.py reads
the exact card rectangles out of the PDF drawings, so

  question image = the stem card  (never the feedback card, never the header)
  answer   image = the feedback card (the worked solution + printed answer)

Whitewashing is then limited to what the CSS page printed *inside* the stem card
but a student must not see before answering:

  * the Correct / Incorrect / Not answered word  (it is in the header card, so
    normally out of frame -- handled anyway)
  * the radio buttons, which show which option the student picked
  * the tick / cross glyphs next to the correct option
  * the value typed into an answer input, inside its own box

Radios and input boxes are redrawn as neutral empty ones so the card still looks
like a Moodle question and not like a redacted document.

Output: out/img/q/<qid>.png, out/img/a/<qid>.png, data/crops.json
"""
import json
import os
import pymupdf
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAT = os.path.join(os.path.dirname(ROOT), "mth028-material")
D = os.path.join(ROOT, "data")
OUTBASE = os.path.join(ROOT, "out")
QDIR = os.path.join(OUTBASE, "img", "q")
ADIR = os.path.join(OUTBASE, "img", "a")
SCALE = 2.0
MAX_W = 1500
INSET = 2.0


def src_path(row):
    """Where the source PDF lives: three print styles, three folders."""
    if row.get("qid", "").startswith("h"):
        sub = "HJT"
    elif row.get("qid", "").startswith("b"):
        sub = "题库2"
    else:
        sub = "MTH028-Quizzes"
    return os.path.join(MAT, sub, row["file"])


def to_img(rect, clip, scale=SCALE):
    return ((rect[0] - clip.x0) * scale, (rect[1] - clip.y0) * scale,
            (rect[2] - clip.x0) * scale, (rect[3] - clip.y0) * scale)


def render(page, clip, path, radios, inputs, pua, grayscale_guard=True):
    pix = page.get_pixmap(matrix=pymupdf.Matrix(SCALE, SCALE), clip=clip, alpha=False)
    pix.save(path)
    im = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(im)

    for r in pua:                       # tick / cross glyphs
        box = to_img(r, clip)
        draw.rectangle((box[0] - 2.2 * SCALE, box[1] - 2.2 * SCALE,
                        box[2] + 2.2 * SCALE, box[3] + 2.2 * SCALE), fill="white")
    for r in inputs:                    # typed value, keep an empty box
        box = to_img(r, clip)
        draw.rectangle(box, fill="white", outline=(150, 165, 180), width=1)
    for r in radios:                    # chosen option, keep an empty radio
        box = to_img(r, clip)
        draw.rectangle((box[0] - 1, box[1] - 1, box[2] + 1, box[3] + 1), fill="white")
        draw.ellipse(box, outline=(170, 170, 170), width=max(1, int(1.2 * SCALE)))

    # belt and braces: any saturated colour left (anti-aliased tick edges) goes
    if grayscale_guard:
        a = np.asarray(im).astype(np.int16)
        r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        mx = a.max(axis=2)
        mn = a.min(axis=2)
        hot = ((mx - mn) > 34) & (mx > 90)
        a[hot] = [255, 255, 255]
        im = Image.fromarray(a.astype(np.uint8))

    if im.width > MAX_W:
        im = im.resize((MAX_W, int(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(path, optimize=True)
    return im.size


def main(src_json=None, out_root=None, ids=None):
    import sys
    rows = json.load(open(src_json or os.path.join(D, "selection.json")))
    if ids:
        want = {x.strip() for x in ids.split(",") if x.strip()}
        rows = [r for r in rows if r["qid"] in want]
    global OUTBASE, QDIR, ADIR
    if out_root:
        OUTBASE = os.path.abspath(out_root)
        QDIR = os.path.join(OUTBASE, "img", "q")
        ADIR = os.path.join(OUTBASE, "img", "a")
    os.makedirs(QDIR, exist_ok=True)
    os.makedirs(ADIR, exist_ok=True)
    docs, manifest = {}, []

    for r in rows:
        path = src_path(r)
        if path not in docs:
            docs[path] = pymupdf.open(path)
        page = docs[path][r["page"]]
        stem = pymupdf.Rect(*r["rects"]["stem"])
        clip = pymupdf.Rect(stem.x0 + INSET, stem.y0 + INSET,
                            stem.x1 - INSET, stem.y1 - INSET)
        radios = [pymupdf.Rect(*x) for x in r["rects"]["radios"]]
        inputs = [pymupdf.Rect(*x) for x in r["rects"]["inputs"]]
        pua = [pymupdf.Rect(*x) for x in r["rects"]["pua"]]

        qrel = "img/q/%s.png" % r["qid"]
        qsize = render(page, clip, os.path.join(OUTBASE, qrel), radios, inputs, pua)

        arel = None
        if r["rects"].get("feed"):
            f = pymupdf.Rect(*r["rects"]["feed"])
            aclip = pymupdf.Rect(f.x0 + INSET, f.y0 + INSET, f.x1 - INSET, f.y1 - INSET)
            # the solution box needs no redaction: it is only shown after the
            # student commits an answer
            arel = "img/a/%s.png" % r["qid"]
            render(page, aclip, os.path.join(OUTBASE, arel), [], [], [], False)

        manifest.append({"qid": r["qid"], "img": qrel, "answer_img": arel,
                         "w": qsize[0], "h": qsize[1]})

    json.dump(manifest, open(os.path.join(D, "crops.json"), "w"), ensure_ascii=False, indent=1)
    sizes = [os.path.getsize(os.path.join(OUTBASE, m["img"])) for m in manifest]
    print("rendered", len(manifest), "questions,",
          sum(1 for m in manifest if m["answer_img"]), "answer crops")
    print("bytes min/median/max", min(sizes), sorted(sizes)[len(sizes) // 2], max(sizes))
    print("total", sum(sizes) // 1024, "KB")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="render question/answer crops")
    ap.add_argument("--in", dest="src", default=None, help="records json (default data/selection.json)")
    ap.add_argument("--out", dest="out", default=None, help="output root (default mth028/out)")
    ap.add_argument("--ids", dest="ids", default=None, help="comma separated qids, for spot checks")
    a = ap.parse_args()
    main(a.src, a.out, a.ids)
