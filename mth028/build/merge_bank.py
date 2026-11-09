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


def label_for(r):
    if r["qid"].startswith("b"):
        return "B%d-%02d" % (r["quiz"] - 20, r["qno"])
    return "Q%d-%02d" % (r["quiz"], r["qno"])


def main():
    sel = json.load(open(os.path.join(D, "selection.json")))
    crops = {c["qid"]: c for c in json.load(open(os.path.join(D, "crops.json")))}
    tmap = {m["qid"]: m["topic"] for m in
            json.load(open(os.path.join(D, "topic_map.json")))["mapping"]}

    idx, structured = [], []
    for r in sel:
        qid = r["qid"]
        c = crops.get(qid, {})
        ident = r["quiz"] * 1000 + r["qno"]
        label = label_for(r)
        blanks = int(r.get("blanks") or (1 if r["type"] == "fill" else 0))
        idx.append({
            "qid": qid, "quiz": r["quiz"], "qno": r["qno"],
            "type": r["type"],
            "has_printed_answer": bool(r.get("printed") or r.get("printedFull")),
        })
        structured.append({
            "qid": qid, "quiz": r["quiz"], "qno": r["qno"],
            "id": ident, "label": label,
            # a fill item that asks for several values ("m = __, n = __") is a
            # cloze in this data model: the page renders one input per blank
            # and grades them one by one
            "type": ("cloze" if r["type"] == "fill" and blanks > 1 else r["type"]),
            "blanks": blanks,
            "topic": tmap.get(qid),
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
    print("ids", min(s["id"] for s in structured), "..", max(s["id"] for s in structured))
    dup = len(structured) - len({s["id"] for s in structured})
    print("duplicate ids:", dup)
    print("choice with key:", sum(1 for s in structured if s["type"] == "choice" and s["suggested_key"]),
          "/", sum(1 for s in structured if s["type"] == "choice"))
    print("fill with answers:", sum(1 for s in structured if s["type"] == "fill" and s["answers"]),
          "/", sum(1 for s in structured if s["type"] == "fill"))


if __name__ == "__main__":
    main()
