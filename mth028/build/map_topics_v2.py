#!/usr/bin/env python3
"""Assign every selected MTH028 item to a course section (1.1 - 2.8).

Two sources, in order of authority:

 1. data/topic_map.json as shipped before -- those labels were human-audited for
    the original 150 items, so they are never recomputed.
 2. a keyword classifier for everything new, extended with the Chapter 2
    vocabulary that the Quiz 3 exports introduced (matrix operations, inverses,
    invertibility, null space / col A).

data/topic_map_overrides.json still wins over both, so any item can be moved by
editing one line.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")

# section -> patterns; the first section with the strongest hit wins
RULES = [
    ("2.3", [r"notinvertible", r"isinvertible", r"invertiblematrix",
             r"a\^?3\s*=\s*i", r"a3i", r"characteriz", r"elementarymatrix",
             r"elementar(y|ies)"]),
    ("2.2", [r"inverseof", r"findtheinverse", r"a−1", r"a-1", r"theinverse",
             r"invertiblematrices", r"c−1a", r"c-1a", r"b−1"]),
    ("2.8", [r"nullspace", r"nula", r"cola", r"basisfor", r"subspace",
             r"isnotincol", r"columnspace"]),
    ("2.1", [r"transpose", r"at\b", r"atb", r"utv", r"uvt", r"scalar",
             r"entryofthematrix", r"matrixproduct", r"computetheproduct",
             r"productofthematrices", r"(1, 2)-entry", r"(2, 1)-entry",
             r"(3, 1)-entry", r"(1, 3)-entry", r"(3, 2)-entry"]),
    ("1.9", [r"standardmatrix", r"matrixofthelineartransformation",
             r"rotation", r"shear", r"projection"]),
    ("1.8", [r"lineartransformation", r"mapsto", r"one.to.one", r"\bonto\b",
             r"codomain", r"domain", r"rangeof", r"imageof"]),
    ("1.7", [r"linearly(in|de)pendent", r"linear(in|de)pendence",
             r"dependencerelation", r"dependent", r"independent"]),
    ("1.5", [r"homogeneous", r"nontrivialsolution", r"trivialsolution",
             r"parametricvectorform", r"generalsolution", r"solutionset"]),
    ("1.4", [r"\bax=b\b", r"axb", r"matrixequation", r"identitymatrix",
             r"consistentfor(all|every)", r"doesnotspan", r"spanof"]),
    ("1.3", [r"linearcombination", r"\bspan", r"vectorequation", r"weights?",
             r"columnvector", r"writeavectorequation"]),
    ("1.2", [r"echelon", r"rref", r"pivot", r"leadingentr", r"basicvariable",
             r"freevariable", r"rowreduc", r"backwardphase", r"forwardphase"]),
    ("1.1", [r"augmentedmatrix", r"coefficientmatrix", r"consistent",
             r"inconsistent", r"rowoperation", r"replacerow", r"elementaryrow",
             r"rowequivalent", r"solutionofthesystem"]),
]
FALLBACK = "1.1"


def squash(s):
    return re.sub(r"\s+", "", (s or "").lower())


def classify(stem, options):
    text = squash(stem)
    opts = " ".join(squash(o.get("text", "")) for o in options)
    best, best_n = None, 0
    for sec, pats in RULES:
        n = 0
        for p in pats:
            if re.search(p, text) or re.search(p, opts):
                n += 1
        if n > best_n:
            best, best_n = sec, n
    return (best or FALLBACK), best_n


def main():
    sel = json.load(open(os.path.join(D, "selection.json")))
    old = {}
    p = os.path.join(D, "topic_map.json")
    if os.path.exists(p):
        doc = json.load(open(p))
        for m in doc.get("mapping", []):
            old[m["qid"]] = m
    overrides = {}
    p2 = os.path.join(D, "topic_map_overrides.json")
    if os.path.exists(p2):
        for o in json.load(open(p2)).get("overrides", []):
            overrides[o["qid"]] = o["topic"]

    out, dist, fresh = [], {}, 0
    for r in sel:
        qid = r["qid"]
        legacy = "q" + qid[1:] if qid.startswith("p") else None
        if qid in overrides:
            topic, conf, src = overrides[qid], 99, "override"
        elif legacy and legacy in old:
            topic, conf, src = old[legacy]["topic"], old[legacy].get("confidence", 0), "kept"
        elif qid in old:
            topic, conf, src = old[qid]["topic"], old[qid].get("confidence", 0), "kept"
        else:
            topic, conf = classify(r["stem"], r["options"])
            src = "classified"
            fresh += 1
        dist[topic] = dist.get(topic, 0) + 1
        out.append({"qid": qid, "quiz": r["quiz"], "qno": r["qno"], "topic": topic,
                    "confidence": conf, "source": src, "stem": r["stem"]})

    json.dump({"mapping": out,
               "note": "section per item; edit topic_map_overrides.json to move one"},
              open(os.path.join(D, "topic_map.json"), "w"), ensure_ascii=False, indent=1)
    print("mapped", len(out), "items;", fresh, "newly classified")
    tests = [t["id"] for t in json.load(open(os.path.join(D, "topics.json")))["topics"]]
    for t in tests:
        print("  %-4s %3d" % (t, dist.get(t, 0)))
    empty = [t for t in tests if not dist.get(t)]
    print("  topics with no question:", ", ".join(empty) or "-")
    print("  unclassified (0 keywords):", sum(1 for x in out if x["confidence"] == 0))


if __name__ == "__main__":
    main()
