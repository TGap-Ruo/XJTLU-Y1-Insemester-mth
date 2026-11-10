#!/usr/bin/env python3
"""Turn the selected + cropped + mapped items into the four data files that
assemble_bank.py consumes, i.e. the same shape the previous delivery used.

    data/quiz_index.json      one header row per item
    data/quiz_structured.json stems / options / keys / answers
    data/crops.json           question + answer image per item
    data/topic_map.json       already produced by map_topics_v2.py

Item ids are preserved for every question that already existed (quiz N ->
N001..N015, so a student's stored progress keeps pointing at the same item).
The second bank (题库2) gets ids in the 21xxx..35xxx range, which no previous
item used.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")


def source_label(r):
    """Where the record came from: Q<n>-<qno> / B<n>-<qno> / H<n>-<qno>.

    This used to BE the display label; now the display label follows the
    secondary index (1.1.1-04), so the source is kept only as a traceable
    reference (hover text, admin console, duplicates report).
    """
    if r["qid"].startswith("b"):
        return "B%d-%02d" % (r["quiz"] - 20, r["qno"])
    if r["qid"].startswith("h"):
        return "H%d-%02d" % (r["quiz"] - 60, r["qno"])
    return "Q%d-%02d" % (r["quiz"], r["qno"])


def main():
    # Every record, reps and variants: the page lists the reps and folds each
    # template's other draws underneath it, so all of them need an image, an
    # answer and a label.
    sel = json.load(open(os.path.join(D, "selection_all.json")))
    crops = {c["qid"]: c for c in json.load(open(os.path.join(D, "crops.json")))}
    tmap = {m["qid"]: m["topic"] for m in
            json.load(open(os.path.join(D, "topic_map.json")))["mapping"]}

    # ---------- secondary index + renumbering ----------
    # The label now carries the two-level position: <section>.<sub>-<nn>.  The
    # numbering runs in subtopic order, so browsing the bank (or reading a
    # subtopic list) shows consecutive numbers inside each 考点.  A variant is
    # not a position in that list, so it is labelled "<its template>-v<k>".
    smap = json.load(open(os.path.join(D, "subtopic_map.json")))
    subs_doc = json.load(open(os.path.join(D, "subtopics.json")))
    subs = {s["id"]: s for s in subs_doc["subtopics"]}

    def sub_key(sid):
        return tuple(int(x) for x in sid.split("."))

    ordered = sorted(sel, key=lambda r: (sub_key(smap.get(r["qid"], {}).get("sub", "9.9.9")),
                                         r["quiz"], r["qno"]))
    label, seq = {}, {}
    for r in ordered:
        if r.get("variantOf"):
            continue
        sid = smap.get(r["qid"], {}).get("sub")
        if not sid:
            continue
        seq[sid] = seq.get(sid, 0) + 1
        label[r["qid"]] = "%s-%02d" % (sid, seq[sid])
    # variants follow their template, in a stable order
    vcount = {}
    for r in ordered:
        rep = r.get("variantOf")
        if not rep:
            continue
        base = label.get(rep)
        if not base:
            continue
        vcount[base] = vcount.get(base, 1) + 1
        label[r["qid"]] = "%s-v%d" % (base, vcount[base])

    idx, structured = [], []
    for r in sel:
        qid = r["qid"]
        c = crops.get(qid, {})
        ident = r["quiz"] * 1000 + r["qno"]
        src = source_label(r)
        lab = label.get(qid) or src
        sub = (smap.get(qid) or {}).get("sub")
        # the subtopic is authoritative for the section too (it fixed the items
        # the first classifier had filed under the wrong chapter)
        topic = (subs.get(sub) or {}).get("topic") or tmap.get(qid) or None
        blanks = int(r.get("blanks") or (1 if r["type"] == "fill" else 0))
        idx.append({
            "qid": qid, "quiz": r["quiz"], "qno": r["qno"],
            "type": r["type"],
            "has_printed_answer": bool(r.get("printed") or r.get("printedFull")),
        })
        structured.append({
            "qid": qid, "quiz": r["quiz"], "qno": r["qno"],
            "id": ident, "label": lab, "src": src, "sub": sub,
            # a fill item that asks for several values ("m = __, n = __") is a
            # cloze in this data model: the page renders one input per blank
            # and grades them one by one
            "type": ("cloze" if r["type"] == "fill" and blanks > 1 else r["type"]),
            "blanks": blanks,
            "topic": topic,
            "sub": sub,
            "variant_of": r.get("variantOf"),
            "stem": r["stem"],
            "options": [{"L": o["L"], "text": o["text"]} for o in r["options"]],
            "student_answer": r.get("student") or "",
            "verdict": (r.get("verdict") or "").lower(),
            "printed_answer_text": r.get("printed") or "",
            "suggested_key": r.get("key"),
            "key_confidence": r.get("keyConf") or "none",
            "key_method": r.get("keySrc") or "none",
            # answers travel verbatim: assemble_bank honours them when present
            "answers": r.get("answers"),
            "answer_text": r.get("answerText") or "",
            "answer_source": r.get("answerSrc") or "none",
            "ai_generated": bool(r.get("aiGenerated")),
            "img": c.get("img"),
            "answer_img": c.get("answer_img"),
            "notes": "",
        })

    json.dump(idx, open(os.path.join(D, "quiz_index.json"), "w"), ensure_ascii=False, indent=1)
    json.dump({"items": structured}, open(os.path.join(D, "quiz_structured.json"), "w"),
              ensure_ascii=False, indent=1)
    print("wrote %d index rows and %d structured items" % (len(idx), len(structured)))
    print("reps", sum(1 for s_ in structured if not s_["variant_of"]),
          "| variants", sum(1 for s_ in structured if s_["variant_of"]))
    print("ids", min(s["id"] for s in structured), "..", max(s["id"] for s in structured))
    dup = len(structured) - len({s["id"] for s in structured})
    print("duplicate ids:", dup)
    print("choice with key:", sum(1 for s in structured if s["type"] == "choice" and s["suggested_key"]),
          "/", sum(1 for s in structured if s["type"] == "choice"))
    print("fill with answers:", sum(1 for s in structured if s["type"] == "fill" and s["answers"]),
          "/", sum(1 for s in structured if s["type"] == "fill"))


if __name__ == "__main__":
    main()
