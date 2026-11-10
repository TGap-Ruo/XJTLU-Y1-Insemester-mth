#!/usr/bin/env python3
"""Assign every item a secondary topic (二级目录) taken from the midterm
handout, then re-label the bank in that order.

Why this exists
---------------
The first-level topics came from a keyword classifier over the OCR stems, and it
was too coarse: "1.1 Systems of Linear Equations" ended up holding linear
independence, vector arithmetic and even column-space questions.  The handout
(`MTH028 线代期中自学课件.pdf`) splits each section into named 考点, so this
script re-reads every stem and files it under one of those 考点; an item's
section is then *derived* from its subtopic, which fixes the misfiled ones.

Inputs
    data/subtopics.json          the 二级目录 itself (id / topic / zh / en)
    data/subtopic_rules.json     regex -> subtopic, with weights
    data/subtopic_overrides.json {qid: subtopic} — a human always wins
    data/extract_v2.json         every record (reps and variants)

Output
    data/subtopic_map.json       qid -> {sub, topic, method, score}
    data/subtopic_report.txt     what moved, and what needs a human look

The rules run on a squashed form (lowercase, no spaces) because the PDF text
layer drops spaces: "Which system corresponds..." arrives as
"whichsystemcorrespondstothefollowingaugmentedmatrix".
"""
import json
import os
import re
import unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")


def squash(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("\u2212", "-")
    return re.sub(r"\s+", "", s)


def load(name, default):
    p = os.path.join(D, name)
    if not os.path.exists(p):
        print("  ! missing", name)
        return default
    return json.load(open(p, encoding="utf-8"))


def main():
    subs_doc = load("subtopics.json", {"subtopics": []})
    subs = subs_doc["subtopics"]
    by_id = {s["id"]: s for s in subs}
    topic_subs = defaultdict(list)
    for s in subs:
        topic_subs[s["topic"]].append(s["id"])
    for k in topic_subs:
        topic_subs[k].sort()

    rules = load("subtopic_rules.json", [])
    overrides = load("subtopic_overrides.json", {})
    if isinstance(overrides, dict) and "overrides" in overrides:
        overrides = overrides["overrides"]

    rows = load("extract_v2.json", [])
    print("records", len(rows), "| subtopics", len(subs), "| rules", len(rules))

    out, unmatched, moves = {}, [], []
    for r in rows:
        qid = r["qid"]
        text = squash((r.get("stem") or "") + " " +
                      " ".join((o.get("text") or "") for o in (r.get("options") or [])))
        if qid in overrides:
            ov = overrides[qid]
            sub = ov["sub"] if isinstance(ov, dict) else ov
            out[qid] = {"sub": sub, "topic": by_id[sub]["topic"],
                        "method": "manual", "score": 99}
            continue

        best = {}
        for rule in rules:
            pat = rule["re"]
            if re.search(pat, text):
                sub = rule["sub"]
                best[sub] = best.get(sub, 0) + int(rule.get("w", 1))
        if not best:
            # nothing matched: keep the item where the old classifier put it and
            # drop it into that section's first subtopic, flagged for review
            cand = topic_subs.get(str(r.get("topic")), [])
            sub = cand[0] if cand else subs[0]["id"]
            out[qid] = {"sub": sub, "topic": by_id[sub]["topic"],
                        "method": "fallback", "score": 0}
            unmatched.append((qid, r.get("topic"), squash(r.get("stem"))[:90]))
            continue

        # highest score wins; a tie goes to the subtopic of the item's old topic
        ranked = sorted(best.items(), key=lambda kv: (-kv[1], kv[0]))
        top = ranked[0][1]
        tied = [s for s, sc in ranked if sc == top]
        if len(tied) > 1:
            same = [s for s in tied if by_id[s]["topic"] == str(r.get("topic"))]
            sub = same[0] if same else tied[0]
        else:
            sub = ranked[0][0]
        out[qid] = {"sub": sub, "topic": by_id[sub]["topic"],
                    "method": "rules", "score": top}
        if str(r.get("topic")) != by_id[sub]["topic"]:
            moves.append((qid, r.get("topic"), by_id[sub]["topic"], sub))

    # A variant is the SAME question with new numbers, so it must land in the
    # template's 考点 -- OCR differences between two exports would otherwise
    # scatter one question across sections (it did: an inverse-transform copy
    # ended up under 1.1.1 while its template sat in 2.3.2).
    sel_path = os.path.join(D, "selection_all.json")
    if os.path.exists(sel_path):
        sel = {r["qid"]: r for r in json.load(open(sel_path, encoding="utf-8"))}
        fixed = 0
        for qid, rec in sel.items():
            rep = rec.get("variantOf")
            if not rep or qid not in out:
                continue
            if rep in out and out[qid]["sub"] != out[rep]["sub"]:
                out[qid] = {"sub": out[rep]["sub"], "topic": out[rep]["topic"],
                            "method": "variant-of-rep", "score": out[rep]["score"]}
                fixed += 1
        print("variants aligned to their template:", fixed)

    json.dump(out, open(os.path.join(D, "subtopic_map.json"), "w"),
              ensure_ascii=False, indent=0)

    dist = Counter(v["sub"] for v in out.values())
    print("\n-- per subtopic --")
    for s in subs:
        print("  %-7s %-34s %3d" % (s["id"], s["zh"], dist.get(s["id"], 0)))
    print("\nmethod:", dict(Counter(v["method"] for v in out.values())))

    rep = []
    rep.append("secondary-topic assignment report\n")
    rep.append("records %d, subtopics %d\n" % (len(rows), len(subs)))
    rep.append("\nmoved to another section: %d\n" % len(moves))
    for qid, a, b, sub in sorted(moves, key=lambda x: x[0]):
        rep.append("  %-8s %s -> %s (%s)\n" % (qid, a, b, sub))
    rep.append("\nno rule matched (fell back to old topic): %d\n" % len(unmatched))
    for qid, t, txt in unmatched:
        rep.append("  %-8s old=%s | %s\n" % (qid, t, txt))
    open(os.path.join(D, "subtopic_report.txt"), "w", encoding="utf-8").write("".join(rep))
    print("\nwrote data/subtopic_map.json and data/subtopic_report.txt")


if __name__ == "__main__":
    main()
