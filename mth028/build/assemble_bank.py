#!/usr/bin/env python3
"""Assemble out/bank.js from the independent data files.

Everything the page needs lives in ONE external file.  To add a new question
or a new topic later you only edit data/*.json (or append a row) and re-run
this script -- the page code never changes.  Missing input files degrade to
empty arrays instead of crashing, so a partial delivery still boots.

Inputs (all optional except quiz_index/crops which we generate ourselves):
  data/quiz_structured.json  scout-quiz : 150 items with stems, options, keys
  data/quiz_index.json       our index  : fallback source of the 150 items
  data/crops.json            our crops  : question image + answer image paths
  data/topic_map.json        our map    : qid -> section id
  data/topics.json           scout-topics: 17 sections + 2 chapters
  data/glossary.json         vocabulary : 33 groups / 212 terms
  data/ai_answers.json       AI answers : the 30 items with no printed answer

Output: out/bank.js   ->   window.MTH028_BANK = {...};
"""
import argparse
import json
import os
import re
import unicodedata

# Resolve relative to this file so the script works both in the development
# tree (mth028/) and in the committed copy (repo/mth028/).
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "out", "bank.js")


def load(name, default):
    p = os.path.join(D, name)
    if not os.path.exists(p):
        print("  ! missing %-24s -> %s" % (name, default))
        return default
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception as e:
        print("  ! broken  %-24s -> %s (%s)" % (name, default, e))
        return default


def clean_answer_text(s):
    """Reduce the printed answer line to something a student could type."""
    if not s:
        return None
    t = unicodedata.normalize("NFKC", str(s))
    t = re.sub(r"(?i)the\s*correct\s*answer\s*is\s*:?", " ", t)
    t = t.replace("\u2212", "-").replace("\u2013", "-").replace("\u00a0", " ")
    t = re.sub(r"[|]", " ", t)
    t = re.sub(r"\s+", " ", t).strip(" .;:,|")
    t = re.sub(r"^Answer\s*:?", "", t, flags=re.I).strip()
    # matrix / system / long prose: too fragile to auto-grade
    if not t or len(t) > 90 or any(c in t for c in "⎡⎢⎣⎤⎥⎦⎧⎨⎩\n"):
        return None
    return t or None


def split_blanks(s, blanks):
    """A cloze answer may arrive as '4, 2' or '[4,2]' -> per-blank strings."""
    if not s:
        return None
    if blanks <= 1:
        return [s]
    parts = re.split(r"[,;/]\s*|\s{2,}", s)
    parts = [p.strip(" []()") for p in parts if p.strip(" []()")]
    return parts if len(parts) == blanks else [s]


def esc_text(s):
    """JSON-safe plain text; math stays as $...$ for KaTeX."""
    if s is None:
        return ""
    return str(s).replace("\r", " ").replace("\n", " ").strip()


