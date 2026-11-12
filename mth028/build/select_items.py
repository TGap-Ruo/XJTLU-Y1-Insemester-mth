#!/usr/bin/env python3
"""Decide the answer key of every extracted question, then drop duplicates.

Two problems this solves:

1. Choice keys.  The review export marks the right option with a tick glyph, but
   only for attempts that were actually answered -- 24 of 280 here.  The rest
   only print "The correct answer is: <option content>", so the key is recovered
   by comparing that text with each option (exact, then digit-multiset, then
   fuzzy).  Where a tick exists it wins; a disagreement is reported.

2. Duplicates.  Moodle draws a fresh set of numbers for every attempt, so the
   same template shows up many times across the 30 exports.  Items are grouped
   by a fingerprint of stem+options with every digit replaced by "#": identical
   fingerprints are the same question, only re-parameterised.  One representative
   per group survives -- preferring the copy that has a printed key.

Output: data/selection.json  (the items that go into the site)
        data/duplicates.json (what was merged away, for audit)
"""
import json
import os
import re
import difflib
import unicodedata
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")

NUM = re.compile(r"−?\d+(?:\.\d+)?")


BRACKETS = "⎡⎢⎣⎤⎥⎦⎧⎨⎩⎫⎬⎭[]{}()"


def norm(s):
    """Comparison form: drop layout only, keep signs (they distinguish options)."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s).lower()
    s = "".join(ch for ch in s if ch not in BRACKETS)
    return re.sub(r"\s+", "", s)


def digits(s):
    if not s:
        return []
    s = unicodedata.normalize("NFKC", s).replace("−", "-")
    return re.findall(r"-?\d+(?:\.\d+)?", s)


def key_from_text(printed, options):
    """Which option does the printed answer box duplicate?

    Moodle prints the winning option verbatim, so equality is decisive.  When
    the extraction only recovered part of a tall matrix or system, the printed
    text is a fragment of the right option -- containment then decides, and a
    tighter match (shorter option) is preferred.  Signs are preserved
    throughout: "-78" and "78" are different answers.
    """
    p = norm(printed)
    if not p:
        return None, 0.0, "none"
    scored = []
    for o in options:
        t = norm(o["text"])
        if not t:
            scored.append((0.0, o["L"]))
            continue
        if p == t:
            scored.append((1.0, o["L"]))
            continue
        if len(p) >= 3 and p in t:
            # tighter containment = the option adds less extra material
            scored.append((0.95 + 0.04 * len(p) / len(t), o["L"]))
            continue
        if len(t) >= 3 and t in p:
            scored.append((0.90 + 0.04 * len(t) / len(p), o["L"]))
            continue
        scored.append((difflib.SequenceMatcher(None, p, t).ratio(), o["L"]))
    scored.sort(reverse=True)
    best = scored[0]
    method = ("exact" if best[0] >= 0.999 else
              "contain" if best[0] >= 0.90 else "fuzzy")
    return best[1], best[0], method


def main():
    rows = json.load(open(os.path.join(D, "extract_v2.json")))
    old = {x["qid"].replace("q", "p"): x
           for x in json.load(open(os.path.join(D, "quiz_structured.json")))["items"]}

    # ---------- 1. answer keys ----------
    stats = Counter()
    for r in rows:
        r["key"] = None
        r["keySrc"] = "none"
        r["keyConf"] = "none"
        # a fill item's value never needs a letter key
        if r["type"] != "choice":
            continue
        if r["tick"]:
            r["key"], r["keySrc"], r["keyConf"] = r["tick"], "tick", "high"
            stats["tick"] += 1
            if r["printed"]:
                other, sc, _ = key_from_text(r["printed"], r["options"])
                if other and other != r["tick"] and sc > 0.9:
                    stats["tick/text disagree"] += 1
                    print("  ! tick/text disagree %s tick=%s text=%s(%.2f)"
                          % (r["qid"], r["tick"], other, sc))
            continue
        # Two sources: the value printed on the "The correct answer is:" line
        # (clean but sometimes a fragment) and the whole answer box (complete
        # but can drag in the tail of the explanation above it).  Try the clean
        # line first and only fall back to the box when it cannot decide.
        def match(txt):
            L, sc, method = key_from_text(txt, r["options"])
            _, sc2, _ = key_from_text(txt, [o for o in r["options"] if o["L"] != L])
            return L, sc, method, sc - sc2

        L1, s1, m1, d1 = match(r.get("printed"))
        L2, s2, m2, d2 = match(r.get("printedFull") or r["printed"])
        pick = None
        if m1 == "exact":
            pick = (L1, m1, "high")
        elif m2 == "exact":
            pick = (L2, m2, "high")
        elif m1 in ("contain", "fuzzy") and s1 >= 0.9 and d1 >= 0.02:
            pick = (L1, m1, "high")
        elif m2 in ("contain", "fuzzy") and s2 >= 0.9 and d2 >= 0.02:
            pick = (L2, m2, "high")
        elif L1 and L2 and L1 == L2 and s1 >= 0.72:
            pick = (L1, m1, "medium")
        elif m2 == "contain" and s2 >= 0.9:
            pick = (L2, m2, "medium")
        elif m1 == "fuzzy" and s1 >= 0.72 and d1 >= 0.12:
            pick = (L1, m1, "medium")
        elif m2 == "fuzzy" and s2 >= 0.72 and d2 >= 0.12:
            pick = (L2, m2, "medium")
        else:
            pick = (L2 or L1, m2 if L2 else m1, "low")
        r["key"], r["keySrc"], r["keyConf"] = pick
        stats[pick[2]] += 1

    print("choice keys:", dict(stats))

    # validate against the keys the previous delivery shipped (same questions)
    agree = dis = 0
    for r in rows:
        if r["type"] != "choice" or not r["key"] or r["qid"] not in old:
            continue
        o = old[r["qid"]]
        if not o.get("suggested_key"):
            continue
        if o["suggested_key"] == r["key"]:
            agree += 1
        else:
            dis += 1
            if dis <= 8:
                print("  ~ %s old=%s new=%s (%s %.2f)" % (r["qid"], o["suggested_key"],
                                                          r["key"], r["keySrc"], 0))
    print("vs previous delivery: agree=%d disagree=%d" % (agree, dis))

    # ---------- 2. duplicates ----------
    # Moodle re-draws the numbers for every attempt, so the same template comes
    # back with different values.  Group by "same stem AND same option shapes",
    # ignoring digits; one representative survives, preferring the copy that
    # carries a printed key and a letter-clean type.
    def shape(r):
        s = norm(r["stem"])
        s = NUM.sub("#", s)
        opts = "|".join(NUM.sub("#", norm(o["text"])) for o in r["options"])
        return s, opts

    # Keep the representative of a template stable across rebuilds: an item
    # that already shipped keeps its id, so a student's stored progress and
    # favourites still point at the same question.
    LEGACY = {"p%d-%02d" % (q, n) for q in range(1, 11) for n in range(1, 16)}

    def rank(r):
        return (1 if (r["key"] or r["printed"]) else 0,
                1 if r["keyConf"] == "high" else 0,
                1 if r["verdict"] == "Correct" else 0,
                1 if r["qid"] in LEGACY else 0,
                r["quiz"])

    pool = sorted(rows, key=rank, reverse=True)
    reps, dropped, merged = [], [], {}
    for r in pool:
        rs, ro = shape(r)
        hit = None
        for keep_ in reps:
            if keep_["type"] != r["type"] or len(keep_["options"]) != len(r["options"]):
                continue
            ks, ko = shape(keep_)
            if difflib.SequenceMatcher(None, rs, ks).ratio() >= 0.94 \
                    and difflib.SequenceMatcher(None, ro, ko).ratio() >= 0.90:
                hit = keep_
                break
        if hit is None:
            reps.append(r)
        else:
            dropped.append({"qid": r["qid"], "file": r["file"], "qno": r["qno"],
                            "mergedInto": hit["qid"]})
            merged.setdefault(hit["qid"], []).append(r["qid"])
    for r in reps:
        r["isRep"] = True
        r["variantOf"] = None
    # The variants are kept as first-class records: they are the same template
    # with a fresh draw of numbers, so they are valid practice (the page shows
    # them folded under their template instead of in the main list).
    byqid = {r["qid"]: r for r in rows}
    for d in dropped:
        v = byqid[d["qid"]]
        v["isRep"] = False
        v["variantOf"] = d["mergedInto"]
        d["variantLabel"] = None            # filled in below, for the audit file
    keep = reps
    keep.sort(key=lambda r: (r["quiz"], r["qno"]))
    print("raw %d -> unique %d (merged %d variants kept as practice)"
          % (len(rows), len(keep), len(dropped)))
    big = sorted(merged.items(), key=lambda kv: -len(kv[1]))[:4]
    for q, lst in big:
        print("   %s <- %s" % (q, ", ".join(lst)))

    # ---------- 3. per-item answer payload ----------
    # One input box per blank -- a fill item can ask for several values
    # ("m = __, n = __"), and grading compares them one by one.
    # This runs over EVERY record, not just the representatives: a variant is a
    # different draw of the same template, so it has its own numbers and its own
    # answer, and it must be gradable on its own.
    for r in rows:
        r["blanks"] = max(1, len(r["rects"]["inputs"])) if r["type"] == "fill" else 0
        r["answers"] = None
        r["answerText"] = ""
        r["answerSrc"] = "none"
        r["aiGenerated"] = False
        if r["type"] == "choice":
            continue
        nb = r["blanks"]
        pr = (r["printed"] or "").strip()
        simple = bool(pr) and len(pr) <= 40 and not re.search(r"[⎡⎢⎣⎤⎥⎦⎧⎨⎩]", pr)
        typed = [t for t in re.split(r"[\s,;]+", (r.get("student") or "").strip()) if t]
        if simple and nb == 1:
            r["answers"] = [pr]
            r["answerSrc"] = "pdf"
        elif typed and r["verdict"] == "Correct" and len(typed) == nb:
            r["answers"] = typed
            r["answerSrc"] = "pdf"
        elif simple and nb > 1:
            parts = [t for t in re.split(r"[,;]|\s{2,}", pr) if t.strip()]
            if len(parts) == nb:
                r["answers"] = [p.strip() for p in parts]
                r["answerSrc"] = "pdf"
        if r["answers"]:
            r["answerText"] = ", ".join(r["answers"]) if nb > 1 else r["answers"][0]
        elif pr:
            r["answerText"] = pr          # display only; the reader grades it
            r["answerSrc"] = "pdf-crop"

    # ---------- 4. human / vision corrections ----------
    # Some answer boxes print nothing at all (the attempt was never submitted).
    # Those were computed by hand and checked with sympy; ambiguous choice keys
    # were confirmed by looking at the rendered answer box.  Both live in one
    # editable file so a wrong entry can be fixed without touching code.
    fx_path = os.path.join(D, "answer_fixes.json")
    if os.path.exists(fx_path):
        fx = json.load(open(fx_path))
        # a fix is keyed by qid, but the qid that represents a template can
        # change when a better copy is picked; follow the merge trail so a fix
        # follows its question instead of silently dropping out
        # A fix applies to EXACTLY one record.  Do not look it up through the
        # dedup group: members of a group share a template but not their
        # numbers, so the answer of one instance is wrong for another (this
        # actually shipped once: an inverse-of-A answer was copied onto a
        # different matrix).  If the fixed qid is no longer the representative,
        # the fix is simply unused and the item shows up as "needs an answer".
        dup_path = os.path.join(D, "duplicates.json")
        dropped_to = {}
        if os.path.exists(dup_path):
            for d in json.load(open(dup_path)):
                dropped_to[d["qid"]] = d["mergedInto"]

        def lookup(bucket, qid):
            if qid in bucket:
                return bucket[qid]
            return None

        def why_dropped(qid):
            tgt = dropped_to.get(qid)
            return (" (that copy was merged into %s)" % tgt) if tgt else ""

        nf = nc = 0
        for r in rows:
            f = lookup(fx.get("fill") or {}, r["qid"])
            # once the export itself prints an answer, the paper wins over the
            # hand-computed one (it also caught one mis-read value)
            if f and f.get("answers") and r["answerSrc"] != "pdf":
                r["blanks"] = int(f.get("blanks") or len(f["answers"]))
                r["answers"] = [str(a) for a in f["answers"]]
                r["answerText"] = ", ".join(r["answers"])
                # "from": "paper" marks a value that was read out of the
                # review page's own explanation, so it must NOT carry the
                # AI-generated badge.
                if f.get("from") == "paper":
                    r["answerSrc"] = "pdf"
                    r["aiGenerated"] = False
                else:
                    r["answerSrc"] = "ai"
                    r["aiGenerated"] = True
                nf += 1
            c = lookup(fx.get("choice") or {}, r["qid"])
            if c:
                if isinstance(c, dict):
                    # computed key (no printed answer existed) -> must carry the
                    # AI badge on the site
                    r["key"] = c.get("key")
                    r["keySrc"] = "ai-computed"
                    r["aiGenerated"] = True
                    r["answerSrc"] = "ai"
                else:
                    r["key"] = c
                    r["keySrc"] = "vision"
                r["keyConf"] = "high"
                nc += 1
        print("fixes applied: %d fill answers, %d choice keys" % (nf, nc))

    json.dump(keep, open(os.path.join(D, "selection.json"), "w"),
              ensure_ascii=False, indent=1)
    # Every record, representative and variant alike.  The page shows the reps
    # in the main list and folds the variants under their template; the admin
    # console and the crop renderer read this file.
    allrows = sorted(rows, key=lambda r: (r["quiz"], r["qno"]))
    json.dump(allrows, open(os.path.join(D, "selection_all.json"), "w"),
              ensure_ascii=False, indent=1)
    json.dump(dropped, open(os.path.join(D, "duplicates.json"), "w"),
              ensure_ascii=False, indent=1)
    un = [r for r in keep if r["type"] == "fill" and not r["answers"]]
    print("selected", len(keep), "| choice", sum(1 for r in keep if r["type"] == "choice"),
          "| fill", sum(1 for r in keep if r["type"] == "fill"))
    vb = [r for r in allrows if r["variantOf"]]
    print("all records:", len(allrows), "| variants:", len(vb),
          "| variants gradable:",
          sum(1 for r in vb if (r["key"] if r["type"] == "choice" else r["answers"])))
    print("fill needing an answer:", len(un))
    print("choice without key:", sum(1 for r in keep if r["type"] == "choice" and not r["key"]))


if __name__ == "__main__":
    main()