def main(out_override=None):
    global OUT
    if out_override:
        OUT = os.path.abspath(out_override)
    idx = load("quiz_index.json", [])
    crops = {c["qid"]: c for c in load("crops.json", [])}
    structured = load("quiz_structured.json", {})
    sitems = {x.get("qid"): x for x in (structured.get("items") or [])}
    tmap = {x["qid"]: x for x in load("topic_map.json", {}).get("mapping", [])}
    # Human audited corrections win over the keyword classifier.
    overrides = load("topic_map_overrides.json", {}).get("overrides", [])
    for o in overrides:
        if o.get("qid") in tmap and o.get("topic"):
            tmap[o["qid"]] = dict(tmap[o["qid"]], topic=o["topic"])
    print("  topic overrides applied:", len(overrides))
    topics_doc = load("topics.json", None)
    if not topics_doc or not topics_doc.get("topics"):
        print("  ! topics.json not delivered -> using topics_fallback.json")
        topics_doc = load("topics_fallback.json", {"chapters": [], "topics": []})
    glossary = load("glossary.json", {"groups": []})
    ai_doc = load("ai_answers.json", {"items": []})
    ai = {x["qid"]: x for x in ai_doc.get("items", [])}

    chapters = topics_doc.get("chapters") or [
        {"n": "1", "en": "Linear Equations in Linear Algebra", "zh": "线性代数中的线性方程组"},
        {"n": "2", "en": "Matrix Algebra", "zh": "矩阵代数"},
    ]
    topics = topics_doc.get("topics") or []
    sec_ch = {t["id"]: t.get("ch", 0) for t in topics}

    items = []
    for r in idx:
        qid = r["qid"]
        s = sitems.get(qid, {})
        c = crops.get(qid, {})
        m = tmap.get(qid, {})
        airow = ai.get(qid)

        qtype = s.get("type") or r["type"]
        if qtype not in ("choice", "fill", "cloze"):
            qtype = "fill" if qtype == "fill" else "choice"
        # Trust the measured blank count.  Some cloze items genuinely have a
        # single blank (15 of the 30); forcing them to 2 would misalign the
        # answer array and break per-blank grading.
        blanks = int(s.get("blanks") or (1 if qtype in ("fill", "cloze") else 0))

        # merge_bank already resolved the section for every record (a variant
        # inherits its template's section), so prefer its value and fall back to
        # the classifier's map
        topic = s.get("topic") or m.get("topic") or None
        # printed answer (from quiz_structured, else our crop manifest)
        printed = s.get("printed_answer_text") or c.get("printed_answer_text")
        key = s.get("suggested_key") or None
        conf = s.get("key_confidence") or "none"
        if key and (conf in ("none", "low")):
            key = None
        options = [o["L"] if isinstance(o, dict) else str(o)
                   for o in (s.get("options") or [])] or ["A", "B", "C", "D"]

        # scout-quiz marks matrix / system / multi-row answers as
        # "complex-answer": one input box but a vector or matrix as the answer.
        # They cannot be graded by a string comparison, so leave `answers` null
        # and let the page fall back to the printed-answer crop + self marking.
        complex_answer = ("complex-answer" in (s.get("notes") or "")
                          or "|" in (printed or ""))
        answers, answer_text, source, ai_generated = None, None, "none", False
        # Items delivered by the v2 extractor already carry the grading payload
        # (it had the exact card rectangles, so it knows what the printed answer
        # really says).  Honour it verbatim instead of re-parsing OCR text.
        if s.get("answer_source") and s.get("answer_source") != "none":
            answers = s.get("answers")
            answer_text = s.get("answer_text") or None
            source = s["answer_source"]
            ai_generated = bool(s.get("ai_generated"))
        elif qtype == "choice":
            source = "pdf" if r["has_printed_answer"] else "none"
            # Choice questions: the key letter + printed-answer image are the
            # reference.  The OCR'd text of a matrix/system answer is garbled
            # (e.g. "−656 | −98−3") and would confuse students, so suppress it.
        elif complex_answer:
            source = "pdf" if r["has_printed_answer"] else "none"
            # OCR of a matrix/system answer is garbled, but the numeric answer
            # (e.g. "10" from "Thecorrectansweris:10 | 14 | Question") is usually
            # embedded at the front.  Extract the first numeric token; if it's a
            # simple number, auto-grade it too.
            cleaned = clean_answer_text(printed)
            if cleaned:
                parts = cleaned.split()
                answer_text = parts[0] if parts else None
                # Auto-grade if the first token is a simple number (integer/decimal)
                # and the question has exactly one blank.
                if answer_text and blanks == 1 and re.match(r"^-?\d+(\.\d+)?$", answer_text):
                    answers = [answer_text]
            else:
                answer_text = None
        else:
            txt = clean_answer_text(printed)
            if txt:
                parts = split_blanks(txt, blanks)
                # Per-blank grading requires exactly one answer per blank.
                # A mismatch is safer as "self-check" than as a wrong key.
                if len(parts) == blanks:
                    answers, answer_text, source = parts, txt, "pdf"
            if answers is None and airow:
                vals = airow.get("answer") or []
                vals = vals if isinstance(vals, list) else [vals]
                if len(vals) == blanks:
                    answers = [str(v) for v in vals]
                    answer_text = airow.get("answer_display") or ", ".join(map(str, vals))
                    source, ai_generated = "ai", True

        notes = s.get("notes") or ""
        if ai_generated:
            notes = (notes + "; AI-generated answer; original review page did not print one").strip("; ")
        if printed and not answers and qtype != "choice" and not ai_generated \
                and "complex-answer" not in notes:
            notes = (notes + "; complex-answer: grade yourself against the printed answer crop").strip("; ")

        items.append({
            "id": int(s.get("id") or (r["quiz"] * 1000 + r["qno"])),
            "label": s.get("label") or "Q%d-%02d" % (r["quiz"], r["qno"]),
            "qid": qid,
            "quiz": r["quiz"], "qno": r["qno"],
            "type": qtype, "blanks": blanks,
            "topic": topic, "chapter": sec_ch.get(topic, 0),
            "img": c.get("img"),
            "answerImg": c.get("answer_img"),
            "key": key,
            "keyConfidence": conf,
            "answers": answers,
            "answerText": esc_text(answer_text),
            "answerSource": source,
            "aiGenerated": ai_generated,
            "options": options,
            "stem": esc_text(s.get("stem") or m.get("stem")),
            # null for a template's representative; otherwise the qid of the
            # representative this record is folded under
            "variantOf": s.get("variant_of") or None,
            "notes": esc_text(notes),
        })

    bank = {
        "meta": {"course": "MTH028", "en": "Linear Algebra I",
                 "zh": "线性代数（一）", "version": 1,
                 # total counts every gradable record (variants included);
                 # "main" counts the representatives, which is what the bank
                 # list, the topic bars and the smart rounds use
                 "total": len(items),
                 "main": sum(1 for i in items if not i.get("variantOf")),
                 "variants": sum(1 for i in items if i.get("variantOf")),
                 "topics": len(topics)},
        "chapters": chapters,
        "topics": topics,
        "items": items,
        "glossary": {"groups": glossary.get("groups", [])},
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("window.MTH028_BANK = ")
        json.dump(bank, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")

    from collections import Counter
    print("bank.js", os.path.getsize(OUT), "bytes")
    print("  items", len(items), "main", bank["meta"]["main"],
          "variants", bank["meta"]["variants"],
          "types", dict(Counter(i["type"] for i in items)))
    print("  topics", len(topics), "chapters", len(chapters),
          "glossary", sum(len(g.get("items", [])) for g in bank["glossary"]["groups"]))
    print("  key(auto-grade choice)", sum(1 for i in items if i["key"]))
    print("  answers(auto-grade fill)", sum(1 for i in items if i["answers"]))
    print("  AI answers", sum(1 for i in items if i["aiGenerated"]))
    print("  items with topic", sum(1 for i in items if i["topic"]))
    print("  missing images", sum(1 for i in items if not i["img"]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Assemble MTH028 bank.js from data/*.json")
    ap.add_argument("--out", default=None,
                    help="output path (default: <project>/out/bank.js)")
    args = ap.parse_args()
    main(args.out)
